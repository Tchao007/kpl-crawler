# -*- coding: utf-8 -*-
"""HTTP API wrapper for generated Kaipanla capture scenarios."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
from datetime import datetime, timedelta, timezone
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
STATIC_DIR = ROOT / "static"
SPA_INDEX_FILE = STATIC_DIR / "index.html"
AUTH_DB_FILE = ROOT / "users.json"
SCENARIO_LEVEL_FILE = ROOT / "scenario_levels.json"
SCENARIO_META_FILE = ROOT / "scenario_meta.json"
CALL_LOG_FILE = ROOT / "scenario_call_logs.jsonl"
FRIDA_CAPTURE_LOG = ROOT.parent / "outputs" / "frida" / "kpl_capture.ndjson"
DEFAULT_INTERFACE_ADDED_TIME = "2026-06-25"
SESSION_COOKIE = "kpl_session"
AUTH = AuthStore(AUTH_DB_FILE)
SENSITIVE_LOG_KEYS = {"token", "userid", "deviceid", "clientsign", "log", "datalist", "x-api-key"}
MAX_CALL_LOGS = 1000
UPSTREAM_IDENTITY_CACHE: dict[str, object] = {"mtime": 0.0, "identity": {}}
LATEST_MARKET_DAY_CACHE: dict[str, object] = {"expires_at": 0.0, "day": ""}
INTERFACE_API_KEY_HEADER = "x-api-key"
LEGACY_INTERFACE_API_KEY_FIELDS = {"activation_code", "ActivationCode", "api_activation_code", "code"}
CHINA_TZ = timezone(timedelta(hours=8))
STOCK_GETNEWESTDAY_SESSION_ID = "213"
DYNAMIC_LATEST_DATE_FIELDS = {
    "1880": {"Time": "date"},
    "18019": {"Day": "compact"},
    "18021": {"Day": "compact"},
    "18249": {"Time": "date"},
    "18250": {"Time": "date"},
    "18252": {"Time": "date"},
}
SENTIMENT_TEMPLATE_PATHS = {
    "/api/sentiment": "sentiment",
    "/api/emotion/mood": "mood",
    "/api/emotion/distribution": "distribution",
}
SENTIMENT_TEMPLATE_SOURCES = {
    "change": ("HisHomeDingPan", "ChangeStatistics"),
    "daily_limit": ("HomeDingPan", "DailyLimitIndex"),
    "distribution": ("HomeDingPan", "MarketStockZDNum"),
    "mood": ("MarketMood", "MoodNumCount"),
    "volume": ("HisHomeDingPan", "MarketVolumeBenchmarkLine"),
    "capacity": ("HomeDingPan", "MarketCapacityKLine"),
}
SENTIMENT_TEMPLATE_SCENARIO_IDS = {
    "sentiment": "template:sentiment",
    "mood": "template:emotion_mood",
    "distribution": "template:emotion_distribution",
}
EMOTION_BODY_ONLY_SESSION_IDS = {
    "18019",
    "18126",
    "18208",
    "18209",
    "18210",
    "18211",
    "18212",
    "18213",
    "18214",
    "18215",
    "18216",
    "18217",
    "18218",
    "18219",
    "18220",
    "18221",
    "18222",
    "18223",
    "18224",
    "18233",
    "18234",
    "18235",
    "18236",
    "18237",
    "18238",
    "18239",
    "18240",
    "18241",
    "18242",
    "18243",
    "18244",
    "18245",
    "18246",
    "18247",
    "18248",
    "18303",
}
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


def _find_request_spec(controller: str, action: str) -> dict[str, object] | None:
    for spec in REQUESTS:
        data = spec.get("data") or {}
        if str(data.get("c", "")).lower() == controller.lower() and str(data.get("a", "")).lower() == action.lower():
            return spec
    return None


def _latest_day_from_update_payload(payload: object) -> str:
    if not isinstance(payload, dict):
        return ""
    raw_time = payload.get("Time") or payload.get("time")
    if raw_time in {None, ""}:
        return ""
    try:
        timestamp = int(float(str(raw_time)))
    except ValueError:
        return ""
    return datetime.fromtimestamp(timestamp, CHINA_TZ).date().isoformat()


def _format_latest_day(day: str, kind: str) -> str:
    if kind == "compact":
        return day.replace("-", "")
    return day


def _latest_market_day_cached() -> str:
    now = time.time()
    cached_day = str(LATEST_MARKET_DAY_CACHE.get("day") or "")
    if cached_day and float(LATEST_MARKET_DAY_CACHE.get("expires_at") or 0) > now:
        return cached_day

    update_spec = _find_request_spec("LongHuBang", "UpdateList")
    if not update_spec:
        return cached_day
    client = KaipanlaCapturedClient()
    client.session.trust_env = False
    captured_identity = _latest_upstream_identity()
    data = dict(update_spec.get("data") or {})
    params = dict(update_spec.get("params") or {})
    upstream_user_id = os.environ.get("KPL_UPSTREAM_USER_ID") or captured_identity.get("UserID")
    upstream_token = os.environ.get("KPL_UPSTREAM_TOKEN") or captured_identity.get("Token")
    upstream_device_id = os.environ.get("KPL_UPSTREAM_DEVICE_ID") or captured_identity.get("DeviceID")
    if upstream_user_id and _is_placeholder_value(data.get("UserID")):
        data["UserID"] = upstream_user_id
    if upstream_token and _is_placeholder_value(data.get("Token")):
        data["Token"] = upstream_token
    if upstream_device_id and _is_placeholder_value(data.get("DeviceID")):
        data["DeviceID"] = upstream_device_id
    params["_ts"] = str(int(now * 1000))
    try:
        response = client.request(update_spec, data=data, params=params)
        latest_day = _latest_day_from_update_payload(response.json())
    except Exception:
        latest_day = ""
    if latest_day:
        LATEST_MARKET_DAY_CACHE["day"] = latest_day
        LATEST_MARKET_DAY_CACHE["expires_at"] = now + 60
        return latest_day
    return cached_day


def _scenarios_with_latest_date_defaults(scenarios: list[dict[str, object]]) -> list[dict[str, object]]:
    latest_day = _latest_market_day_cached()
    if not latest_day:
        return scenarios
    result: list[dict[str, object]] = []
    for scenario in scenarios:
        fields = DYNAMIC_LATEST_DATE_FIELDS.get(str(scenario.get("session_id", "")))
        if not fields:
            result.append(scenario)
            continue
        item = dict(scenario)
        data = dict(item.get("data") or {})
        for field, kind in fields.items():
            if field in data:
                data[field] = _format_latest_day(latest_day, kind)
        item["data"] = data
        result.append(item)
    return result


def _compact_date(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) >= 8:
        return digits[:8]
    return ""


def _display_date(compact_date: str) -> str:
    if len(compact_date) == 8:
        return f"{compact_date[:4]}-{compact_date[4:6]}-{compact_date[6:8]}"
    return compact_date


def _clean_none_values(payload: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in payload.items() if value is not None}


def _iter_payload_items(payload: object):
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield str(key), value
            yield from _iter_payload_items(value)
    elif isinstance(payload, list):
        for item in payload:
            yield from _iter_payload_items(item)


def _normalized_field_name(name: object) -> str:
    return "".join(ch.lower() for ch in str(name) if ch.isalnum())


def _coerce_number(value: object) -> int | float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value) if float(value).is_integer() else float(value)
    text = str(value).strip().replace(",", "").replace("%", "")
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return int(number) if number.is_integer() else number


def _first_number(payload: object, *field_names: str) -> int | float | None:
    wanted = {_normalized_field_name(name) for name in field_names}
    for key, value in _iter_payload_items(payload):
        if _normalized_field_name(key) in wanted:
            number = _coerce_number(value)
            if number is not None:
                return number
    return None


def _extract_first_list(payload: object, *field_names: str) -> list[object]:
    wanted = {_normalized_field_name(name) for name in field_names}
    for key, value in _iter_payload_items(payload):
        if _normalized_field_name(key) in wanted and isinstance(value, list):
            return value
    return []


def _build_sentiment_board(raw_sources: dict[str, object]) -> dict[str, object]:
    all_sources = list(raw_sources.values())
    distribution_source = raw_sources.get("distribution")
    daily_limit_source = raw_sources.get("daily_limit")
    mood_source = raw_sources.get("mood")
    change_source = raw_sources.get("change")
    return _clean_none_values(
        {
            "todayZhangTing": _first_number(
                daily_limit_source,
                "todayZhangTing",
                "ZhangTing",
                "ZTNum",
                "ZT",
                "ztNum",
                "LimitUp",
            ),
            "lastZhangTing": _first_number(daily_limit_source, "lastZhangTing", "YesterdayZT", "YZTNum"),
            "todayDieTing": _first_number(daily_limit_source, "todayDieTing", "DTNum", "DT", "LimitDown"),
            "lastDieTing": _first_number(daily_limit_source, "lastDieTing", "YesterdayDT", "YDTNum"),
            "upCount": _first_number(
                distribution_source,
                "upCount",
                "UpCount",
                "ZhangNum",
                "SZJS",
                "SZZS",
                "RedNum",
                "riseCount",
            ),
            "downCount": _first_number(
                distribution_source,
                "downCount",
                "DownCount",
                "DieNum",
                "XDJS",
                "XDZS",
                "GreenNum",
                "fallCount",
            ),
            "flatCount": _first_number(distribution_source, "flatCount", "FlatCount", "PingNum", "PJS", "equalCount"),
            "intensity": _first_number(
                mood_source,
                "intensity",
                "Mood",
                "MoodNum",
                "MoodValue",
                "Strength",
                "Score",
                "ZHQD",
                "QDD",
            )
            or _first_number(change_source, "intensity", "Strength", "Score", "ZHQD", "QDD"),
            "lastZTMoney": _first_number(all_sources, "lastZTMoney", "LastZTMoney", "ZTMoney", "YZZJXY"),
            "lastLBMoney": _first_number(all_sources, "lastLBMoney", "LastLBMoney", "LBMoney", "YZLBZJXY"),
        }
    )


def _build_sentiment_distribution(raw_sources: dict[str, object], board: dict[str, object]) -> dict[str, object]:
    volume_source = raw_sources.get("volume")
    capacity_source = raw_sources.get("capacity")
    distribution_source = raw_sources.get("distribution")
    return _clean_none_values(
        {
            "upCount": board.get("upCount"),
            "downCount": board.get("downCount"),
            "flatCount": board.get("flatCount"),
            "volume": _first_number(volume_source, "volume", "Vol", "MarketVolume", "CJL", "CJE"),
            "amount": _first_number(volume_source, "amount", "Money", "MarketAmount", "CJE", "Turnover"),
            "capacity": _first_number(capacity_source, "capacity", "MarketCapacity", "Capacity", "RongLiang"),
            "rawDistribution": distribution_source,
            "rawVolume": volume_source,
            "rawCapacity": capacity_source,
        }
    )


def _is_emotion_body_only_scenario(scenario: dict[str, object]) -> bool:
    session_id = str(scenario.get("session_id") or "")
    if session_id in EMOTION_BODY_ONLY_SESSION_IDS:
        return True
    text = f"{scenario.get('title', '')} {scenario.get('title_cn', '')} {scenario.get('method_name', '')}".lower()
    return any(keyword in text for keyword in ("情绪", "大幅回撤", "涨停表现", "风向标", "emotion", "mood"))


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


TITLE_CN_FIXES = {
    "18001": "异动看盘 P19",
    "18003": "市场风口数据",
    "18012": "异动看盘列表",
    "18013": "异动看盘详情",
    "18019": "市场情绪指标",
    "18021": "异动股票列表",
    "18026": "市场主题机会",
    "18054": "异动看盘 P41",
    "18055": "上证指数数据",
    "18059": "指数行情",
    "18061": "涨停统计",
    "18062": "跌停统计",
    "18063": "市场概览",
    "18065": "热点题材",
    "18071": "个股异动",
    "18080": "异动看盘 P85",
    "18083": "主题机会数据",
    "18090": "异动看盘 P140",
    "18091": "异动看盘 P176",
    "18092": "市场强度指标",
    "18124": "异动看盘 P301",
    "18125": "异动看盘 P143",
    "18126": "市场情绪明细",
    "18127": "异动看盘 P177",
    "18128": "市场机会明细",
    "18139": "异动看盘 P40",
    "18157": "严重异动列表",
    "18162": "市场提醒列表",
    "18181": "严重异动提醒数据",
    "18182": "异动提醒",
    "18190": "异动看盘 P174",
    "18191": "异动数据",
    "18207": "异动看盘 P507",
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
    "18229": "市场量能-个股区间访问历史",
    "18230": "市场量能-个股区间访问实时",
    "18231": "市场量能-指数区间访问历史",
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
    "18259": "龙虎榜-游资组合信息-成都系",
    "18260": "龙虎榜-游资组合信息-佛山系",
    "18261": "龙虎榜-游资组合信息-炒股养家",
    "18262": "龙虎榜-游资组合信息-赵老哥",
    "18263": "龙虎榜-游资组合信息-小鳄鱼",
    "18264": "龙虎榜-游资组合信息-作手新一",
    "18265": "龙虎榜-游资组合信息-章盟主",
    "18266": "龙虎榜-游资组合信息-量化基金",
    "18267": "龙虎榜-游资组合信息-上塘路",
    "18268": "龙虎榜-游资组合信息-北京光华路",
    "18269": "龙虎榜-游资组合信息-思明南路",
    "18270": "龙虎榜-游资组合信息-南京帮",
    "18271": "龙虎榜-游资组合信息-机构",
    "18272": "龙虎榜-游资组合流水-成都系",
    "18273": "龙虎榜-游资组合流水-佛山系",
    "18274": "龙虎榜-游资组合流水-炒股养家",
    "18275": "龙虎榜-游资组合流水-赵老哥",
    "18276": "龙虎榜-游资组合流水-小鳄鱼",
    "18277": "龙虎榜-游资组合流水-作手新一",
    "18278": "龙虎榜-游资组合流水-章盟主",
    "18279": "龙虎榜-游资组合流水-量化基金",
    "18280": "龙虎榜-游资组合流水-上塘路",
    "18281": "龙虎榜-游资组合流水-北京光华路",
    "18282": "龙虎榜-游资组合流水-思明南路",
    "18283": "龙虎榜-游资组合流水-南京帮",
    "18284": "龙虎榜-游资组合流水-机构",
    "18285": "行情-历史指数窄幅走势",
    "18286": "行情-历史排名信息",
    "18287": "行情-历史题材指数排名",
    "18288": "行情-历史行业指数排名",
    "18289": "行情-历史地域指数排名",
    "18290": "行情-历史行业指数时间段排名",
    "18291": "行情-历史地域指数时间段排名",
}


def _looks_garbled_title(value: str) -> bool:
    if not value:
        return False
    if "?" in value or "\ufffd" in value:
        return True
    mojibake_markers = ("鐢", "鎯", "甯", "榫", "琛", "棰", "涓", "鍘", "娑", "椋")
    return any(marker in value for marker in mojibake_markers)


def _fixed_title_cn(session_id: str, value: str) -> str:
    fixed = TITLE_CN_FIXES.get(session_id)
    if fixed and _looks_garbled_title(value):
        return fixed
    return value


def _title_cn_for(spec: dict[str, object], controller: object, action: object) -> str:
    session_id = str(spec.get("session_id") or "")
    meta_title = _scenario_meta_for(session_id).get("title_cn", "")
    if meta_title and not _looks_garbled_title(meta_title):
        return meta_title
    spec_title = str(spec.get("title_cn", "")).strip()
    fixed = _fixed_title_cn(session_id, spec_title)
    if fixed:
        return fixed
    if session_id in TITLE_CN_BY_SESSION:
        return _fixed_title_cn(session_id, TITLE_CN_BY_SESSION[session_id])
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
    for template_name, endpoint in {
        "sentiment": "/api/sentiment",
        "mood": "/api/emotion/mood",
        "distribution": "/api/emotion/distribution",
    }.items():
        session_id = SENTIMENT_TEMPLATE_SCENARIO_IDS[template_name]
        core_meta = _scenario_meta_for(session_id)
        default_titles = {
            "sentiment": ("Sentiment.Template", "情绪模板-情绪总览"),
            "mood": ("Sentiment.MoodTemplate", "情绪模板-综合强度"),
            "distribution": ("Sentiment.DistributionTemplate", "情绪模板-涨跌分布与量能"),
        }
        title, title_cn = default_titles[template_name]
        level = _scenario_level_for(session_id)
        scenarios.append(
            {
                "session_id": session_id,
                "title": core_meta.get("title", title),
                "title_cn": core_meta.get("title_cn", title_cn),
                "added_time": core_meta.get("maintenance_time", "2026-07-01"),
                "maintenance_time": core_meta.get("maintenance_time", "2026-07-01"),
                "level": level,
                "level_label": SCENARIO_LEVELS[level],
                "method_name": endpoint.rsplit("/", 1)[-1].replace("-", "_"),
                "http_method": "GET",
                "target_url": "sentiment-template",
                "endpoint": endpoint,
                "alias_endpoint": endpoint,
                "params": {"date": ""},
                "data": {},
                "is_template": True,
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

        if path.startswith("/assets/") or path.startswith("/static/"):
            static_path = path[len("/static") :] if path.startswith("/static/") else path
            self._serve_static_file(STATIC_DIR / static_path.lstrip("/"))
            return

        if path in {"/", "/index.html", f"/{PAGE_FILE}", f"/{ADMIN_FILE}", "/admin"}:
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=False)
                return
            if path in {f"/{ADMIN_FILE}", "/admin"} and user.get("role") != "admin":
                self._send_json({"error": "forbidden", "message": "Admin role required"}, status=403)
                return
            if path in {f"/{ADMIN_FILE}", "/admin"}:
                self._serve_file(ROOT / ADMIN_FILE, "text/html; charset=utf-8")
                return
            page_path = SPA_INDEX_FILE if SPA_INDEX_FILE.exists() else ROOT / PAGE_FILE
            self._serve_file(page_path, "text/html; charset=utf-8")
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
                    "scenarios": _scenarios_with_latest_date_defaults(SCENARIOS),
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

        if path in SENTIMENT_TEMPLATE_PATHS:
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            if self.command not in {"GET", "POST"}:
                self._send_json({"error": "method_not_allowed"}, status=405)
                return
            if not self._validate_interface_api_key(user):
                return
            self._handle_sentiment_template_api(user, path, parsed)
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
            if not self._validate_interface_api_key(user):
                return
            for key in LEGACY_INTERFACE_API_KEY_FIELDS:
                overrides.pop(key, None)
            if route.get("core_name"):
                self._call_core_scene(user, route["scenario"], str(route["core_name"]), overrides)
                return
            self._call_scene(user, route["scenario"], route["spec"], overrides)
            return

        self._send_json({"error": "not_found", "path": path}, status=404)

    def _handle_sentiment_template_api(self, user: dict[str, object], path: str, parsed) -> None:
        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        mode = SENTIMENT_TEMPLATE_PATHS[path]
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values() if self.command == "POST" else {}
        overrides = {**query_values, **body_values}
        for key in LEGACY_INTERFACE_API_KEY_FIELDS | {"_ts"}:
            overrides.pop(key, None)

        latest_day = _latest_market_day_cached()
        latest_compact = _format_latest_day(latest_day, "compact") if latest_day else ""
        today_compact = datetime.now(CHINA_TZ).strftime("%Y%m%d")
        requested_date = _compact_date(overrides.get("date") or overrides.get("Day")) or latest_compact or today_compact
        data_date = latest_compact or requested_date
        source_names = {
            "sentiment": ["daily_limit", "distribution", "mood", "change", "volume", "capacity"],
            "mood": ["mood", "change", "daily_limit"],
            "distribution": ["distribution", "volume", "capacity"],
        }[mode]

        client = KaipanlaCapturedClient()
        client.session.trust_env = False
        captured_identity = _latest_upstream_identity()
        source_results: dict[str, dict[str, object]] = {}
        for source_name in source_names:
            controller, action = SENTIMENT_TEMPLATE_SOURCES[source_name]
            source_results[source_name] = self._call_sentiment_template_source(
                client,
                captured_identity,
                source_name,
                controller,
                action,
                data_date,
                requested_at,
            )

        raw_sources = {name: result.get("body") for name, result in source_results.items()}
        board = _build_sentiment_board(raw_sources)
        distribution = _build_sentiment_distribution(raw_sources, board)
        source_meta = {
            name: {
                key: value
                for key, value in result.items()
                if key not in {"body"} and value not in {None, ""}
            }
            for name, result in source_results.items()
        }
        errors = {
            name: result.get("error")
            for name, result in source_results.items()
            if result.get("error") or result.get("ok") is False
        }
        base_payload: dict[str, object] = {
            "requestedDate": requested_date,
            "dataDate": data_date,
            "isFallback": requested_date != data_date,
            "date": _display_date(data_date),
            "source": "kaipanla-captured-template",
            "basis": "Aggregated from captured Kaipanla sentiment endpoints.",
            "sources": source_meta,
        }
        if mode == "mood":
            payload = {
                **base_payload,
                "intensity": board.get("intensity"),
                "board": board,
                "raw": {
                    "mood": raw_sources.get("mood"),
                    "change": raw_sources.get("change"),
                    "daily_limit": raw_sources.get("daily_limit"),
                },
            }
        elif mode == "distribution":
            payload = {
                **base_payload,
                "distribution": distribution,
                "board": {
                    key: board[key]
                    for key in ("upCount", "downCount", "flatCount")
                    if key in board
                },
                "raw": {
                    "distribution": raw_sources.get("distribution"),
                    "volume": raw_sources.get("volume"),
                    "capacity": raw_sources.get("capacity"),
                },
            }
        else:
            payload = {
                **base_payload,
                "board": board,
                "weatherVane": {
                    "topUp": _extract_first_list(raw_sources, "topUp", "TopUp", "top_up"),
                    "topDown": _extract_first_list(raw_sources, "topDown", "TopDown", "top_down"),
                },
                "distribution": distribution,
                "raw": raw_sources,
            }
        if errors:
            payload["sourceErrors"] = errors

        status_code = 200 if any(result.get("ok") for result in source_results.values()) else 502
        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": SENTIMENT_TEMPLATE_SCENARIO_IDS[mode],
                "title": f"Sentiment.{mode}",
                "title_cn": {
                    "sentiment": "情绪模板-情绪总览",
                    "mood": "情绪模板-综合强度",
                    "distribution": "情绪模板-涨跌分布与量能",
                }[mode],
                "endpoint": path,
                "target_url": "sentiment-template",
                "http_method": self.command,
                "status": "ok" if status_code == 200 else "upstream_error",
                "status_code": status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(overrides),
            }
        )
        self._send_json(payload, status=status_code)

    def _call_sentiment_template_source(
        self,
        client: KaipanlaCapturedClient,
        captured_identity: dict[str, str],
        source_name: str,
        controller: str,
        action: str,
        data_date: str,
        requested_at: float,
    ) -> dict[str, object]:
        spec = _find_request_spec(controller, action)
        if not spec:
            return {
                "ok": False,
                "source": source_name,
                "controller": controller,
                "action": action,
                "error": "source_not_found",
            }
        data = dict(spec.get("data") or {})
        params = dict(spec.get("params") or {})
        upstream_user_id = os.environ.get("KPL_UPSTREAM_USER_ID") or captured_identity.get("UserID")
        upstream_token = os.environ.get("KPL_UPSTREAM_TOKEN") or captured_identity.get("Token")
        upstream_device_id = os.environ.get("KPL_UPSTREAM_DEVICE_ID") or captured_identity.get("DeviceID")
        if upstream_user_id and _is_placeholder_value(data.get("UserID")):
            data["UserID"] = upstream_user_id
        if upstream_token and _is_placeholder_value(data.get("Token")):
            data["Token"] = upstream_token
        if upstream_device_id and _is_placeholder_value(data.get("DeviceID")):
            data["DeviceID"] = upstream_device_id
        if "Day" in data:
            data["Day"] = data_date
        if "day" in data:
            data["day"] = data_date
        if "Date" in data:
            data["Date"] = data_date
        params["_ts"] = str(int(requested_at * 1000))
        try:
            response = client.request(spec, data=data, params=params)
            content_type = response.headers.get("Content-Type", "")
            try:
                payload: object = response.json()
            except ValueError:
                payload = response.text
            return {
                "ok": response.ok,
                "source": source_name,
                "session_id": spec.get("session_id", ""),
                "controller": controller,
                "action": action,
                "status_code": response.status_code,
                "content_type": content_type,
                "upstream_url": response.url,
                "body": payload,
            }
        except Exception as exc:
            return {
                "ok": False,
                "source": source_name,
                "session_id": spec.get("session_id", ""),
                "controller": controller,
                "action": action,
                "error": str(exc),
            }

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

        self._apply_dynamic_latest_date_defaults(data, scenario, client, captured_identity, overrides, requested_at)

        if str(scenario.get("session_id", "")) == STOCK_GETNEWESTDAY_SESSION_ID and not str(overrides.get("StockID", "")).strip():
            if self._call_stock_getnewestday_latest(user, scenario, client, captured_identity, overrides, requested_at, started_iso):
                return
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

        if _is_emotion_body_only_scenario(scenario):
            self._send_json(payload)
            return

        self._send_json(
            {
                "requested_at": requested_at,
                "status_code": response.status_code,
                "content_type": content_type,
                "upstream_url": response.url,
                "body": payload,
            }
        )

    def _call_stock_getnewestday_latest(
        self,
        user: dict[str, object],
        scenario: dict[str, object],
        client: KaipanlaCapturedClient,
        captured_identity: dict[str, str],
        overrides: dict[str, str],
        requested_at: float,
        started_iso: str,
    ) -> bool:
        update_spec = _find_request_spec("LongHuBang", "UpdateList")
        if not update_spec:
            return False

        data = dict(update_spec.get("data") or {})
        params = dict(update_spec.get("params") or {})
        upstream_user_id = os.environ.get("KPL_UPSTREAM_USER_ID") or captured_identity.get("UserID")
        upstream_token = os.environ.get("KPL_UPSTREAM_TOKEN") or captured_identity.get("Token")
        upstream_device_id = os.environ.get("KPL_UPSTREAM_DEVICE_ID") or captured_identity.get("DeviceID")
        if upstream_user_id and _is_placeholder_value(data.get("UserID")):
            data["UserID"] = upstream_user_id
        if upstream_token and _is_placeholder_value(data.get("Token")):
            data["Token"] = upstream_token
        if upstream_device_id and _is_placeholder_value(data.get("DeviceID")):
            data["DeviceID"] = upstream_device_id
        params["_ts"] = str(int(requested_at * 1000))

        try:
            response = client.request(update_spec, data=data, params=params)
        except Exception:
            return False

        content_type = response.headers.get("Content-Type", "")
        try:
            upstream_payload: object = response.json()
        except ValueError:
            upstream_payload = response.text

        latest_day = _latest_day_from_update_payload(upstream_payload)
        if not latest_day:
            return False

        payload = {
            "Day": _format_latest_day(latest_day, "compact"),
            "errcode": str(upstream_payload.get("errcode", "0")) if isinstance(upstream_payload, dict) else "0",
        }
        if isinstance(upstream_payload, dict) and "t" in upstream_payload:
            payload["t"] = upstream_payload["t"]

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
                "target_url": update_spec.get("url", ""),
                "http_method": scenario.get("http_method", update_spec.get("method", "")),
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
        return True

    def _apply_dynamic_latest_date_defaults(
        self,
        data: dict[str, object],
        scenario: dict[str, object],
        client: KaipanlaCapturedClient,
        captured_identity: dict[str, str],
        overrides: dict[str, str],
        requested_at: float,
    ) -> None:
        fields = DYNAMIC_LATEST_DATE_FIELDS.get(str(scenario.get("session_id", "")))
        if not fields:
            return
        pending = {field: kind for field, kind in fields.items() if field not in overrides}
        if not pending:
            return
        latest_day = self._resolve_latest_market_day(client, captured_identity, requested_at)
        if not latest_day:
            return
        for field, kind in pending.items():
            data[field] = _format_latest_day(latest_day, kind)

    def _resolve_latest_market_day(
        self,
        client: KaipanlaCapturedClient,
        captured_identity: dict[str, str],
        requested_at: float,
    ) -> str:
        update_spec = _find_request_spec("LongHuBang", "UpdateList")
        if not update_spec:
            return ""
        data = dict(update_spec.get("data") or {})
        params = dict(update_spec.get("params") or {})
        upstream_user_id = os.environ.get("KPL_UPSTREAM_USER_ID") or captured_identity.get("UserID")
        upstream_token = os.environ.get("KPL_UPSTREAM_TOKEN") or captured_identity.get("Token")
        upstream_device_id = os.environ.get("KPL_UPSTREAM_DEVICE_ID") or captured_identity.get("DeviceID")
        if upstream_user_id and _is_placeholder_value(data.get("UserID")):
            data["UserID"] = upstream_user_id
        if upstream_token and _is_placeholder_value(data.get("Token")):
            data["Token"] = upstream_token
        if upstream_device_id and _is_placeholder_value(data.get("DeviceID")):
            data["DeviceID"] = upstream_device_id
        params["_ts"] = str(int(requested_at * 1000))
        try:
            response = client.request(update_spec, data=data, params=params)
            return _latest_day_from_update_payload(response.json())
        except Exception:
            return ""

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
        if not self._validate_interface_api_key(user):
            return
        for key in LEGACY_INTERFACE_API_KEY_FIELDS:
            values.pop(key, None)
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
        if not self._validate_interface_api_key(user):
            return
        for key in LEGACY_INTERFACE_API_KEY_FIELDS:
            overrides.pop(key, None)

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

    def _interface_api_key(self) -> str:
        return str(self.headers.get(INTERFACE_API_KEY_HEADER) or "").strip()

    def _validate_interface_api_key(self, user: dict[str, object]) -> bool:
        code = self._interface_api_key()
        ok, error = AUTH.validate_interface_activation_code(
            str(user.get("username", "")),
            str(user.get("role", "")),
            code,
        )
        if ok:
            return True
        status = 403 if error in {"disabled", "expired"} else 400
        self._send_json(
            {
                "error": error or "invalid_activation_code",
                "message": f"Interface calls require a valid {INTERFACE_API_KEY_HEADER} header",
            },
            status=status,
        )
        return False

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

    def _serve_static_file(self, path: Path) -> None:
        try:
            resolved = path.resolve()
            static_root = STATIC_DIR.resolve()
        except OSError:
            self._send_json({"error": "file_not_found", "path": path.name}, status=404)
            return
        if static_root not in resolved.parents and resolved != static_root:
            self._send_json({"error": "forbidden"}, status=403)
            return
        self._serve_file(resolved, "application/octet-stream")

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
