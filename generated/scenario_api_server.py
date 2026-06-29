# -*- coding: utf-8 -*-
"""HTTP API wrapper for generated Kaipanla capture scenarios."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, unquote, urlparse

from auth_store import AuthStore
from kaipanla_capture_client import KaipanlaCapturedClient, REQUESTS
from kpl_core_client import CORE_API_KEYS, CORE_LOCAL_API_KEYS, KaipanlaCoreClient
from kpl_hqstock_decoder import (
    DEFAULT_LOG as HQSTOCK_LOG,
    HQ_API_KEYS,
    latest_five_level,
    latest_stock_for_code,
    latest_time_sales,
    normalize_stock_id,
)


ROOT = Path(__file__).resolve().parent
TOOLS_DIR = ROOT.parent / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
try:
    from crawl_topic_library import crawl_topic_library, write_outputs
except ModuleNotFoundError:
    crawl_topic_library = None
    write_outputs = None

CLIENT_FILE = "kaipanla_capture_client.py"
PAGE_FILE = "capture_scenarios.html"
LOGIN_FILE = "login.html"
REGISTER_FILE = "register.html"
EXPIRED_FILE = "expired.html"
ADMIN_FILE = "admin.html"
AUTH_DB_FILE = ROOT / "users.json"
SCENARIO_LEVEL_FILE = ROOT / "scenario_levels.json"
SCENARIO_META_FILE = ROOT / "scenario_meta.json"
CALL_LOG_FILE = ROOT / "scenario_call_logs.jsonl"
FRIDA_CAPTURE_LOG = ROOT.parent / "outputs" / "frida" / "kpl_capture.ndjson"
DEFAULT_INTERFACE_ADDED_TIME = "2026-06-25"
SESSION_COOKIE = "kpl_session"
AUTH = AuthStore(AUTH_DB_FILE)
SENSITIVE_LOG_KEYS = {"token", "userid", "deviceid", "clientsign", "log", "datalist"}
MAX_CALL_LOGS = 1000
UPSTREAM_IDENTITY_CACHE: dict[str, object] = {"mtime": 0.0, "identity": {}}
CORE_LOCAL_ADDED_TIME = "2026-06-28"
CORE_LOCAL_TITLES = {
    "five_level": {
        "method_name": "hqstock_five_level",
        "title_cn": "行情核心-五档盘口",
        "params": {"StockID": "688008"},
    },
    "time_sales": {
        "method_name": "hqstock_time_sales",
        "title_cn": "行情核心-分时成交",
        "params": {"StockID": "688008", "limit": "100"},
    },
}


def _safe_route_part(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


SCENARIO_LEVELS = {
    "normal": "一般",
    "important": "重要",
    "rare": "稀缺",
    "pending_delete": "待删除",
}


def _load_scenario_meta_data() -> dict[str, dict[str, str]]:
    payload: object = {}
    if SCENARIO_META_FILE.exists():
        try:
            payload = json.loads(SCENARIO_META_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
    elif SCENARIO_LEVEL_FILE.exists():
        # Backward compatibility for installs that already saved level tags.
        try:
            level_payload = json.loads(SCENARIO_LEVEL_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            level_payload = {}
        raw_levels = level_payload.get("levels", level_payload) if isinstance(level_payload, dict) else {}
        if isinstance(raw_levels, dict):
            payload = {
                "scenarios": {
                    str(session_id): {"level": str(level)}
                    for session_id, level in raw_levels.items()
                }
            }
    raw_scenarios = payload.get("scenarios", payload) if isinstance(payload, dict) else {}
    if not isinstance(raw_scenarios, dict):
        return {}
    normalized: dict[str, dict[str, str]] = {}
    for session_id, meta in raw_scenarios.items():
        if not isinstance(meta, dict):
            continue
        item: dict[str, str] = {}
        level = str(meta.get("level", "normal"))
        if level in SCENARIO_LEVELS:
            item["level"] = level
        title = str(meta.get("title", "")).strip()
        title_cn = str(meta.get("title_cn", "")).strip()
        maintenance_time = str(meta.get("maintenance_time", "")).strip()
        if title:
            item["title"] = title
        if title_cn:
            item["title_cn"] = title_cn
        if maintenance_time:
            item["maintenance_time"] = maintenance_time
        if item:
            normalized[str(session_id)] = item
    return normalized


def _save_scenario_meta_data(meta: dict[str, dict[str, str]]) -> None:
    scenarios: dict[str, dict[str, str]] = {}
    for session_id, values in sorted(meta.items(), key=lambda item: item[0]):
        clean: dict[str, str] = {}
        level = values.get("level", "normal")
        if level in SCENARIO_LEVELS and level != "normal":
            clean["level"] = level
        title = str(values.get("title", "")).strip()
        title_cn = str(values.get("title_cn", "")).strip()
        maintenance_time = str(values.get("maintenance_time", "")).strip()
        if title:
            clean["title"] = title
        if title_cn:
            clean["title_cn"] = title_cn
        if maintenance_time:
            clean["maintenance_time"] = maintenance_time
        if clean:
            scenarios[session_id] = clean
    payload = {"scenarios": scenarios}
    tmp_path = SCENARIO_META_FILE.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(SCENARIO_META_FILE)


SCENARIO_META_DATA = _load_scenario_meta_data()


def _scenario_meta_for(session_id: object) -> dict[str, str]:
    return SCENARIO_META_DATA.get(str(session_id), {})


def _load_scenario_level_data() -> dict[str, str]:
    if SCENARIO_META_DATA:
        return {
            session_id: meta["level"]
            for session_id, meta in SCENARIO_META_DATA.items()
            if meta.get("level") in SCENARIO_LEVELS
        }
    if not SCENARIO_LEVEL_FILE.exists():
        return {}
    try:
        payload = json.loads(SCENARIO_LEVEL_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    raw_levels = payload.get("levels", payload) if isinstance(payload, dict) else {}
    if not isinstance(raw_levels, dict):
        return {}
    return {
        str(session_id): str(level)
        for session_id, level in raw_levels.items()
        if str(level) in SCENARIO_LEVELS
    }


def _save_scenario_level_data(levels: dict[str, str]) -> None:
    for session_id, level in levels.items():
        meta = SCENARIO_META_DATA.setdefault(session_id, {})
        meta["level"] = level
    for session_id in list(SCENARIO_META_DATA):
        if session_id not in levels and SCENARIO_META_DATA[session_id].get("level"):
            SCENARIO_META_DATA[session_id].pop("level", None)
        if not SCENARIO_META_DATA.get(session_id):
            SCENARIO_META_DATA.pop(session_id, None)
    _save_scenario_meta_data(SCENARIO_META_DATA)


SCENARIO_LEVEL_DATA = _load_scenario_level_data()


def _scenario_level_for(session_id: object) -> str:
    level = SCENARIO_LEVEL_DATA.get(str(session_id), "normal")
    return level if level in SCENARIO_LEVELS else "normal"


def _safe_log_values(values: dict[str, object]) -> dict[str, str]:
    clean: dict[str, str] = {}
    for key, value in values.items():
        if key.lower() in SENSITIVE_LOG_KEYS:
            clean[key] = "***"
        else:
            clean[key] = str(value)
    return clean


def _is_placeholder_value(value: object) -> bool:
    return value is None or str(value).strip() in {"", "0", "null", "None"}


def _form_values_from_hex(hex_text: str) -> dict[str, str]:
    try:
        raw = bytes(int(part, 16) for part in hex_text.split())
    except ValueError:
        return {}
    _, separator, body = raw.partition(b"\r\n\r\n")
    if not separator:
        return {}
    try:
        query = body.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        return {}
    return {key: values[-1] if values else "" for key, values in parse_qs(query, keep_blank_values=True).items()}


def _latest_upstream_identity() -> dict[str, str]:
    try:
        stat = FRIDA_CAPTURE_LOG.stat()
    except OSError:
        return {}
    cached_mtime = float(UPSTREAM_IDENTITY_CACHE.get("mtime") or 0)
    if stat.st_mtime == cached_mtime:
        cached = UPSTREAM_IDENTITY_CACHE.get("identity")
        return dict(cached) if isinstance(cached, dict) else {}
    identity: dict[str, str] = {}
    try:
        lines = FRIDA_CAPTURE_LOG.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        lines = []
    for line in reversed(lines[-5000:]):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = item.get("payload") if isinstance(item, dict) else {}
        if not isinstance(payload, dict) or payload.get("direction") != "ssl_write":
            continue
        values = _form_values_from_hex(str(payload.get("hex") or ""))
        token = str(values.get("Token") or "").strip()
        user_id = str(values.get("UserID") or "").strip()
        device_id = str(values.get("DeviceID") or "").strip()
        if token and user_id and not _is_placeholder_value(token) and not _is_placeholder_value(user_id):
            identity = {"Token": token, "UserID": user_id}
            if device_id and not _is_placeholder_value(device_id):
                identity["DeviceID"] = device_id
            break
    UPSTREAM_IDENTITY_CACHE["mtime"] = stat.st_mtime
    UPSTREAM_IDENTITY_CACHE["identity"] = identity
    return dict(identity)


def _append_call_log(record: dict[str, object]) -> None:
    try:
        with CALL_LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    except OSError:
        return


def _load_call_logs(limit: int = 200) -> list[dict[str, object]]:
    if not CALL_LOG_FILE.exists():
        return []
    try:
        lines = CALL_LOG_FILE.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    records: list[dict[str, object]] = []
    for line in reversed(lines[-MAX_CALL_LOGS:]):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            records.append(item)
        if len(records) >= limit:
            break
    return records


def _interface_added_time_for(spec: dict[str, object]) -> str:
    return str(
        spec.get("added_time")
        or spec.get("created_at")
        or spec.get("capture_time")
        or DEFAULT_INTERFACE_ADDED_TIME
    ).strip()


def _maintenance_time_for(spec: dict[str, object]) -> str:
    session_id = str(spec.get("session_id") or "")
    return _scenario_meta_for(session_id).get("maintenance_time", "") or _interface_added_time_for(spec)


TITLE_CN_BY_SESSION = {
    "1": "应用资讯",
    "2": "题材个股关联",
    "4": "用户登录埋点",
    "7": "用户消息",
    "10": "广告配置",
    "14": "现货列表",
    "15": "最新评论用户",
    "19": "自选股状态更新",
    "23": "原始行情请求",
    "52": "首页指数信息",
    "53": "应用布局配置",
    "54": "首页新列表",
    "56": "指数板块列表",
    "108": "日K线",
    "111": "当日K线",
    "112": "首页盯盘模块",
    "119": "功能使用记录",
    "120": "全部自选股",
    "121": "L2日期显示控制",
    "122": "龙虎榜标题",
    "123": "龙虎榜东财状态",
    "126": "龙虎榜股票列表",
    "128": "龙虎榜添加",
    "146": "股票图表",
    "147": "个股最新信息",
    "159": "评论列表",
    "193": "个股最新信息",
    "194": "用户点击统计",
    "196": "股票走势",
    "197": "用户点击统计",
    "199": "营业部趋势",
    "200": "模块开关",
    "209": "批量点击统计",
    "210": "用户日志上报",
    "211": "营业部趋势",
    "213": "最新交易日",
    "214": "龙虎榜更新列表",
    "215": "股票留言栏信息",
    "216": "涨停基因",
    "217": "股票所属板块",
    "218": "文章标题",
    "265": "用户页面统计",
    "267": "用户日志上报",
    "272": "论坛栏目列表",
    "273": "焦点消息",
    "274": "焦点消息",
    "277": "精选消息列表",
    "278": "客户端广告",
    "287": "论坛栏目详情",
    "298": "首页信息",
    "310": "功能说明",
    "311": "新股指数变化",
    "312": "ETF排行",
    "313": "指数K线",
    "319": "功能说明",
    "325": "用户点击统计",
    "326": "主力持仓列表",
    "329": "主力持仓列表",
    "335": "用户点击统计",
    "336": "功能说明",
    "337": "文章标题",
    "342": "用户点击统计",
    "343": "题材库功能说明",
    "352": "用户页面统计",
    "354": "用户日志上报",
    "374": "十日换手率",
    "375": "委托盘口",
    "383": "用户日志上报",
    "387": "用户页面统计",
    "407": "指数走势",
    "413": "异动看盘实时数据",
    "414": "用户权限",
    "415": "异动看盘说明",
    "418": "F10基础首页",
    "419": "重要提醒",
    "420": "历史涨停复盘",
    "421": "涨停K线",
    "422": "公司公告列表",
    "423": "公司研报列表",
    "424": "研报字段导出",
    "425": "研报字段列表",
    "426": "机构持仓日期",
    "427": "机构持仓明细",
    "428": "基金持仓",
    "429": "风口标签列表",
    "430": "个股风口",
    "432": "个股风口",
    "446": "用户日志上报",
    "1015": "行情首页信息",
    "1019": "行情首页信息",
    "1021": "行情首页信息",
    "1031": "指数量额增量",
    "1032": "指数走势增量",
    "1033": "父级板块代码",
    "1034": "板块区间信息",
    "1035": "板块文章标题",
    "1036": "子板块信息",
    "1037": "股票池标签",
    "1040": "板块分时直播",
    "1880": "游资动向列表",
    '18001': '?????? P19',
    '18003': '市场风口????',
    '18012': '???????',
    '18013': '??????',
    '18019': '????????',
    '18021': '??????',
    '18026': '????????',
    '18054': '?????? P41',
    '18055': '上证指数????',
    '18059': '??????',
    '18061': '?????',
    '18062': '?????',
    '18063': '??????',
    '18065': '??????',
    '18071': '??????',
    '18080': '?????? P85',
    '18083': '主题机会????',
    '18090': '?????? P140',
    '18091': '?????? P176',
    '18092': '????????',
    '18124': '?????? P301',
    '18125': '?????? P143',
    '18126': '????????',
    '18127': '?????? P177',
    '18128': '????????',
    '18139': '?????? P40',
    '18157': '?????????',
    '18162': '????????',
    '18181': '严重异动提醒????',
    '18182': '??????',
    '18190': '?????? P174',
    '18191': '????',
    '18207': '?????? P507',
    "18208": "情绪-变化统计",
    "18209": "情绪-市场连板K线",
    "18210": "情绪-市场量能基准线",
    "18211": "情绪-市场容量K线",
    "18212": "情绪-涨停表现说明",
    "18213": "情绪-涨停指数",
    "18214": "情绪-涨跌家数",
    "18215": "情绪-现货列表",
    "18216": "情绪-急跌列表",
    "18217": "情绪-权重表现列表",
    "18218": "大幅回撤-查询历史",
    "18219": "涨停表现-历史指数",
    "18220": "涨停表现-历史列表",
    "18221": "涨停表现-历史连板列表",
    "18222": "涨停表现-历史打板列表",
    "18223": "涨停表现-历史走势增量",
    "18224": "涨停表现-历史量额增量",
    "18225": "市场量能-大单历史K线",
    "18226": "市场量能-指数历史K线",
    "18227": "市场量能-大单当日K线",
    "18228": "市场量能-指数当日K线",
    "18229": "市场量能-个股区间访谈历史",
    "18230": "市场量能-个股区间访谈实时",
    "18231": "市场量能-指数区间访谈历史",
    "18232": "市场量能-历史量能",
    "18233": "市场情绪-最新主题提醒",
    "18234": "市场情绪-最新主题阅读计数",
    "18235": "风向标-父级板块代码",
    "18236": "风向标-实时量额增量",
    "18237": "风向标-实时走势增量",
    "18238": "风向标-文章标题",
    "18239": "风向标-历史走势增量",
    "18240": "风向标-历史板块行情",
    "18241": "风向标-历史量额增量",
    "18242": "风向标-历史子板块",
    "18243": "风向标-历史题材标签",
    "18244": "风向标-历史分时直播",
    "18245": "风向标-历史股票列表",
    "18246": "风向标-强势题材股票列表",
    "18247": "风向标-高强题材股票列表",
    "18248": "风向标-活跃题材股票列表",
    "18249": "龙虎榜-今日上榜股票列表",
    "18250": "龙虎榜-今日上榜营业部列表",
    "18251": "龙虎榜-营业部K线",
    "18252": "龙虎榜-营业部买卖列表",
    "18253": "龙虎榜-营业部区间统计",
    "18254": "龙虎榜-游资组合信息",
    "18255": "龙虎榜-游资组合流水",
    "18256": "龙虎榜-营业部基础列表",
    "18257": "龙虎榜-游资组合股票图表",
    "18258": "龙虎榜-游资日期列表",
    "18285": "行情-历史指数窄幅走势",
    "18286": "行情-历史排名信息",
    "18287": "行情-历史题材指数排名",
    "18288": "行情-历史行业指数排名",
    "18289": "行情-历史地域指数排名",
    "18290": "行情-历史行业指数时间段排名",
    "18291": "行情-历史地域指数时间段排名",
    "18259": "龙虎榜-游资组合信息-成都系",
    "18272": "龙虎榜-游资组合流水-成都系",
    "18260": "龙虎榜-游资组合信息-佛山系",
    "18273": "龙虎榜-游资组合流水-佛山系",
    "18261": "龙虎榜-游资组合信息-炒股养家",
    "18274": "龙虎榜-游资组合流水-炒股养家",
    "18262": "龙虎榜-游资组合信息-赵老哥",
    "18275": "龙虎榜-游资组合流水-赵老哥",
    "18263": "龙虎榜-游资组合信息-小鳄鱼",
    "18276": "龙虎榜-游资组合流水-小鳄鱼",
    "18264": "龙虎榜-游资组合信息-作手新一",
    "18277": "龙虎榜-游资组合流水-作手新一",
    "18265": "龙虎榜-游资组合信息-章盟主",
    "18278": "龙虎榜-游资组合流水-章盟主",
    "18266": "龙虎榜-游资组合信息-量化基金",
    "18279": "龙虎榜-游资组合流水-量化基金",
    "18267": "龙虎榜-游资组合信息-上塘路",
    "18280": "龙虎榜-游资组合流水-上塘路",
    "18268": "龙虎榜-游资组合信息-北京光华路",
    "18281": "龙虎榜-游资组合流水-北京光华路",
    "18269": "龙虎榜-游资组合信息-思明南路",
    "18282": "龙虎榜-游资组合流水-思明南路",
    "18270": "龙虎榜-游资组合信息-南京帮",
    "18283": "龙虎榜-游资组合流水-南京帮",
    "18271": "龙虎榜-游资组合信息-机构",
    "18284": "龙虎榜-游资组合流水-机构",
}


def _title_cn_for(spec: dict[str, object], controller: object, action: object) -> str:
    session_id = str(spec.get("session_id") or "")
    meta_title = _scenario_meta_for(session_id).get("title_cn", "")
    if meta_title:
        return meta_title
    spec_title = str(spec.get("title_cn", "")).strip()
    if spec_title:
        return spec_title
    if session_id in TITLE_CN_BY_SESSION:
        return TITLE_CN_BY_SESSION[session_id]
    return f"{controller}.{action}"


def _title_for(spec: dict[str, object], controller: object, action: object) -> str:
    session_id = str(spec.get("session_id") or "")
    meta_title = _scenario_meta_for(session_id).get("title", "")
    if meta_title:
        return meta_title
    return f"{controller}.{action}"


def _build_scenarios() -> list[dict[str, object]]:
    scenarios: list[dict[str, object]] = []
    used_method_names: dict[str, int] = {}
    for spec in REQUESTS:
        params = spec.get("params") or {}
        data = spec.get("data") or {}
        controller = data.get("c") or params.get("c") or "request"
        action = data.get("a") or params.get("a") or spec["session_id"]
        base_method_name = f"{_safe_route_part(controller)}_{_safe_route_part(action)}"
        duplicate_index = used_method_names.get(base_method_name, 0)
        used_method_names[base_method_name] = duplicate_index + 1
        method_name = (
            base_method_name
            if duplicate_index == 0
            else f"{base_method_name}_{_safe_route_part(str(spec['session_id']))}"
        )
        endpoint = f"/api/{method_name}"
        base_alias_endpoint = f"/api/{_safe_route_part(controller)}/{_safe_route_part(action)}"
        alias_endpoint = (
            base_alias_endpoint
            if duplicate_index == 0
            else f"{base_alias_endpoint}/{_safe_route_part(str(spec['session_id']))}"
        )
        scenarios.append(
            {
                "session_id": spec["session_id"],
                "title": _title_for(spec, controller, action),
                "title_cn": _title_cn_for(spec, controller, action),
                "added_time": _interface_added_time_for(spec),
                "maintenance_time": _maintenance_time_for(spec),
                "level": _scenario_level_for(spec["session_id"]),
                "level_label": SCENARIO_LEVELS[_scenario_level_for(spec["session_id"])],
                "method_name": method_name,
                "http_method": spec["method"],
                "target_url": spec["url"],
                "endpoint": endpoint,
                "alias_endpoint": alias_endpoint,
                "params": params,
                "data": data,
                "hide_url_fields": spec.get("hide_url_fields", []),
            }
        )
    for name, (host, controller, action) in CORE_API_KEYS.items():
        if name not in CORE_LOCAL_API_KEYS:
            continue
        session_id = f"core:{name}"
        defaults = CORE_LOCAL_TITLES.get(name, {})
        core_meta = _scenario_meta_for(session_id)
        method_name = str(defaults.get("method_name") or name)
        title = core_meta.get("title", f"{controller}.{action}")
        title_cn = core_meta.get("title_cn", str(defaults.get("title_cn") or f"{controller}.{action}"))
        maintenance_time = core_meta.get("maintenance_time", CORE_LOCAL_ADDED_TIME)
        added_time = CORE_LOCAL_ADDED_TIME
        level = _scenario_level_for(session_id)
        scenarios.append(
            {
                "session_id": session_id,
                "title": title,
                "title_cn": title_cn,
                "added_time": added_time,
                "maintenance_time": maintenance_time,
                "level": level,
                "level_label": SCENARIO_LEVELS[level],
                "method_name": method_name,
                "http_method": "GET",
                "target_url": str(HQSTOCK_LOG),
                "endpoint": f"/api/{method_name}",
                "alias_endpoint": f"/api/core/{name}",
                "params": dict(defaults.get("params") or {"StockID": "000620"}),
                "data": {},
                "host": host,
                "core_name": name,
                "is_core": True,
                "hide_url_fields": [],
            }
        )
    return scenarios


SCENARIOS = _build_scenarios()
ROUTES: dict[str, dict[str, object]] = {}


def _refresh_routes() -> None:
    global SCENARIOS, ROUTES
    SCENARIOS = _build_scenarios()
    ROUTES = {}
    for scenario, spec in zip(SCENARIOS, REQUESTS):
        ROUTES[scenario["endpoint"]] = {"scenario": scenario, "spec": spec}
        ROUTES[scenario["alias_endpoint"]] = {"scenario": scenario, "spec": spec}
    for scenario in SCENARIOS[len(REQUESTS) :]:
        if not scenario.get("is_core"):
            continue
        ROUTES[scenario["endpoint"]] = {"scenario": scenario, "core_name": scenario.get("core_name")}
        ROUTES[scenario["alias_endpoint"]] = {"scenario": scenario, "core_name": scenario.get("core_name")}


_refresh_routes()


class ScenarioApiHandler(BaseHTTPRequestHandler):
    server_version = "KaipanlaScenarioAPI/1.0"

    def do_GET(self) -> None:
        self._handle_request()

    def do_POST(self) -> None:
        self._handle_request()

    def do_PATCH(self) -> None:
        self._handle_request()

    def do_DELETE(self) -> None:
        self._handle_request()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        print("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format % args))

    def _handle_request(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path.rstrip("/") or "/")

        if path in {f"/{LOGIN_FILE}", "/login"}:
            self._serve_file(ROOT / LOGIN_FILE, "text/html; charset=utf-8")
            return

        if path in {f"/{REGISTER_FILE}", "/register"}:
            self._serve_file(ROOT / REGISTER_FILE, "text/html; charset=utf-8")
            return

        if path in {f"/{EXPIRED_FILE}", "/expired"}:
            self._serve_file(ROOT / EXPIRED_FILE, "text/html; charset=utf-8")
            return

        if path.startswith("/api/auth/"):
            self._handle_auth_api(path)
            return

        if path.startswith("/api/admin/"):
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            if user.get("role") != "admin":
                self._send_json({"error": "forbidden", "message": "Admin role required"}, status=403)
                return
            self._handle_admin_api(path)
            return

        if path in {"/", "/index.html", f"/{PAGE_FILE}", f"/{ADMIN_FILE}", "/admin"}:
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=False)
                return
            if path in {f"/{ADMIN_FILE}", "/admin"} and user.get("role") != "admin":
                self._send_json({"error": "forbidden", "message": "Admin role required"}, status=403)
                return
            page = ADMIN_FILE if path in {f"/{ADMIN_FILE}", "/admin"} else PAGE_FILE
            self._serve_file(ROOT / page, "text/html; charset=utf-8")
            return

        if path == f"/{CLIENT_FILE}":
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            if user.get("role") != "admin":
                self._send_json({"error": "forbidden", "message": "Admin role required"}, status=403)
                return
            self._serve_file(ROOT / CLIENT_FILE, "text/plain; charset=utf-8")
            return

        if path == "/api/scenarios":
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._send_json(
                {
                    "count": len(SCENARIOS),
                    "scenarios": SCENARIOS,
                    "level_options": [
                        {"value": value, "label": label}
                        for value, label in SCENARIO_LEVELS.items()
                    ],
                    "user": user,
                }
            )
            return

        if path.startswith("/api/topic-library"):
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_topic_library_api(path)
            return

        if path == "/api/core" or path.startswith("/api/core/"):
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_core_api(user, path)
            return

        if path == "/api/hq" or path.startswith("/api/hq/"):
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_hq_api(user, path)
            return

        if path in ROUTES:
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            if self.command not in {"GET", "POST"}:
                self._send_json({"error": "method_not_allowed"}, status=405)
                return
            route = ROUTES[path]
            query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
            body_values = self._read_body_values()
            overrides = {**query_values, **body_values}
            overrides.pop("_ts", None)
            if route.get("core_name"):
                self._call_core_scene(user, route["scenario"], str(route["core_name"]), overrides)
                return
            self._call_scene(user, route["scenario"], route["spec"], overrides)
            return

        self._send_json({"error": "not_found", "path": path}, status=404)

    def _call_scene(self, user: dict[str, object], scenario: dict[str, object], spec: dict[str, object], overrides: dict[str, str]) -> None:
        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        client = KaipanlaCapturedClient()
        client.session.trust_env = False
        data = dict(spec.get("data") or {})
        params = dict(spec.get("params") or {})
        captured_identity = _latest_upstream_identity()
        upstream_user_id = os.environ.get("KPL_UPSTREAM_USER_ID") or captured_identity.get("UserID")
        upstream_token = os.environ.get("KPL_UPSTREAM_TOKEN") or captured_identity.get("Token")
        upstream_device_id = os.environ.get("KPL_UPSTREAM_DEVICE_ID") or captured_identity.get("DeviceID")

        for key, value in overrides.items():
            if key in params and key not in data:
                params[key] = value
            else:
                data[key] = value
        if upstream_user_id and _is_placeholder_value(data.get("UserID")):
            data["UserID"] = upstream_user_id
        if upstream_token and _is_placeholder_value(data.get("Token")):
            data["Token"] = upstream_token
        if upstream_device_id and _is_placeholder_value(data.get("DeviceID")):
            data["DeviceID"] = upstream_device_id
        params["_ts"] = str(int(requested_at * 1000))

        try:
            response = client.request(spec, data=data, params=params)
        except Exception as exc:
            _append_call_log(
                {
                    "requested_at": requested_at,
                    "requested_at_text": started_iso,
                    "username": user.get("username", ""),
                    "role": user.get("role", ""),
                    "session_id": scenario.get("session_id", ""),
                    "title": scenario.get("title", ""),
                    "title_cn": scenario.get("title_cn", ""),
                    "endpoint": scenario.get("endpoint", ""),
                    "target_url": scenario.get("target_url", spec.get("url", "")),
                    "http_method": scenario.get("http_method", spec.get("method", "")),
                    "status": "failed",
                    "status_code": 502,
                    "duration_ms": int((time.time() - requested_at) * 1000),
                    "overrides": _safe_log_values(overrides),
                    "error": str(exc),
                }
            )
            self._send_json(
                {
                    "error": "upstream_request_failed",
                    "message": str(exc),
                    "scenario": scenario,
                    "overrides": overrides,
                },
                status=502,
            )
            return

        content_type = response.headers.get("Content-Type", "")
        payload: object
        try:
            payload = response.json()
        except ValueError:
            payload = response.text

        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": scenario.get("session_id", ""),
                "title": scenario.get("title", ""),
                "title_cn": scenario.get("title_cn", ""),
                "endpoint": scenario.get("endpoint", ""),
                "target_url": scenario.get("target_url", spec.get("url", "")),
                "http_method": scenario.get("http_method", spec.get("method", "")),
                "status": "ok" if response.ok else "upstream_error",
                "status_code": response.status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "content_type": content_type,
                "overrides": _safe_log_values(overrides),
            }
        )

        self._send_json(
            {
                "requested_at": requested_at,
                "status_code": response.status_code,
                "content_type": content_type,
                "upstream_url": response.url,
                "body": payload,
            }
        )

    def _handle_auth_api(self, path: str) -> None:
        if path == "/api/auth/login" and self.command == "POST":
            payload = self._read_json_body()
            token, user, error = AUTH.login(
                str(payload.get("username", "")).strip(),
                str(payload.get("password", "")),
            )
            if error:
                status = 403 if error in {"disabled", "expired"} else 401
                headers = [self._make_session_cookie(token)] if token else None
                self._send_json({"error": error, "message": error, "user": user}, status=status, extra_headers=headers)
                return
            self._send_json({"user": user}, extra_headers=[self._make_session_cookie(token)])
            return

        if path == "/api/auth/register" and self.command == "POST":
            payload = self._read_json_body()
            password = str(payload.get("password", ""))
            confirm_password = str(payload.get("confirm_password", password))
            if password != confirm_password:
                self._send_json({"error": "invalid_request", "message": "passwords do not match"}, status=400)
                return
            try:
                user = AUTH.register_trial_user(payload)
                token, user, error = AUTH.login(str(payload.get("username", "")).strip(), password)
            except ValueError as exc:
                self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                return
            if error:
                status = 201 if error == "expired" else 403
                self._send_json(
                    {"error": error, "message": error, "user": user},
                    status=status,
                    extra_headers=[self._make_session_cookie(token)] if token else None,
                )
                return
            self._send_json({"user": user}, status=201, extra_headers=[self._make_session_cookie(token)])
            return

        if path == "/api/auth/redeem" and self.command == "POST":
            user, error = AUTH.session_identity(self._session_token())
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            payload = self._read_json_body()
            try:
                result = AUTH.redeem_activation_code(str(user["username"]), str(payload.get("code", "")))
            except (KeyError, ValueError) as exc:
                self._send_json({"error": "invalid_activation_code", "message": str(exc)}, status=400)
                return
            self._send_json(result)
            return

        if path == "/api/auth/logout" and self.command in {"GET", "POST"}:
            AUTH.logout(self._session_token())
            self._send_json({"ok": True}, extra_headers=[self._clear_session_cookie()])
            return

        if path == "/api/auth/me" and self.command == "GET":
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._send_json({"user": user})
            return

        self._send_json({"error": "not_found", "path": path}, status=404)

    def _handle_admin_api(self, path: str) -> None:
        if path == "/api/admin/call-logs" and self.command == "GET":
            parsed = urlparse(self.path)
            query = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
            try:
                limit = max(1, min(1000, int(query.get("limit", "200"))))
            except ValueError:
                limit = 200
            username = query.get("username", "").strip().lower()
            session_id = query.get("session_id", "").strip()
            keyword = query.get("q", "").strip().lower()
            logs = _load_call_logs(limit=1000)
            filtered: list[dict[str, object]] = []
            for item in logs:
                if username and username not in str(item.get("username", "")).lower():
                    continue
                if session_id and session_id != str(item.get("session_id", "")):
                    continue
                if keyword:
                    haystack = " ".join(
                        str(item.get(key, ""))
                        for key in ("username", "session_id", "title", "title_cn", "endpoint", "status", "status_code")
                    ).lower()
                    if keyword not in haystack:
                        continue
                filtered.append(item)
                if len(filtered) >= limit:
                    break
            self._send_json({"logs": filtered, "count": len(filtered)})
            return

        if path in {"/api/admin/scenario-levels", "/api/admin/scenario-meta"} and self.command == "GET":
            self._send_json(
                {
                    "level_options": [
                        {"value": value, "label": label}
                        for value, label in SCENARIO_LEVELS.items()
                    ],
                    "scenarios": [
                        {
                            "session_id": scenario["session_id"],
                            "title": scenario["title"],
                            "title_cn": scenario.get("title_cn", ""),
                            "added_time": scenario.get("added_time", ""),
                            "maintenance_time": scenario.get("maintenance_time", ""),
                            "level": scenario.get("level", "normal"),
                            "level_label": scenario.get("level_label", SCENARIO_LEVELS["normal"]),
                            "endpoint": scenario["endpoint"],
                            "target_url": scenario["target_url"],
                        }
                        for scenario in SCENARIOS
                    ],
                }
            )
            return

        level_prefix = "/api/admin/scenario-levels/"
        meta_prefix = "/api/admin/scenario-meta/"
        if (
            (path.startswith(level_prefix) or path.startswith(meta_prefix))
            and self.command == "PATCH"
        ):
            prefix = level_prefix if path.startswith(level_prefix) else meta_prefix
            session_id = unquote(path[len(prefix) :])
            if not any(str(scenario["session_id"]) == session_id for scenario in SCENARIOS):
                self._send_json({"error": "not_found", "message": "scenario not found"}, status=404)
                return
            payload = self._read_json_body()
            current = next(item for item in SCENARIOS if str(item["session_id"]) == session_id)
            level = str(payload.get("level", current.get("level", "normal")))
            if level not in SCENARIO_LEVELS:
                self._send_json(
                    {
                        "error": "invalid_level",
                        "message": f"level must be one of: {', '.join(SCENARIO_LEVELS)}",
                    },
                    status=400,
                )
                return
            title = str(payload.get("title", current.get("title", ""))).strip()
            title_cn = str(payload.get("title_cn", current.get("title_cn", ""))).strip()
            maintenance_time = str(
                payload.get("maintenance_time", current.get("maintenance_time", ""))
            ).strip()
            if not title:
                self._send_json({"error": "invalid_title", "message": "English title cannot be empty"}, status=400)
                return
            if not title_cn:
                self._send_json({"error": "invalid_title_cn", "message": "Chinese title cannot be empty"}, status=400)
                return
            meta = SCENARIO_META_DATA.setdefault(session_id, {})
            if level == "normal":
                meta.pop("level", None)
                SCENARIO_LEVEL_DATA.pop(session_id, None)
            else:
                meta["level"] = level
                SCENARIO_LEVEL_DATA[session_id] = level
            spec = next((item for item in REQUESTS if str(item.get("session_id")) == session_id), None)
            if spec is None:
                core_name = session_id.split(":", 1)[1] if session_id.startswith("core:") else ""
                if core_name in CORE_API_KEYS:
                    _, default_controller, default_action = CORE_API_KEYS[core_name]
                    default_maintenance_time = CORE_LOCAL_ADDED_TIME
                    default_title = f"{default_controller}.{default_action}"
                    default_title_cn = str(CORE_LOCAL_TITLES.get(core_name, {}).get("title_cn", ""))
                else:
                    default_maintenance_time = str(current.get("added_time") or CORE_LOCAL_ADDED_TIME)
                    default_title = str(current.get("title") or "")
                    default_title_cn = str(current.get("title_cn") or "")
            else:
                spec_params = spec.get("params") or {}
                spec_data = spec.get("data") or {}
                default_maintenance_time = _interface_added_time_for(spec)
                default_controller = spec_data.get("c") or spec_params.get("c") or "request"
                default_action = spec_data.get("a") or spec_params.get("a") or spec.get("session_id")
                default_title = f"{default_controller}.{default_action}"
                default_title_cn = str(spec.get("title_cn") or TITLE_CN_BY_SESSION.get(session_id, ""))
            if title == default_title:
                meta.pop("title", None)
            else:
                meta["title"] = title
            if title_cn == default_title_cn:
                meta.pop("title_cn", None)
            else:
                meta["title_cn"] = title_cn
            if maintenance_time and maintenance_time != default_maintenance_time:
                meta["maintenance_time"] = maintenance_time
            else:
                meta.pop("maintenance_time", None)
            if not meta:
                SCENARIO_META_DATA.pop(session_id, None)
            _save_scenario_meta_data(SCENARIO_META_DATA)
            _refresh_routes()
            scenario = next(item for item in SCENARIOS if str(item["session_id"]) == session_id)
            self._send_json({"scenario": scenario})
            return

        if path == "/api/admin/users" and self.command == "GET":
            self._send_json({"users": AUTH.list_users()})
            return

        if path == "/api/admin/users" and self.command == "POST":
            try:
                user = AUTH.create_user(self._read_json_body())
            except ValueError as exc:
                self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                return
            self._send_json({"user": user}, status=201)
            return

        prefix = "/api/admin/users/"
        if path.startswith(prefix):
            username = unquote(path[len(prefix) :])
            if self.command == "PATCH":
                try:
                    user = AUTH.update_user(username, self._read_json_body())
                except KeyError as exc:
                    self._send_json({"error": "not_found", "message": str(exc)}, status=404)
                    return
                except ValueError as exc:
                    self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                    return
                self._send_json({"user": user})
                return
            if self.command == "DELETE":
                try:
                    AUTH.delete_user(username)
                except KeyError as exc:
                    self._send_json({"error": "not_found", "message": str(exc)}, status=404)
                    return
                except ValueError as exc:
                    self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                    return
                self._send_json({"ok": True})
                return

        if path == "/api/admin/activation-codes" and self.command == "GET":
            self._send_json({"codes": AUTH.list_activation_codes()})
            return

        if path == "/api/admin/activation-codes" and self.command == "POST":
            try:
                codes = AUTH.create_activation_codes(self._read_json_body())
            except ValueError as exc:
                self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                return
            self._send_json({"codes": codes}, status=201)
            return

        code_prefix = "/api/admin/activation-codes/"
        if path.startswith(code_prefix):
            code_id = unquote(path[len(code_prefix) :])
            if self.command == "PATCH":
                try:
                    code = AUTH.update_activation_code(code_id, self._read_json_body())
                except KeyError as exc:
                    self._send_json({"error": "not_found", "message": str(exc)}, status=404)
                    return
                self._send_json({"code": code})
                return
            if self.command == "DELETE":
                try:
                    AUTH.delete_activation_code(code_id)
                except KeyError as exc:
                    self._send_json({"error": "not_found", "message": str(exc)}, status=404)
                    return
                except ValueError as exc:
                    self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                    return
                self._send_json({"ok": True})
                return

        self._send_json({"error": "not_found", "path": path}, status=404)

    def _handle_topic_library_api(self, path: str) -> None:
        latest_path = ROOT / "topic_library" / "topic_library_latest.json"
        if path == "/api/topic-library/latest" and self.command == "GET":
            if not latest_path.exists():
                self._send_json({"exists": False, "message": "No topic-library crawl result yet."}, status=404)
                return
            try:
                payload = json.loads(latest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                self._send_json({"error": "invalid_latest_file", "message": str(exc)}, status=500)
                return
            self._send_json({"exists": True, "result": payload})
            return

        if path == "/api/topic-library/crawl" and self.command == "POST":
            if crawl_topic_library is None or write_outputs is None:
                self._send_json(
                    {
                        "error": "topic_library_tool_missing",
                        "message": "tools/crawl_topic_library.py is not available in this workspace.",
                    },
                    status=501,
                )
                return
            body = self._read_json_body()
            args = argparse.Namespace(
                func_name=str(body.get("func_name") or "题材库"),
                out_dir=str(ROOT / "topic_library"),
                param0=str(body.get("param0") or "507"),
                param1=str(body.get("param1") or "1"),
                skip_click=bool(body.get("skip_click", False)),
                allow_anonymous=bool(body.get("allow_anonymous", False)),
                timeout=float(body.get("timeout") or 15),
                min_interval=float(body.get("min_interval") or 1.2),
                jitter=float(body.get("jitter") or 0.8),
            )
            try:
                payload = crawl_topic_library(args)
                output_path = write_outputs(payload, Path(args.out_dir))
            except SystemExit as exc:
                self._send_json({"error": "missing_credentials", "message": str(exc)}, status=400)
                return
            except Exception as exc:
                self._send_json({"error": "topic_library_crawl_failed", "message": str(exc)}, status=502)
                return
            self._send_json({"ok": True, "output": str(output_path), "result": payload})
            return

        self._send_json({"error": "not_found", "path": path}, status=404)

    def _handle_hq_api(self, user: dict[str, object], path: str) -> None:
        if self.command not in {"GET", "POST"}:
            self._send_json({"error": "method_not_allowed"}, status=405)
            return
        if path == "/api/hq":
            self._send_json(
                {
                    "apis": [
                        {
                            "name": name,
                            "source": meta["source"],
                            "packet_code": meta["packet_code"],
                            "endpoint": meta["endpoint"],
                            "description": meta["description"],
                        }
                        for name, meta in HQ_API_KEYS.items()
                    ],
                    "log": str(HQSTOCK_LOG),
                }
            )
            return
        name = path[len("/api/hq/") :].strip("/")
        if name == "five-level":
            name = "five_level"
        if name not in HQ_API_KEYS:
            self._send_json({"error": "not_found", "message": f"unknown hq api: {name}"}, status=404)
            return
        parsed = urlparse(self.path)
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values()
        values = {**query_values, **body_values}
        default_code = "2015" if name == "five_level" else "2006"
        stock_id = normalize_stock_id(
            str(
                values.get("StockID")
                or values.get("stock_id")
                or values.get("stock")
                or latest_stock_for_code(default_code)
            )
        )
        if not stock_id:
            self._send_json({"error": "missing_stock_id", "message": "Pass StockID=688008"}, status=400)
            return

        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        if name == "five_level":
            result = latest_five_level(stock_id)
            packet_code = "2015"
            not_found_message = f"no hqStock 2015 five-level packet found for {stock_id}"
        else:
            try:
                limit = max(1, min(1000, int(values.get("limit", "100"))))
            except ValueError:
                limit = 100
            result = latest_time_sales(stock_id, limit=limit)
            packet_code = "2006"
            not_found_message = f"no hqStock 2006 time-sales packet found for {stock_id}"
        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": f"hq:{name}",
                "title": f"hqStock.{packet_code}",
                "title_cn": "五档行情",
                "endpoint": f"/api/hq/{name}",
                "target_url": str(HQSTOCK_LOG),
                "http_method": self.command,
                "status": "ok" if result else "not_found",
                "status_code": 200 if result else 404,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(values),
            }
        )
        if not result:
            self._send_json(
                {
                    "error": "not_found",
                    "message": not_found_message,
                    "stock": stock_id,
                    "log": str(HQSTOCK_LOG),
                    "hint": "Start Frida capture and open the stock quote page before calling this API.",
                },
                status=404,
            )
            return
        self._send_json({"requested_at": requested_at, "body": result})

    def _call_core_scene(
        self,
        user: dict[str, object],
        scenario: dict[str, object],
        name: str,
        overrides: dict[str, str],
    ) -> None:
        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        host, controller, action = CORE_API_KEYS[name]
        packet_code_for_default = "2015" if name == "five_level" else "2006"
        stock_id = normalize_stock_id(
            str(
                overrides.get("StockID")
                or overrides.get("stock_id")
                or overrides.get("stock")
                or latest_stock_for_code(packet_code_for_default)
            )
        )
        if not stock_id:
            self._send_json({"error": "missing_stock_id", "message": "Pass StockID=688008"}, status=400)
            return
        if name == "five_level":
            result = latest_five_level(stock_id)
            packet_code = "2015"
            not_found_message = f"no hqStock 2015 five-level packet found for {stock_id}"
        elif name == "time_sales":
            try:
                limit = max(1, min(1000, int(overrides.get("limit", "100"))))
            except ValueError:
                limit = 100
            result = latest_time_sales(stock_id, limit=limit)
            packet_code = "2006"
            not_found_message = f"no hqStock 2006 time-sales packet found for {stock_id}"
        else:
            self._send_json({"error": "not_found", "message": f"unknown local core api: {name}"}, status=404)
            return
        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": scenario.get("session_id", f"core:{name}"),
                "title": scenario.get("title", f"{controller}.{action}"),
                "title_cn": scenario.get("title_cn", ""),
                "endpoint": scenario.get("endpoint", f"/api/core/{name}"),
                "target_url": scenario.get("target_url", str(HQSTOCK_LOG)),
                "http_method": self.command,
                "status": "ok" if result else "not_found",
                "status_code": 200 if result else 404,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(overrides),
            }
        )
        if not result:
            self._send_json(
                {
                    "error": "not_found",
                    "message": not_found_message,
                    "stock": stock_id,
                    "log": str(HQSTOCK_LOG),
                    "hint": "Start Frida capture and open the stock quote page before calling this API.",
                },
                status=404,
            )
            return
        self._send_json(
            {
                "requested_at": requested_at,
                "status_code": 200,
                "content_type": "application/json",
                "upstream_url": str(HQSTOCK_LOG),
                "core_api": {
                    "name": name,
                    "host": host,
                    "controller": controller,
                    "action": action,
                    "packet_code": packet_code,
                },
                "body": result,
            }
        )

    def _handle_core_api(self, user: dict[str, object], path: str) -> None:
        if self.command not in {"GET", "POST"}:
            self._send_json({"error": "method_not_allowed"}, status=405)
            return

        if path == "/api/core":
            self._send_json(
                {
                    "apis": [
                        {
                            "name": name,
                            "host": host,
                            "controller": controller,
                            "action": action,
                            "endpoint": f"/api/core/{name}",
                        }
                        for name, (host, controller, action) in CORE_API_KEYS.items()
                    ]
                }
            )
            return

        name = path[len("/api/core/") :].strip("/")
        if name not in CORE_API_KEYS:
            self._send_json({"error": "not_found", "message": f"unknown core api: {name}"}, status=404)
            return

        parsed = urlparse(self.path)
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values()
        overrides = {**query_values, **body_values}
        overrides.pop("_ts", None)

        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        host, controller, action = CORE_API_KEYS[name]
        if name in CORE_LOCAL_API_KEYS:
            scenario = next(
                (item for item in SCENARIOS if item.get("core_name") == name),
                {
                    "session_id": f"core:{name}",
                    "title": f"{controller}.{action}",
                    "title_cn": CORE_LOCAL_TITLES.get(name, {}).get("title_cn", ""),
                    "endpoint": f"/api/core/{name}",
                    "target_url": str(HQSTOCK_LOG),
                },
            )
            self._call_core_scene(user, scenario, name, overrides)
            return

        client = KaipanlaCoreClient()
        try:
            response = client.request_core(name, **overrides)
        except Exception as exc:
            _append_call_log(
                {
                    "requested_at": requested_at,
                    "requested_at_text": started_iso,
                    "username": user.get("username", ""),
                    "role": user.get("role", ""),
                    "session_id": f"core:{name}",
                    "title": f"{controller}.{action}",
                    "title_cn": f"核心接口 {name}",
                    "endpoint": f"/api/core/{name}",
                    "target_url": f"https://{host}/w1/api/index.php",
                    "http_method": "POST",
                    "status": "failed",
                    "status_code": 502,
                    "duration_ms": int((time.time() - requested_at) * 1000),
                    "overrides": _safe_log_values(overrides),
                    "error": str(exc),
                }
            )
            self._send_json(
                {
                    "error": "upstream_request_failed",
                    "message": str(exc),
                    "core_api": name,
                    "overrides": overrides,
                },
                status=502,
            )
            return

        duration_ms = int((time.time() - requested_at) * 1000)
        content_type = response.headers.get("Content-Type", "")
        try:
            body: object = response.json()
        except ValueError:
            body = response.text

        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": f"core:{name}",
                "title": f"{controller}.{action}",
                "title_cn": f"核心接口 {name}",
                "endpoint": f"/api/core/{name}",
                "target_url": response.url,
                "http_method": "POST",
                "status": "ok" if response.ok else "upstream_error",
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "overrides": _safe_log_values(overrides),
            }
        )
        self._send_json(
            {
                "requested_at": requested_at,
                "status_code": response.status_code,
                "content_type": content_type,
                "upstream_url": response.url,
                "core_api": {
                    "name": name,
                    "host": host,
                    "controller": controller,
                    "action": action,
                },
                "body": body,
            },
            status=200 if response.ok else 502,
        )

    def _require_user(self) -> tuple[dict[str, object] | None, str | None]:
        return AUTH.session_user(self._session_token())

    def _send_auth_failure(self, error: str, json_response: bool) -> None:
        if json_response:
            status = 403 if error in {"disabled", "expired"} else 401
            self._send_json({"error": error, "message": error}, status=status)
            return
        target = "/expired.html" if error == "expired" else f"/login.html?next={self.path}"
        self.send_response(302)
        self._send_cors_headers()
        self.send_header("Location", target)
        self.end_headers()

    def _session_token(self) -> str | None:
        raw = self.headers.get("Cookie", "")
        cookie = SimpleCookie()
        cookie.load(raw)
        value = cookie.get(SESSION_COOKIE)
        return value.value if value else None

    def _make_session_cookie(self, token: str | None) -> tuple[str, str]:
        return (
            "Set-Cookie",
            f"{SESSION_COOKIE}={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age={7 * 24 * 60 * 60}",
        )

    def _clear_session_cookie(self) -> tuple[str, str]:
        return ("Set-Cookie", f"{SESSION_COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0")

    def _read_body_values(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}

        raw = self.rfile.read(length)
        content_type = self.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                payload = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                return {}
            if isinstance(payload, dict):
                return {str(key): str(value) for key, value in payload.items() if value is not None}
            return {}

        text = raw.decode("utf-8", "replace")
        return self._flatten_query(parse_qs(text, keep_blank_values=True))

    @staticmethod
    def _flatten_query(values: dict[str, list[str]]) -> dict[str, str]:
        return {key: items[-1] if items else "" for key, items in values.items()}

    def _read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _serve_file(self, path: Path, fallback_content_type: str) -> None:
        if not path.exists() or not path.is_file():
            self._send_json({"error": "file_not_found", "path": path.name}, status=404)
            return
        content_type = mimetypes.guess_type(path.name)[0] or fallback_content_type
        body = path.read_bytes()
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(
        self,
        payload: object,
        status: int = 200,
        extra_headers: list[tuple[str, str]] | None = None,
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        for key, value in extra_headers or []:
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve generated Kaipanla scene APIs.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), ScenarioApiHandler)
    print(f"Serving scenario APIs on http://{args.host}:{args.port}")
    print(f"Scenario list: http://{args.host}:{args.port}/api/scenarios")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
