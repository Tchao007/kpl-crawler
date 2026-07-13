# -*- coding: utf-8 -*-
"""HTTP API wrapper for generated Kaipanla capture scenarios."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, unquote, urlparse
from xml.etree import ElementTree as ET

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
from kpl_topic_rank_decoder import (
    DEFAULT_LOG as TOPIC_RANK_LOG,
    TOPIC_RANK_API,
    TOPIC_TABLE_API,
    available_topic_table_topics,
    available_topic_rank_days,
    latest_topic_table_content,
    latest_topic_rank_list,
    normalize_day as normalize_topic_rank_day,
)
from upstream_guard import (
    UpstreamCircuitOpen,
    UpstreamGuard,
    UpstreamRateLimited,
    host_from_url,
    stable_cache_key,
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
CHANGE_PASSWORD_FILE = "change_password.html"
STATIC_DIR = ROOT / "static"
SPA_INDEX_FILE = STATIC_DIR / "index.html"
AUTH_DB_FILE = ROOT / "users.json"
SCENARIO_LEVEL_FILE = ROOT / "scenario_levels.json"
SCENARIO_META_FILE = ROOT / "scenario_meta.json"
CALL_LOG_FILE = ROOT / "scenario_call_logs.jsonl"
UPSTREAM_IDENTITY_FILE = ROOT / "upstream_identity.local.json"
FRIDA_CAPTURE_LOG = ROOT.parent / "outputs" / "frida" / "kpl_capture.ndjson"
DEFAULT_INTERFACE_ADDED_TIME = "2026-06-25"
SESSION_COOKIE = "kpl_session"
AUTH = AuthStore(AUTH_DB_FILE)
SENSITIVE_LOG_KEYS = {"token", "userid", "deviceid", "clientsign", "log", "datalist", "x-api-key"}
MAX_CALL_LOGS = 1000
MAX_CALL_LOG_TAIL_BYTES = 2 * 1024 * 1024
MAX_FRIDA_IDENTITY_TAIL_BYTES = 4 * 1024 * 1024
UPSTREAM_IDENTITY_CACHE: dict[str, object] = {"mtime": 0.0, "identity": {}}
INTERFACE_API_KEY_HEADER = "x-api-key"
LEGACY_INTERFACE_API_KEY_FIELDS = {"activation_code", "ActivationCode", "api_activation_code", "code"}
CORE_LOCAL_ADDED_TIME = "2026-06-28"
PENDING_DELETE_GROUP = "待删除模块"
MARKET_FENGK_GROUP = "市场风口模块"
MARKET_FENGK_SESSION_IDS = {"429", "430", "432", "18003", "18013", "18019", "18021", "18071", "18337", "18338"}
MARKET_VOLUME_GROUP = "市场量能"
EMOTION_GROUP = "情绪模块"
HQ_CORE_GROUP = "行情核心"
STOCK_DETAIL_GROUP = "个股详情"
INFO_CONTENT_GROUP = "资讯内容"
TOPIC_DATA_GROUP = "题材数据"
LHB_GROUP = "龙虎榜"
BILEILA_GROUP = "避雷啦"
SYSTEM_CONFIG_GROUP = "系统配置接口"
BILEILA_EXCEL_CACHE_DIR = ROOT.parent / "outputs" / "bileila"
BILEILA_EXCEL_API = {
    "name": "bileila_excel",
    "endpoint": "/api/bileila/excel",
    "alias_endpoint": "/api/bileila/excel-download",
    "download_endpoint": "/api/bileila/excel/file",
    "description": "避雷啦 ST预警/退市预警 Excel 下载与解析",
}
UPSTREAM_GUARD = UpstreamGuard(
    min_interval=float(os.environ.get("KPL_UPSTREAM_MIN_INTERVAL", "2.0")),
    max_per_minute=int(os.environ.get("KPL_UPSTREAM_MAX_PER_MINUTE", "24")),
    max_per_hour=int(os.environ.get("KPL_UPSTREAM_MAX_PER_HOUR", "300")),
)
BEIJING_TZ = timezone(timedelta(hours=8))
TIMESTAMP_FIELD_NAMES = {
    "createtime",
    "create_time",
    "datetime",
    "endtime",
    "lasttime",
    "mtime",
    "opentime",
    "requested_at",
    "servertime",
    "server_time",
    "serverts",
    "starttime",
    "timestamp",
    "time",
    "updatetime",
    "update_time",
    "updatedat",
    "updated_at",
    "uptime",
}
STATUS_ONLY_RESPONSE_KEYS = {
    "code",
    "coin",
    "complete",
    "complete_num",
    "errcode",
    "info",
    "kaipanb",
    "message",
    "msg",
    "num",
    "serverts",
    "status",
    "success",
    "t",
    "time",
    "ttag",
}
EMPTY_LIST_RESPONSE_KEYS = STATUS_ONLY_RESPONSE_KEYS | {
    "day",
    "list",
    "msgid",
    "show",
    "uptime",
}
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


def _epoch_to_beijing_text(value: object) -> str | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        epoch = float(value)
    elif isinstance(value, str):
        text = value.strip()
        if not text or not re.fullmatch(r"\d+(?:\.\d+)?", text):
            return None
        epoch = float(text)
    else:
        return None

    if epoch > 10_000_000_000:
        epoch = epoch / 1000
    if epoch < 946_684_800 or epoch > 4_102_444_800:
        return None
    return datetime.fromtimestamp(epoch, BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S")


def _is_timestamp_field_name(key: object) -> bool:
    name = str(key or "").strip().lower()
    if not name or name.endswith(("_beijing", "_bj", "_text")):
        return False
    return name in TIMESTAMP_FIELD_NAMES or name.endswith(("time", "timestamp"))


def _with_beijing_time_fields(payload: object) -> object:
    if isinstance(payload, list):
        return [_with_beijing_time_fields(item) for item in payload]
    if not isinstance(payload, dict):
        return payload

    converted: dict[object, object] = {}
    additions: dict[str, str] = {}
    for key, value in payload.items():
        converted_value = _with_beijing_time_fields(value)
        converted[key] = converted_value
        if _is_timestamp_field_name(key):
            beijing_text = _epoch_to_beijing_text(value)
            if beijing_text:
                additions[f"{key}_beijing"] = beijing_text
    converted.update(additions)
    return converted


def _read_tail_lines(path: Path, max_bytes: int) -> list[str]:
    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            if size > max_bytes:
                handle.seek(-max_bytes, os.SEEK_END)
                handle.readline()
            data = handle.read()
    except OSError:
        return []
    return data.decode("utf-8", errors="ignore").splitlines()


def _normalize_bileila_excel_date(value: object = None) -> tuple[str, str]:
    text = str(value or "").strip()
    if not text:
        day = datetime.now(BEIJING_TZ).strftime("%Y-%m-%d")
        return day, day.replace("-", ".")
    digits = re.sub(r"\D", "", text)
    if len(digits) != 8:
        raise ValueError("date must be YYYY-MM-DD, YYYYMMDD, or YYYY.MM.DD")
    day = f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
    datetime.strptime(day, "%Y-%m-%d")
    return day, day.replace("-", ".")


def _bileila_excel_url(dot_day: str) -> str:
    return f"https://appcdn.longhuvip.com/BiLeiLa/kaipanla_bileila_{dot_day}.xlsx"


def _column_name_to_index(name: str) -> int:
    value = 0
    for char in name.upper():
        if not ("A" <= char <= "Z"):
            continue
        value = value * 26 + ord(char) - ord("A") + 1
    return max(value - 1, 0)


def _xlsx_cell_text(cell: ET.Element, shared_strings: list[str]) -> object:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        parts = [item.text or "" for item in cell.findall(".//{*}t")]
        return "".join(parts).strip()
    value_node = cell.find("{*}v")
    if value_node is None:
        return ""
    text = (value_node.text or "").strip()
    if cell_type == "s":
        try:
            return shared_strings[int(text)]
        except (ValueError, IndexError):
            return text
    if cell_type == "b":
        return text == "1"
    return text


def _unique_headers(values: list[object]) -> list[str]:
    headers: list[str] = []
    seen: dict[str, int] = {}
    for index, value in enumerate(values, start=1):
        header = str(value or "").strip() or f"Column{index}"
        seen[header] = seen.get(header, 0) + 1
        headers.append(header if seen[header] == 1 else f"{header}_{seen[header]}")
    return headers


def _parse_bileila_xlsx(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        shared_strings: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall("{*}si"):
                shared_strings.append("".join(node.text or "" for node in item.findall(".//{*}t")).strip())

        rel_targets: dict[str, str] = {}
        if "xl/_rels/workbook.xml.rels" in archive.namelist():
            rel_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
            for rel in rel_root.findall("{*}Relationship"):
                target = rel.attrib.get("Target", "")
                rel_id = rel.attrib.get("Id", "")
                if rel_id and target:
                    rel_targets[rel_id] = "xl/" + target.lstrip("/")

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets: list[dict[str, object]] = []
        all_codes: set[str] = set()
        for sheet in workbook.findall(".//{*}sheet"):
            sheet_name = sheet.attrib.get("name", "")
            rel_id = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id", "")
            sheet_path = rel_targets.get(rel_id, "")
            if not sheet_path or sheet_path not in archive.namelist():
                continue
            sheet_root = ET.fromstring(archive.read(sheet_path))
            raw_rows: list[list[object]] = []
            for row in sheet_root.findall(".//{*}sheetData/{*}row"):
                cells: list[object] = []
                for cell in row.findall("{*}c"):
                    ref = cell.attrib.get("r", "")
                    match = re.match(r"([A-Z]+)", ref)
                    column_index = _column_name_to_index(match.group(1)) if match else len(cells)
                    while len(cells) < column_index:
                        cells.append("")
                    cells.append(_xlsx_cell_text(cell, shared_strings))
                if any(str(value).strip() for value in cells):
                    raw_rows.append(cells)
                    for value in cells:
                        all_codes.update(re.findall(r"(?<!\d)(?:00|30|60|68|83|87|92)\d{4}(?!\d)", str(value)))

            headers = _unique_headers(raw_rows[0]) if raw_rows else []
            row_dicts: list[dict[str, object]] = []
            for raw_row in raw_rows[1:]:
                row_dicts.append(
                    {
                        headers[index] if index < len(headers) else f"Column{index + 1}": value
                        for index, value in enumerate(raw_row)
                        if str(value).strip()
                    }
                )
            sheets.append(
                {
                    "name": sheet_name,
                    "header": headers,
                    "row_count": len(row_dicts),
                    "rows": row_dicts,
                }
            )
    return {"sheets": sheets, "stock_codes": sorted(all_codes)}


def _load_bileila_excel(day_value: object = None, force: bool = False) -> dict[str, object]:
    day, dot_day = _normalize_bileila_excel_date(day_value)
    url = _bileila_excel_url(dot_day)
    BILEILA_EXCEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = BILEILA_EXCEL_CACHE_DIR / f"kaipanla_bileila_{dot_day}.xlsx"
    from_cache = cache_path.exists() and not force
    if not from_cache:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)",
                "Accept": "*/*",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                body = response.read()
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"upstream HTTP {exc.code}: {url}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"upstream download failed: {exc.reason}") from exc
        if not body.startswith(b"PK"):
            raise RuntimeError("upstream response is not an XLSX file")
        cache_path.write_bytes(body)
    parsed = _parse_bileila_xlsx(cache_path)
    return {
        "date": day,
        "source_url": url,
        "download_endpoint": f"{BILEILA_EXCEL_API['download_endpoint']}?date={day}",
        "cached_path": str(cache_path),
        "from_cache": from_cache,
        "file_size": cache_path.stat().st_size,
        **parsed,
    }


SCENARIO_LEVELS = {
    "rare": "稀缺",
    "important": "重要",
    "normal": "一般",
    "pending_delete": "待删除",
}

SCENARIO_LEVEL_SORT_ORDER = {
    "rare": 0,
    "important": 1,
    "normal": 2,
    "pending_delete": 3,
}


def _scenario_date_sort_value(value: object) -> int:
    text = str(value or "").strip()
    if not text:
        return 0
    digits = re.sub(r"\D", "", text)
    if len(digits) >= 8:
        return int(digits[:8])
    return 0


def _scenario_display_sort_key(scenario: dict[str, object]) -> tuple[int, int, str, str, str]:
    level = str(scenario.get("level") or "normal")
    added_time = scenario.get("added_time") or scenario.get("addedTime")
    title = str(scenario.get("title_cn") or scenario.get("title") or "")
    session_id = str(scenario.get("session_id") or "")
    endpoint = str(scenario.get("endpoint") or "")
    return (
        SCENARIO_LEVEL_SORT_ORDER.get(level, SCENARIO_LEVEL_SORT_ORDER["normal"]),
        -_scenario_date_sort_value(added_time),
        title.lower(),
        session_id,
        endpoint,
    )


def _sort_scenarios_for_display(scenarios: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(scenarios, key=_scenario_display_sort_key)


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


def _effective_scenario_level_for(session_id: object) -> str:
    session_key = str(session_id)
    if session_key in RUNTIME_PENDING_DELETE_SESSION_IDS:
        return "pending_delete"
    return _scenario_level_for(session_key)


def _is_pending_delete_scenario(scenario: dict[str, object]) -> bool:
    return (
        str(scenario.get("level") or "") == "pending_delete"
        or str(scenario.get("session_id") or "") in RUNTIME_PENDING_DELETE_SESSION_IDS
    )


def _is_market_fengk_scenario(
    spec: dict[str, object] | None = None,
    controller: object = "",
    action: object = "",
    title_cn: object = "",
) -> bool:
    spec = spec or {}
    session_id = str(spec.get("session_id") or "")
    if session_id in MARKET_FENGK_SESSION_IDS:
        return True
    data = spec.get("data") if isinstance(spec.get("data"), dict) else {}
    text = " ".join(
        str(value or "")
        for value in (
            controller,
            action,
            title_cn,
            data.get("c"),
            data.get("a"),
            data.get("FuncName"),
            spec.get("title"),
            spec.get("title_cn"),
        )
    ).lower()
    return (
        "stockfengkdata" in text
        or "forumstuyere" in text
        or "fengk" in text
        or "tuyere" in text
        or "市场风口" in text
        or "风口" in text
    )


def _scenario_group_for(
    level: str,
    spec: dict[str, object] | None = None,
    controller: object = "",
    action: object = "",
    title_cn: object = "",
) -> str:
    if level == "pending_delete":
        return PENDING_DELETE_GROUP
    if _is_market_fengk_scenario(spec, controller, action, title_cn):
        return MARKET_FENGK_GROUP

    spec = spec or {}
    session_id = str(spec.get("session_id") or "")
    data = spec.get("data") if isinstance(spec.get("data"), dict) else {}
    url = str(spec.get("url") or "").lower()
    text = " ".join(
        str(value or "")
        for value in (
            controller,
            action,
            title_cn,
            data.get("c"),
            data.get("a"),
            data.get("FuncName"),
            spec.get("title"),
            spec.get("title_cn"),
            spec.get("url"),
        )
    ).lower()

    if "市场量能" in text or re.match(r"^182(2[5-9]|3[0-2])$", session_id):
        return MARKET_VOLUME_GROUP
    if session_id in {"18222", "18295"} or "打板" in text:
        return HQ_CORE_GROUP
    if (
        "情绪" in text
        or "大幅回撤" in text
        or "涨停表现" in text
        or "风向标" in text
        or re.match(r"^182(0[8-9]|1[0-9]|2[0-4]|3[3-9]|4[0-8])$", session_id)
    ):
        return EMOTION_GROUP
    if "龙虎榜" in text or "longhubang" in text or "businessgroup" in text or "userbusiness" in text:
        return LHB_GROUP
    if "公司公告" in text or "公司研报" in text or "研报" in text or "apparticle" in url:
        return INFO_CONTENT_GROUP
    if "题材" in text or "theme" in text:
        return TOPIC_DATA_GROUP
    if (
        "个股" in text
        or "股东" in text
        or "持仓" in text
        or "stock" in text and ("notice" not in text and "stockline" not in text and "stockl2history" not in text)
    ):
        return STOCK_DETAIL_GROUP
    if (
        "行情" in text
        or "指数" in text
        or "k线" in text
        or "kline" in text
        or "zhishu" in text
        or "stockline" in text
        or "stockl2history" in text
        or "apphwhq" in url
        or "apphis" in url
    ):
        return HQ_CORE_GROUP
    if (
        "appuser" in url
        or "applog" in url
        or "getsockip" in text
        or "userinfo" in text
        or "userselectstock" in text
        or "datastatistics" in text
        or "databatchstatistics" in text
        or "sysappversion" in text
        or "system" in text
        or "log_" in text
        or "用户" in text
        or "系统" in text
        or "网络" in text
        or "埋点" in text
    ):
        return SYSTEM_CONFIG_GROUP
    return ""


def _mark_scenario_pending_delete(session_id: object) -> None:
    session_key = str(session_id or "").strip()
    if not session_key:
        return
    RUNTIME_PENDING_DELETE_SESSION_IDS.add(session_key)
    for scenario in SCENARIOS:
        if str(scenario.get("session_id") or "") != session_key:
            continue
        scenario["level"] = "pending_delete"
        scenario["level_label"] = SCENARIO_LEVELS["pending_delete"]
        scenario["group"] = PENDING_DELETE_GROUP


def _safe_log_values(values: dict[str, object]) -> dict[str, str]:
    clean: dict[str, str] = {}
    for key, value in values.items():
        if key.lower() in SENSITIVE_LOG_KEYS:
            clean[key] = "***"
        else:
            clean[key] = str(value)
    return clean


def _log_headers(headers: object) -> dict[str, str]:
    if not isinstance(headers, dict):
        try:
            return {str(key): str(value) for key, value in dict(headers).items()}
        except (TypeError, ValueError):
            return {}
    return {str(key): str(value) for key, value in headers.items()}


def _log_payload(payload: object) -> object:
    if isinstance(payload, dict):
        return {str(key): _log_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [_log_payload(item) for item in payload]
    return payload


def _request_log_payload(
    method: object,
    url: object,
    headers: object,
    params: dict[str, object],
    data: dict[str, object],
    overrides: dict[str, object],
) -> dict[str, object]:
    return {
        "method": str(method or ""),
        "url": str(url or ""),
        "headers": _log_headers(headers),
        "query": _log_payload(dict(params or {})),
        "body": _log_payload(dict(data or {})),
        "overrides": _log_payload(dict(overrides or {})),
    }


def _response_log_payload(response: object, body: object) -> dict[str, object]:
    return {
        "url": str(getattr(response, "url", "") or ""),
        "status_code": int(getattr(response, "status_code", 0) or 0),
        "headers": _log_headers(getattr(response, "headers", {})),
        "body": _log_payload(body),
    }


def _is_upstream_auth_error(body: object) -> bool:
    if not isinstance(body, dict):
        text = str(body or "").lower()
        return any(marker in text for marker in ("login", "token", "auth", "登录", "登陆", "失效", "过期", "未授权"))
    errcode = str(body.get("errcode", "")).strip()
    message = str(body.get("message") or body.get("msg") or body.get("errmsg") or body.get("error") or "").strip()
    lowered = message.lower()
    if errcode in {"1001", "1002", "401", "403"}:
        return True
    return any(marker in lowered for marker in ("login", "token", "auth", "登录", "登陆", "失效", "过期", "未授权"))


def _upstream_error_message(body: object) -> str:
    if not isinstance(body, dict):
        text = str(body or "")
        return text[:300] if text else ""
    errcode = str(body.get("errcode", "")).strip()
    message = str(body.get("message") or body.get("msg") or body.get("errmsg") or body.get("error") or "").strip()
    if errcode and errcode not in {"0", "200", "success"}:
        return message or f"upstream errcode: {errcode}"
    lowered = message.lower()
    if any(marker in lowered for marker in ("login", "token", "auth", "登录", "登陆", "失效", "过期", "未授权")):
        return message
    return ""


def _is_body_only_market_scenario(scenario: dict[str, object]) -> bool:
    if scenario.get("body_only_disabled"):
        return False
    endpoint = str(scenario.get("endpoint") or "").lower()
    alias_endpoint = str(scenario.get("alias_endpoint") or "").lower()
    title = str(scenario.get("title") or "").lower()
    return any(
        marker in value
        for value in (endpoint, alias_endpoint, title)
        for marker in ("xianhuodata_getxianhuolist", "xianhuodata/getxianhuolist")
    )


def _is_theme_infogr_scenario(scenario: dict[str, object]) -> bool:
    endpoint = str(scenario.get("endpoint") or "").lower()
    alias_endpoint = str(scenario.get("alias_endpoint") or "").lower()
    title = str(scenario.get("title") or "").lower()
    return any(
        marker in value
        for value in (endpoint, alias_endpoint, title)
        for marker in ("theme_infogr", "theme/infogr")
    )


def _is_stock_getnewestday_scenario(scenario: dict[str, object]) -> bool:
    endpoint = str(scenario.get("endpoint") or "").lower()
    alias_endpoint = str(scenario.get("alias_endpoint") or "").lower()
    title = str(scenario.get("title") or "").lower()
    return any(
        marker in value
        for value in (endpoint, alias_endpoint, title)
        for marker in ("stock_getnewestday", "stock/getnewestday")
    )


def _latest_weekday_trading_day(now: datetime | None = None) -> str:
    day = (now or datetime.now()).date()
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day.isoformat()


def _parse_day_text(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) >= 8:
        return f"{digits[:4]}-{digits[4:6]}-{digits[6:8]}"
    return text


def _stock_newestday_payload(payload: object) -> object:
    if not isinstance(payload, dict):
        return payload
    fixed = dict(payload)
    latest_day = _latest_weekday_trading_day()
    date_keys = ("Day", "Date", "NewestDay", "NewDay", "TradeDate", "TradingDay", "latest_trading_day")
    matched_key = next((key for key in date_keys if key in fixed), "")
    raw_day = _parse_day_text(fixed.get(matched_key)) if matched_key else ""
    target_key = matched_key or "Day"
    fixed[target_key] = latest_day
    fixed["latest_trading_day"] = latest_day
    fixed["raw_latest_trading_day"] = raw_day
    fixed["latest_trading_day_fixed"] = raw_day != latest_day
    fixed["latest_trading_day_source"] = "local_weekday_calendar"
    return fixed


def _flatten_for_dataframe(value: object, prefix: str = "") -> dict[str, object]:
    if isinstance(value, dict):
        flattened: dict[str, object] = {}
        for key, item in value.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(item, dict):
                flattened.update(_flatten_for_dataframe(item, name))
            elif isinstance(item, list):
                flattened[name] = json.dumps(item, ensure_ascii=False)
            else:
                flattened[name] = item
        return flattened
    return {prefix or "value": value}


def _find_dataframe_rows(payload: object) -> tuple[list[dict[str, object]], str]:
    if isinstance(payload, list):
        if all(isinstance(item, dict) for item in payload):
            return [_flatten_for_dataframe(item) for item in payload], "root"
        return [{"value": item} for item in payload], "root"
    if not isinstance(payload, dict):
        return [{"value": payload}], "root"
    candidates = ("List", "list", "Data", "data", "Rows", "rows", "Result", "result")
    for key in candidates:
        value = payload.get(key)
        if isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                return [_flatten_for_dataframe(item) for item in value], key
            return [{"value": item} for item in value], key
    for key, value in payload.items():
        if isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                return [_flatten_for_dataframe(item) for item in value], str(key)
            return [{"value": item} for item in value], str(key)
    return [_flatten_for_dataframe(payload)], "root"


def _dataframe_payload(payload: object) -> dict[str, object]:
    rows, source = _find_dataframe_rows(payload)
    columns: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)
    data = [[row.get(column) for column in columns] for row in rows]
    return {
        "format": "dataframe",
        "source": source,
        "columns": columns,
        "data": data,
        "records": rows,
        "shape": [len(rows), len(columns)],
    }


def _hq_not_found_payload(packet_code: str, label: str, stock_id: str) -> dict[str, object]:
    if not HQSTOCK_LOG.exists():
        message = f"hqStock capture log not found: {HQSTOCK_LOG}"
        hint = "Start Frida capture first, then open the stock quote page in the app before calling this API."
    else:
        message = f"no hqStock {packet_code} {label} packet found for {stock_id}"
        hint = "Open or refresh the target stock quote page while Frida capture is running, then call this API again."
    return {
        "error": "not_found",
        "message": message,
        "stock": stock_id,
        "log": str(HQSTOCK_LOG),
        "hint": hint,
    }


def _as_float(value: object, default: float = 0.0) -> float:
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return default


def _as_int(value: object, default: int = 0) -> int:
    try:
        return int(float(str(value).replace(",", "").strip()))
    except (TypeError, ValueError):
        return default


def _weituo_level(price: float, volume: int, amount: float) -> dict[str, object]:
    return {
        "price": price,
        "price_raw": int(round(price * 10000)),
        "volume": volume,
        "volume_unit": "lot",
        "amount": round(amount, 2),
        "amount_raw": int(round(amount * 100)),
        "amount_unit": "CNY",
    }


def _decode_weituo_five_level(stock_id: str, payload: object) -> dict[str, object] | None:
    if not isinstance(payload, dict):
        return None
    rows = payload.get("List")
    if not isinstance(rows, list):
        return None
    books: dict[str, dict[float, dict[str, float]]] = {"buy": {}, "sell": {}}
    latest_time = ""
    for row in rows:
        if not isinstance(row, list) or len(row) < 9:
            continue
        if str(row[8]) == "1":
            continue
        price = _as_float(row[2])
        volume = _as_int(row[3])
        amount = _as_float(row[4])
        if price <= 0 or volume <= 0:
            continue
        side = "buy" if str(row[6]) == "1" else "sell" if str(row[6]) == "2" else ""
        if not side:
            continue
        bucket = books[side].setdefault(price, {"volume": 0.0, "amount": 0.0})
        bucket["volume"] += volume
        bucket["amount"] += amount
        latest_time = str(row[0] or latest_time)

    buy = [
        _weituo_level(price, int(values["volume"]), float(values["amount"]))
        for price, values in sorted(books["buy"].items(), key=lambda item: item[0], reverse=True)[:5]
    ]
    sell = [
        _weituo_level(price, int(values["volume"]), float(values["amount"]))
        for price, values in sorted(books["sell"].items(), key=lambda item: item[0])[:5]
    ]
    if not buy and not sell:
        return None
    return {
        "stock": stock_id,
        "source": "online_stockl2data_getweituo",
        "packet_code": "2015",
        "packet_note": "Online parsed from StockL2Data.GetWeiTuo order data; local Frida hqStock 2015 remains fallback.",
        "time": latest_time,
        "base_price": None,
        "sell": sell,
        "buy": buy,
        "raw_fields": {
            "count": payload.get("Count"),
            "total": payload.get("total"),
            "title": payload.get("Title", ""),
            "errcode": payload.get("errcode"),
        },
    }


def _decode_weituo_time_sales(stock_id: str, payload: object, limit: int = 100) -> dict[str, object] | None:
    if not isinstance(payload, dict):
        return None
    rows = payload.get("List")
    if not isinstance(rows, list):
        return None
    trades: list[dict[str, object]] = []
    for row in rows:
        if not isinstance(row, list) or len(row) < 9:
            continue
        price = _as_float(row[2])
        volume = _as_int(row[3])
        amount = _as_float(row[4])
        if price <= 0 or volume <= 0:
            continue
        side_flag = _as_int(row[6])
        trades.append(
            {
                "time": str(row[0] or ""),
                "order_id": str(row[1] or ""),
                "price": price,
                "price_raw": int(round(price * 10000)),
                "side": "buy" if side_flag == 1 else "sell" if side_flag == 2 else "neutral",
                "side_flag": side_flag,
                "volume": volume,
                "volume_unit": "lot",
                "amount": round(amount, 2),
                "amount_raw": int(round(amount * 100)),
                "amount_unit": "CNY",
                "cancelled": str(row[8]) == "1",
                "timestamp": str(row[9] if len(row) > 9 else ""),
            }
        )
    if not trades:
        return None
    selected = trades[-limit:] if limit > 0 else trades
    return {
        "stock": stock_id,
        "source": "online_stockl2data_getweituo",
        "packet_code": "2006",
        "packet_note": "Online parsed from StockL2Data.GetWeiTuo order data; local Frida hqStock 2006 remains fallback.",
        "day": payload.get("day") or "",
        "count": len(trades),
        "trades": selected,
        "raw_fields": {
            "count": payload.get("Count"),
            "total": payload.get("total"),
            "title": payload.get("Title", ""),
            "errcode": payload.get("errcode"),
        },
    }


def _fetch_online_weituo(stock_id: str, overrides: dict[str, str]) -> tuple[object, object]:
    client = KaipanlaCapturedClient(timeout=15, min_interval=0, jitter=0)
    client.session.trust_env = False
    request_overrides = {
        "StockID": stock_id,
        "st": str(overrides.get("st") or overrides.get("St") or "25"),
        "Type": str(overrides.get("Type") or "0"),
        "Tur": str(overrides.get("Tur") or "30"),
        "Vol": str(overrides.get("Vol") or "500"),
    }
    host = "apphwhq.longhuvip.com"
    endpoint = "/api/stockl2data/getweituo"
    UPSTREAM_GUARD.before_request(host, endpoint)
    response = client.stockl2data_getweituo(**request_overrides)
    try:
        body: object = response.json()
    except ValueError:
        body = response.text
    UPSTREAM_GUARD.record_result(host, endpoint, body, _upstream_error_message(body))
    return response, body


def _fetch_online_five_level(stock_id: str, overrides: dict[str, str]) -> tuple[dict[str, object] | None, object, object]:
    response, body = _fetch_online_weituo(stock_id, overrides)
    return _decode_weituo_five_level(stock_id, body), response, body


def _fetch_online_time_sales(
    stock_id: str, overrides: dict[str, str], limit: int = 100
) -> tuple[dict[str, object] | None, object, object]:
    response, body = _fetch_online_weituo(stock_id, overrides)
    return _decode_weituo_time_sales(stock_id, body, limit=limit), response, body


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


def _latest_upstream_identity(force: bool = False) -> dict[str, str]:
    try:
        stat = FRIDA_CAPTURE_LOG.stat()
    except OSError:
        return {}
    cached_mtime = float(UPSTREAM_IDENTITY_CACHE.get("mtime") or 0)
    if not force and stat.st_mtime == cached_mtime:
        cached = UPSTREAM_IDENTITY_CACHE.get("identity")
        return dict(cached) if isinstance(cached, dict) else {}
    identity: dict[str, str] = {}
    lines = _read_tail_lines(FRIDA_CAPTURE_LOG, MAX_FRIDA_IDENTITY_TAIL_BYTES)
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


def _current_upstream_identity(force: bool = False) -> dict[str, str]:
    file_identity: dict[str, str] = {}
    if UPSTREAM_IDENTITY_FILE.exists():
        try:
            payload = json.loads(UPSTREAM_IDENTITY_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        if isinstance(payload, dict):
            file_identity = {
                key: str(payload.get(key) or "").strip()
                for key in ("UserID", "Token", "DeviceID")
            }
    captured_identity = _latest_upstream_identity(force=force)
    identity = {
        "UserID": os.environ.get("KPL_UPSTREAM_USER_ID") or file_identity.get("UserID") or captured_identity.get("UserID", ""),
        "Token": os.environ.get("KPL_UPSTREAM_TOKEN") or file_identity.get("Token") or captured_identity.get("Token", ""),
        "DeviceID": os.environ.get("KPL_UPSTREAM_DEVICE_ID") or file_identity.get("DeviceID") or captured_identity.get("DeviceID", ""),
    }
    return {key: value for key, value in identity.items() if value and not _is_placeholder_value(value)}


def _apply_upstream_identity(data: dict[str, object], identity: dict[str, str]) -> None:
    for key in ("UserID", "Token", "DeviceID"):
        value = identity.get(key)
        if value and _is_placeholder_value(data.get(key)):
            data[key] = value


def _append_call_log(record: dict[str, object]) -> None:
    try:
        with CALL_LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    except OSError:
        return


def _load_call_logs(limit: int = 200) -> list[dict[str, object]]:
    if not CALL_LOG_FILE.exists():
        return []
    lines = _read_tail_lines(CALL_LOG_FILE, MAX_CALL_LOG_TAIL_BYTES)
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


def _is_scalar_status_value(value: object) -> bool:
    return value is None or isinstance(value, (str, int, float, bool))


def _unwrap_response_body(payload: object) -> object:
    if isinstance(payload, dict):
        response = payload.get("response")
        if isinstance(response, dict) and "body" in response:
            return response.get("body")
        if "body" in payload and {
            "requested_at",
            "status_code",
            "content_type",
            "upstream_url",
        }.intersection(payload):
            return payload.get("body")
    return payload


def _is_status_only_response_body(payload: object) -> bool:
    body = _unwrap_response_body(payload)
    if not isinstance(body, dict) or not body:
        return False
    keys = {str(key).lower() for key in body}
    if not keys <= STATUS_ONLY_RESPONSE_KEYS:
        return False
    if not {"errcode", "code", "status", "success"}.intersection(keys):
        return False
    return all(_is_scalar_status_value(value) for value in body.values())


def _is_empty_list_response_body(payload: object) -> bool:
    body = _unwrap_response_body(payload)
    if not isinstance(body, dict) or not body:
        return False
    keys = {str(key).lower() for key in body}
    if not keys <= EMPTY_LIST_RESPONSE_KEYS:
        return False
    if not isinstance(body.get("List"), list) or body.get("List"):
        return False
    if str(body.get("errcode", "0")).strip() not in {"", "0"}:
        return False
    return all(
        key == "List" or _is_scalar_status_value(value)
        for key, value in body.items()
    )


def _is_non_data_response_body(payload: object) -> bool:
    return _is_status_only_response_body(payload) or _is_empty_list_response_body(payload)


def _load_pending_delete_session_ids_from_logs() -> set[str]:
    session_ids: set[str] = set()
    for record in _load_call_logs(limit=MAX_CALL_LOGS):
        if not _is_non_data_response_body(record):
            continue
        session_id = str(record.get("session_id") or "").strip()
        if session_id:
            session_ids.add(session_id)
    return session_ids


RUNTIME_PENDING_DELETE_SESSION_IDS = _load_pending_delete_session_ids_from_logs()


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
    "18222": "行情-打板列表",
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
    "18295": "行情-打板统计数量",
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
    "18019": "历史市场情绪指标",
    "18021": "历史异动股票列表",
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
    "18222": "行情-打板列表",
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
    "18295": "行情-打板统计数量",
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


def _is_history_spec(spec: dict[str, object]) -> bool:
    url = str(spec.get("url") or "").lower()
    session_id = str(spec.get("session_id") or "")
    data = spec.get("data") if isinstance(spec.get("data"), dict) else {}
    title = " ".join(
        str(value or "")
        for value in (
            spec.get("title"),
            spec.get("title_cn"),
            data.get("c"),
            data.get("a"),
        )
    ).lower()
    if "apphis.longhuvip.com" in url:
        return True
    if "history" in title or "his" in str(data.get("c") or "").lower():
        return True
    return session_id in {
        "18019",
        "18021",
        "18218",
        "18219",
        "18220",
        "18221",
        "18222",
        "18223",
        "18224",
        "18229",
        "18231",
        "18232",
        "18239",
        "18240",
        "18241",
        "18242",
        "18243",
        "18244",
        "18245",
        "18285",
        "18286",
        "18287",
        "18288",
        "18289",
        "18290",
        "18291",
        "18295",
    }


def _history_title_cn_for(spec: dict[str, object], title_cn: str) -> str:
    if not title_cn or not _is_history_spec(spec):
        return title_cn
    if title_cn.startswith("历史"):
        return title_cn
    return f"历史{title_cn}"


def _title_cn_for(spec: dict[str, object], controller: object, action: object) -> str:
    session_id = str(spec.get("session_id") or "")
    meta_title = _scenario_meta_for(session_id).get("title_cn", "")
    if meta_title and not _looks_garbled_title(meta_title):
        return _history_title_cn_for(spec, meta_title)
    spec_title = str(spec.get("title_cn", "")).strip()
    fixed = _fixed_title_cn(session_id, spec_title)
    if fixed:
        return _history_title_cn_for(spec, fixed)
    if session_id in TITLE_CN_BY_SESSION:
        return _history_title_cn_for(spec, _fixed_title_cn(session_id, TITLE_CN_BY_SESSION[session_id]))
    return _history_title_cn_for(spec, f"{controller}.{action}")


def _title_for(spec: dict[str, object], controller: object, action: object) -> str:
    session_id = str(spec.get("session_id") or "")
    meta_title = _scenario_meta_for(session_id).get("title", "")
    if meta_title:
        return meta_title
    return f"{controller}.{action}"


def _is_system_config_scenario(scenario: dict[str, object]) -> bool:
    text = " ".join(
        str(scenario.get(key, ""))
        for key in ("title", "title_cn", "method_name", "endpoint", "alias_endpoint", "target_url", "host")
    ).lower()
    system_markers = (
        "appuser",
        "applog",
        "getsockip",
        "userinfo",
        "userselectstock",
        "datastatistics",
        "databatchstatistics",
        "log.",
        "log_",
        "system",
        "sysappversion",
        "getiplist",
        "用户",
        "系统",
        "网络",
        "埋点",
    )
    return any(marker in text for marker in system_markers)


def _scenario_risk_policy(
    level: str,
    spec: dict[str, object] | None = None,
    scenario: dict[str, object] | None = None,
) -> dict[str, object]:
    spec = spec or {}
    scenario = scenario or {}
    data = spec.get("data") if isinstance(spec.get("data"), dict) else {}
    host = host_from_url(spec.get("url") or scenario.get("target_url") or "")
    text = " ".join(
        str(value or "")
        for value in (
            host,
            spec.get("url"),
            data.get("c"),
            data.get("a"),
            scenario.get("title"),
            scenario.get("title_cn"),
            scenario.get("method_name"),
            scenario.get("endpoint"),
        )
    ).lower()
    if level == "pending_delete":
        return {
            "risk_level": "critical",
            "call_policy": "admin_only",
            "call_disabled": True,
            "risk_reason": "Non-data or pending-delete interface",
            "cache_ttl": 0,
        }
    high_markers = (
        "applog",
        "datastatistics",
        "databatchstatistics",
        "userinfo",
        "userselectstock",
        "userselect",
        "system",
        "sysappversion",
        "getsockip",
        "log_",
    )
    if any(marker in text for marker in high_markers):
        return {
            "risk_level": "high",
            "call_policy": "admin_only",
            "call_disabled": True,
            "risk_reason": "User state, system config or tracking endpoint",
            "cache_ttl": 0,
        }
    if "apphis.longhuvip.com" in text or _is_history_spec(spec):
        return {
            "risk_level": "medium",
            "call_policy": "rate_limited_cached",
            "call_disabled": False,
            "risk_reason": "Historical upstream endpoint",
            "cache_ttl": 600,
        }
    if "theme" in text or "zhishu" in text or "stockfengk" in text:
        return {
            "risk_level": "medium",
            "call_policy": "rate_limited_cached",
            "call_disabled": False,
            "risk_reason": "Market data endpoint",
            "cache_ttl": 30,
        }
    return {
        "risk_level": "low",
        "call_policy": "rate_limited_cached",
        "call_disabled": False,
        "risk_reason": "Standard upstream endpoint",
        "cache_ttl": 5,
    }


def _cache_ttl_for_scenario(scenario: dict[str, object]) -> int:
    try:
        return max(0, int(scenario.get("cache_ttl", 0)))
    except (TypeError, ValueError):
        return 0


def _guard_error_payload(error: Exception, requested_at: float) -> tuple[dict[str, object], int]:
    retry_after = int(getattr(error, "retry_after", 60) or 60)
    code = "upstream_circuit_open" if isinstance(error, UpstreamCircuitOpen) else "upstream_rate_limited"
    status = 429 if isinstance(error, UpstreamRateLimited) else 503
    return (
        {
            "error": code,
            "message": str(error),
            "requested_at": requested_at,
            "retry_after": retry_after,
        },
        status,
    )


def _normalized_scene_overrides(spec: dict[str, object], overrides: dict[str, str]) -> dict[str, str]:
    data = spec.get("data") if isinstance(spec.get("data"), dict) else {}
    controller = str(data.get("c") or "").lower()
    action = str(data.get("a") or "").lower()
    normalized = dict(overrides)
    if controller == "theme" and action == "infoget":
        lower_id = normalized.pop("id", None)
        if lower_id is not None and "ID" not in normalized:
            normalized["ID"] = lower_id
    return normalized


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
        level = _effective_scenario_level_for(spec["session_id"])
        title = _title_for(spec, controller, action)
        title_cn = _title_cn_for(spec, controller, action)
        risk_policy = _scenario_risk_policy(level, spec, {"title": title, "title_cn": title_cn, "endpoint": endpoint})
        scenarios.append(
            {
                "session_id": spec["session_id"],
                "title": title,
                "title_cn": title_cn,
                "added_time": _interface_added_time_for(spec),
                "maintenance_time": _maintenance_time_for(spec),
                "level": level,
                "level_label": SCENARIO_LEVELS[level],
                "group": _scenario_group_for(level, spec, controller, action, title_cn),
                "risk_level": risk_policy["risk_level"],
                "call_policy": risk_policy["call_policy"],
                "call_disabled": risk_policy["call_disabled"],
                "risk_reason": risk_policy["risk_reason"],
                "cache_ttl": risk_policy["cache_ttl"],
                "method_name": method_name,
                "http_method": spec["method"],
                "target_url": spec["url"],
                "endpoint": endpoint,
                "alias_endpoint": alias_endpoint,
                "params": params,
                "data": data,
                "url_params": spec.get("url_params", []),
                "hide_url_fields": spec.get("hide_url_fields", []),
            }
        )
    for scenario in list(scenarios):
        if scenario.get("endpoint") != "/api/xianhuodata_getxianhuolist":
            continue
        copy_scenario = dict(scenario)
        copy_scenario["session_id"] = f"{scenario.get('session_id')}:copy"
        copy_scenario["title"] = f"{scenario.get('title')} Copy"
        copy_scenario["title_cn"] = f"{scenario.get('title_cn') or scenario.get('title')}（原始包装返回）"
        copy_scenario["method_name"] = "xianhuodata_getxianhuolist_copy"
        copy_scenario["endpoint"] = "/api/xianhuodata_getxianhuolist_copy"
        copy_scenario["alias_endpoint"] = "/api/xianhuodata/getxianhuolist/copy"
        copy_scenario["body_only_disabled"] = True
        copy_scenario["copy_of_endpoint"] = scenario.get("endpoint")
        scenarios.append(copy_scenario)
        break
    for scenario in list(scenarios):
        if scenario.get("endpoint") != "/api/stock_getnewestday":
            continue
        copy_scenario = dict(scenario)
        copy_scenario["session_id"] = f"{scenario.get('session_id')}:copy"
        copy_scenario["title"] = f"{scenario.get('title')} Copy"
        copy_scenario["title_cn"] = f"{scenario.get('title_cn') or scenario.get('title')} DataFrame"
        copy_scenario["method_name"] = "stock_getnewestday_copy"
        copy_scenario["endpoint"] = "/api/stock_getnewestday_copy"
        copy_scenario["alias_endpoint"] = "/api/stock/getnewestday/copy"
        copy_scenario["stock_newestday_body_only"] = True
        copy_scenario["copy_of_endpoint"] = scenario.get("endpoint")
        scenarios.append(copy_scenario)
        break
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
        level = _effective_scenario_level_for(session_id)
        risk_policy = _scenario_risk_policy(level, scenario={"title": title, "title_cn": title_cn, "endpoint": f"/api/{method_name}", "target_url": str(HQSTOCK_LOG)})
        scenarios.append(
            {
                "session_id": session_id,
                "title": title,
                "title_cn": title_cn,
                "added_time": added_time,
                "maintenance_time": maintenance_time,
                "level": level,
                "level_label": SCENARIO_LEVELS[level],
                "group": _scenario_group_for(level),
                "risk_level": risk_policy["risk_level"],
                "call_policy": risk_policy["call_policy"],
                "call_disabled": risk_policy["call_disabled"],
                "risk_reason": risk_policy["risk_reason"],
                "cache_ttl": risk_policy["cache_ttl"],
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
    topic_rank_level = _effective_scenario_level_for("topic_rank:3009")
    topic_rank_policy = _scenario_risk_policy(
        topic_rank_level,
        scenario={
            "title": "global.3009 Topic Rank List",
            "title_cn": "\u9898\u6750\u5e93-\u6bcf\u65e5\u699c\u5355\u5217\u8868",
            "endpoint": TOPIC_RANK_API["endpoint"],
            "target_url": str(TOPIC_RANK_LOG),
        },
    )
    scenarios.append(
        {
            "session_id": "topic_rank:3009",
            "title": "global.3009 Topic Rank List",
            "title_cn": "\u9898\u6750\u5e93-\u6bcf\u65e5\u699c\u5355\u5217\u8868",
            "added_time": "2026-07-05",
            "maintenance_time": "2026-07-05",
            "level": topic_rank_level,
            "level_label": SCENARIO_LEVELS[topic_rank_level],
            "group": TOPIC_DATA_GROUP,
            "risk_level": topic_rank_policy["risk_level"],
            "call_policy": topic_rank_policy["call_policy"],
            "call_disabled": topic_rank_policy["call_disabled"],
            "risk_reason": topic_rank_policy["risk_reason"],
            "cache_ttl": 0,
            "method_name": TOPIC_RANK_API["name"],
            "http_method": "GET",
            "target_url": str(TOPIC_RANK_LOG),
            "endpoint": TOPIC_RANK_API["endpoint"],
            "alias_endpoint": TOPIC_RANK_API["alias_endpoint"],
            "params": {"date": "20260705", "limit": "100"},
            "url_params": ["date", "day", "Day", "limit"],
            "data": {},
            "host": "global|26:20020",
            "source": TOPIC_RANK_API["source"],
            "packet_code": TOPIC_RANK_API["packet_code"],
            "is_local": True,
            "hide_url_fields": [],
        }
    )
    topic_table_level = _effective_scenario_level_for("topic_table:3010")
    topic_table_policy = _scenario_risk_policy(
        topic_table_level,
        scenario={
            "title": "global.3010 Topic Table Content",
            "title_cn": "\u9898\u6750\u5e93-\u5c0f\u8868\u683c\u5185\u5bb9",
            "endpoint": TOPIC_TABLE_API["endpoint"],
            "target_url": str(TOPIC_RANK_LOG),
        },
    )
    scenarios.append(
        {
            "session_id": "topic_table:3010",
            "title": "global.3010 Topic Table Content",
            "title_cn": "\u9898\u6750\u5e93-\u5c0f\u8868\u683c\u5185\u5bb9",
            "added_time": "2026-07-05",
            "maintenance_time": "2026-07-05",
            "level": topic_table_level,
            "level_label": SCENARIO_LEVELS[topic_table_level],
            "group": TOPIC_DATA_GROUP,
            "risk_level": topic_table_policy["risk_level"],
            "call_policy": topic_table_policy["call_policy"],
            "call_disabled": topic_table_policy["call_disabled"],
            "risk_reason": topic_table_policy["risk_reason"],
            "cache_ttl": 0,
            "method_name": TOPIC_TABLE_API["name"],
            "http_method": "GET",
            "target_url": str(TOPIC_RANK_LOG),
            "endpoint": TOPIC_TABLE_API["endpoint"],
            "alias_endpoint": TOPIC_TABLE_API["alias_endpoint"],
            "params": {"topic_id": "395", "date": "20260705", "limit": "100"},
            "url_params": ["topic_id", "id", "ID", "TopicID", "date", "day", "Day", "limit"],
            "data": {},
            "host": "global|26:20020",
            "source": TOPIC_TABLE_API["source"],
            "packet_code": TOPIC_TABLE_API["packet_code"],
            "is_local": True,
            "hide_url_fields": [],
        }
    )
    bileila_session_id = "bileila:excel"
    bileila_level = _effective_scenario_level_for(bileila_session_id)
    if bileila_level == "normal":
        bileila_level = "rare"
    bileila_policy = _scenario_risk_policy(
        bileila_level,
        scenario={
            "title": "BiLeiLa Excel Download",
            "title_cn": "\u907f\u96f7\u5566-Excel\u4e0b\u8f7d",
            "endpoint": BILEILA_EXCEL_API["endpoint"],
            "target_url": _bileila_excel_url("YYYY.MM.DD"),
        },
    )
    scenarios.append(
        {
            "session_id": bileila_session_id,
            "title": "BiLeiLa Excel Download",
            "title_cn": "\u907f\u96f7\u5566-Excel\u4e0b\u8f7d",
            "added_time": "2026-07-06",
            "maintenance_time": "2026-07-06",
            "level": bileila_level,
            "level_label": SCENARIO_LEVELS[bileila_level],
            "group": BILEILA_GROUP,
            "risk_level": bileila_policy["risk_level"],
            "call_policy": bileila_policy["call_policy"],
            "call_disabled": bileila_policy["call_disabled"],
            "risk_reason": bileila_policy["risk_reason"],
            "cache_ttl": 0,
            "method_name": BILEILA_EXCEL_API["name"],
            "http_method": "GET",
            "target_url": _bileila_excel_url("YYYY.MM.DD"),
            "endpoint": BILEILA_EXCEL_API["endpoint"],
            "alias_endpoint": BILEILA_EXCEL_API["alias_endpoint"],
            "params": {"date": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d"), "force": "0"},
            "url_params": ["date", "day", "Day", "force"],
            "data": {},
            "source": "appcdn.longhuvip.com/BiLeiLa",
            "is_local": True,
            "local_name": BILEILA_EXCEL_API["name"],
            "hide_url_fields": [],
        }
    )
    return scenarios


SCENARIOS: list[dict[str, object]] = []
ROUTES: dict[str, dict[str, object]] = {}


def _refresh_routes() -> None:
    global SCENARIOS, ROUTES
    SCENARIOS = _build_scenarios()
    ROUTES = {}
    for scenario, spec in zip(SCENARIOS, REQUESTS):
        ROUTES[scenario["endpoint"]] = {"scenario": scenario, "spec": spec}
        ROUTES[scenario["alias_endpoint"]] = {"scenario": scenario, "spec": spec}
    for scenario in SCENARIOS[len(REQUESTS) :]:
        copy_of_endpoint = scenario.get("copy_of_endpoint")
        if copy_of_endpoint:
            source_route = ROUTES.get(str(copy_of_endpoint))
            if source_route and source_route.get("spec"):
                ROUTES[scenario["endpoint"]] = {"scenario": scenario, "spec": source_route["spec"]}
                ROUTES[scenario["alias_endpoint"]] = {"scenario": scenario, "spec": source_route["spec"]}
            continue
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

        if path == "/api/health":
            self._send_json(
                {
                    "ok": True,
                    "service": "KaipanlaScenarioAPI",
                    "scenarios": len(SCENARIOS),
                    "time": datetime.now(BEIJING_TZ).isoformat(timespec="seconds"),
                }
            )
            return

        if path in {f"/{LOGIN_FILE}", "/login"}:
            self._serve_file(ROOT / LOGIN_FILE, "text/html; charset=utf-8")
            return

        if path in {f"/{REGISTER_FILE}", "/register"}:
            self._serve_file(ROOT / REGISTER_FILE, "text/html; charset=utf-8")
            return

        if path in {f"/{EXPIRED_FILE}", "/expired"}:
            self._serve_file(ROOT / EXPIRED_FILE, "text/html; charset=utf-8")
            return

        if path in {f"/{CHANGE_PASSWORD_FILE}", "/change-password"}:
            self._serve_file(ROOT / CHANGE_PASSWORD_FILE, "text/html; charset=utf-8")
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
            visible_scenarios = (
                SCENARIOS
                if user.get("role") == "admin"
                else [
                    item
                    for item in SCENARIOS
                    if not _is_system_config_scenario(item) and not _is_pending_delete_scenario(item)
                ]
            )
            visible_scenarios = _sort_scenarios_for_display(list(visible_scenarios))
            self._send_json(
                {
                    "count": len(visible_scenarios),
                    "scenarios": visible_scenarios,
                    "level_options": [
                        {"value": value, "label": label}
                        for value, label in SCENARIO_LEVELS.items()
                    ],
                    "user": user,
                }
            )
            return

        if (
            path == "/api/topic"
            or path.startswith("/api/topic/")
            or path in {TOPIC_RANK_API["alias_endpoint"], TOPIC_TABLE_API["alias_endpoint"]}
        ):
            user, error = self._require_interface_or_session_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_topic_rank_api(user, path)
            return

        if path.startswith("/api/topic-library"):
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_topic_library_api(path)
            return

        if path in {
            BILEILA_EXCEL_API["endpoint"],
            BILEILA_EXCEL_API["alias_endpoint"],
            BILEILA_EXCEL_API["download_endpoint"],
        }:
            user, error = self._require_interface_or_session_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_bileila_excel_api(user, path)
            return

        if path == "/api/core" or path.startswith("/api/core/"):
            user, error = self._require_interface_or_session_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_core_api(user, path)
            return

        if path == "/api/hq" or path.startswith("/api/hq/"):
            user, error = self._require_interface_or_session_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_hq_api(user, path)
            return

        if path in ROUTES:
            if path == "/api/stock_getnewestday" and self._interface_api_key():
                user, error = self._require_api_key_user()
                if error:
                    self._send_json(
                        {"error": error, "message": error, "auth_error": True},
                        status=self._auth_failure_status(error),
                    )
                    return
                route = ROUTES[path]
                query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
                body_values = self._read_body_values()
                overrides = {**query_values, **body_values}
                overrides.pop("_ts", None)
                for key in LEGACY_INTERFACE_API_KEY_FIELDS:
                    overrides.pop(key, None)
                self._call_stock_getnewestday_api_key(user, route["scenario"], route["spec"], overrides)
                return
            user, error = self._require_interface_or_session_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            if self.command not in {"GET", "POST"}:
                self._send_json({"error": "method_not_allowed"}, status=405)
                return
            route = ROUTES[path]
            if user.get("role") != "admin" and _is_pending_delete_scenario(route["scenario"]):
                self._send_json({"error": "forbidden", "message": "Admin role required"}, status=403)
                return
            if user.get("role") != "admin" and route["scenario"].get("call_disabled"):
                self._send_json({"error": "forbidden", "message": "High-risk interface is admin only"}, status=403)
                return
            query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
            body_values = self._read_body_values()
            overrides = {**query_values, **body_values}
            overrides.pop("_ts", None)
            if not self._validate_interface_api_key(user):
                return
            for key in LEGACY_INTERFACE_API_KEY_FIELDS:
                overrides.pop(key, None)
            overrides = _normalized_scene_overrides(route["spec"], overrides)
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

        for key, value in overrides.items():
            if key in params and key not in data:
                params[key] = value
            else:
                data[key] = value
        identity = _current_upstream_identity()
        _apply_upstream_identity(data, identity)
        params["_ts"] = str(int(requested_at * 1000))
        request_log = _request_log_payload(
            spec.get("method", ""),
            spec.get("url", ""),
            spec.get("headers", {}),
            params,
            data,
            overrides,
        )
        host = host_from_url(spec.get("url"))
        endpoint = str(scenario.get("endpoint") or "")
        cache_ttl = _cache_ttl_for_scenario(scenario)
        cache_key = stable_cache_key(spec.get("method"), spec.get("url"), params, data, endpoint)
        cached = UPSTREAM_GUARD.cache_get(cache_key) if cache_ttl else None
        if cached:
            payload, cache_info = cached
            _append_call_log(
                {
                    "requested_at": requested_at,
                    "requested_at_text": started_iso,
                    "username": user.get("username", ""),
                    "role": user.get("role", ""),
                    "session_id": scenario.get("session_id", ""),
                    "title": scenario.get("title", ""),
                    "title_cn": scenario.get("title_cn", ""),
                    "endpoint": endpoint,
                    "target_url": scenario.get("target_url", spec.get("url", "")),
                    "http_method": scenario.get("http_method", spec.get("method", "")),
                    "status": "ok",
                    "status_code": cache_info.get("status_code", 200),
                    "duration_ms": int((time.time() - requested_at) * 1000),
                    "content_type": cache_info.get("content_type", "application/json"),
                    "overrides": _safe_log_values(overrides),
                    "request": request_log,
                    "response": None,
                    "cache": cache_info,
                    "risk_level": scenario.get("risk_level", ""),
                    "call_policy": scenario.get("call_policy", ""),
                }
            )
            if _is_body_only_market_scenario(scenario):
                self._send_json(payload)
                return
            if _is_theme_infogr_scenario(scenario):
                self._send_json(_dataframe_payload(payload))
                return
            if scenario.get("stock_newestday_body_only"):
                self._send_json(_dataframe_payload(_stock_newestday_payload(payload)))
                return
            response_body = _stock_newestday_payload(payload) if _is_stock_getnewestday_scenario(scenario) else payload
            self._send_json(
                {
                    "requested_at": requested_at,
                    "status_code": cache_info.get("status_code", 200),
                    "content_type": cache_info.get("content_type", "application/json"),
                    "body": response_body,
                    "upstream_error": "",
                    "cache": cache_info,
                    "upstream_relogin_attempted": False,
                    "upstream_relogin_succeeded": False,
                }
            )
            return

        try:
            guard_info = UPSTREAM_GUARD.before_request(host, endpoint)
        except (UpstreamCircuitOpen, UpstreamRateLimited) as exc:
            payload, status = _guard_error_payload(exc, requested_at)
            _append_call_log(
                {
                    "requested_at": requested_at,
                    "requested_at_text": started_iso,
                    "username": user.get("username", ""),
                    "role": user.get("role", ""),
                    "session_id": scenario.get("session_id", ""),
                    "title": scenario.get("title", ""),
                    "title_cn": scenario.get("title_cn", ""),
                    "endpoint": endpoint,
                    "target_url": scenario.get("target_url", spec.get("url", "")),
                    "http_method": scenario.get("http_method", spec.get("method", "")),
                    "status": payload["error"],
                    "status_code": status,
                    "duration_ms": int((time.time() - requested_at) * 1000),
                    "overrides": _safe_log_values(overrides),
                    "request": request_log,
                    "response": None,
                    "cache": {"hit": False},
                    "risk_level": scenario.get("risk_level", ""),
                    "call_policy": scenario.get("call_policy", ""),
                    "retry_after": payload.get("retry_after"),
                }
            )
            self._send_json(payload, status=status)
            return

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
                    "request": request_log,
                    "response": None,
                    "cache": {"hit": False},
                    "guard": guard_info,
                    "risk_level": scenario.get("risk_level", ""),
                    "call_policy": scenario.get("call_policy", ""),
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
        relogin_attempted = False
        relogin_succeeded = False
        if _is_upstream_auth_error(payload):
            refreshed_identity = _current_upstream_identity(force=True)
            if refreshed_identity and refreshed_identity != identity:
                identity = refreshed_identity
                retry_data = dict(data)
                for key, value in identity.items():
                    retry_data[key] = value
                retry_params = dict(params)
                retry_params["_ts"] = str(int(time.time() * 1000))
                relogin_attempted = True
                try:
                    response = client.request(spec, data=retry_data, params=retry_params)
                    data = retry_data
                    params = retry_params
                    request_log = _request_log_payload(
                        spec.get("method", ""),
                        spec.get("url", ""),
                        spec.get("headers", {}),
                        params,
                        data,
                        overrides,
                    )
                    content_type = response.headers.get("Content-Type", "")
                    try:
                        payload = response.json()
                    except ValueError:
                        payload = response.text
                    relogin_succeeded = not _is_upstream_auth_error(payload)
                except Exception:
                    pass
        upstream_error = "" if response.ok else f"upstream HTTP {response.status_code}"
        upstream_body_error = _upstream_error_message(payload)
        if upstream_body_error:
            upstream_error = upstream_body_error
        guard_result = UPSTREAM_GUARD.record_result(host, endpoint, payload, upstream_error)
        if not upstream_error and _is_non_data_response_body(payload):
            _mark_scenario_pending_delete(scenario.get("session_id", ""))
        if not upstream_error:
            UPSTREAM_GUARD.cache_set(cache_key, payload, content_type, response.status_code, cache_ttl)

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
                "status": "ok" if not upstream_error else "upstream_error",
                "status_code": response.status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "content_type": content_type,
                "overrides": _safe_log_values(overrides),
                "request": request_log,
                "response": _response_log_payload(response, payload),
                "cache": {"hit": False, "ttl": cache_ttl},
                "guard": {**guard_info, **guard_result},
                "risk_level": scenario.get("risk_level", ""),
                "call_policy": scenario.get("call_policy", ""),
                "upstream_relogin_attempted": relogin_attempted,
                "upstream_relogin_succeeded": relogin_succeeded,
            }
        )

        if not upstream_error and _is_body_only_market_scenario(scenario):
            self._send_json(payload)
            return

        if not upstream_error and _is_theme_infogr_scenario(scenario):
            self._send_json(_dataframe_payload(payload))
            return

        if not upstream_error and scenario.get("stock_newestday_body_only"):
            self._send_json(_dataframe_payload(_stock_newestday_payload(payload)))
            return

        response_body = _stock_newestday_payload(payload) if not upstream_error and _is_stock_getnewestday_scenario(scenario) else payload
        self._send_json(
            {
                "requested_at": requested_at,
                "status_code": response.status_code,
                "content_type": content_type,
                "body": response_body,
                "upstream_error": upstream_error,
                "cache": {"hit": False, "ttl": cache_ttl},
                "upstream_relogin_attempted": relogin_attempted,
                "upstream_relogin_succeeded": relogin_succeeded,
            }
            if not upstream_error
            else {
                "error": "upstream_error",
                "message": upstream_error,
                "requested_at": requested_at,
                "status_code": response.status_code,
                "content_type": content_type,
                "body": payload,
                "cache": {"hit": False, "ttl": cache_ttl},
                "upstream_relogin_attempted": relogin_attempted,
                "upstream_relogin_succeeded": relogin_succeeded,
            },
            status=200 if not upstream_error else 502,
        )

    def _call_stock_getnewestday_api_key(
        self,
        user: dict[str, object],
        scenario: dict[str, object],
        spec: dict[str, object],
        overrides: dict[str, str],
    ) -> None:
        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        client = KaipanlaCapturedClient()
        client.session.trust_env = False
        data = dict(spec.get("data") or {})
        params = dict(spec.get("params") or {})
        for key, value in overrides.items():
            if key in params and key not in data:
                params[key] = value
            else:
                data[key] = value
        identity = _current_upstream_identity()
        _apply_upstream_identity(data, identity)
        params["_ts"] = str(int(requested_at * 1000))
        request_log = _request_log_payload(spec.get("method", ""), spec.get("url", ""), spec.get("headers", {}), params, data, overrides)
        host = host_from_url(spec.get("url"))
        endpoint = str(scenario.get("endpoint") or "")
        cache_ttl = _cache_ttl_for_scenario(scenario) or 5
        cache_key = stable_cache_key(spec.get("method"), spec.get("url"), params, data, endpoint)
        cached = UPSTREAM_GUARD.cache_get(cache_key)
        if cached:
            payload, cache_info = cached
            body = _stock_newestday_payload(payload)
            self._send_json({**body, "cache": cache_info} if isinstance(body, dict) else body)
            return
        try:
            guard_info = UPSTREAM_GUARD.before_request(host, endpoint)
        except (UpstreamCircuitOpen, UpstreamRateLimited) as exc:
            payload, status = _guard_error_payload(exc, requested_at)
            self._send_json(payload, status=status)
            return
        try:
            response = client.request(spec, data=data, params=params)
            content_type = response.headers.get("Content-Type", "")
            try:
                payload: object = response.json()
            except ValueError:
                payload = response.text
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
                    "http_method": self.command,
                    "status": "failed",
                    "status_code": 502,
                    "duration_ms": int((time.time() - requested_at) * 1000),
                    "overrides": _safe_log_values(overrides),
                    "request": request_log,
                    "response": None,
                    "cache": {"hit": False},
                    "guard": guard_info,
                    "error": str(exc),
                }
            )
            self._send_json({"error": "upstream_request_failed", "message": str(exc)}, status=502)
            return

        upstream_error = "" if response.ok else f"upstream HTTP {response.status_code}"
        upstream_body_error = _upstream_error_message(payload)
        if upstream_body_error:
            upstream_error = upstream_body_error
        guard_result = UPSTREAM_GUARD.record_result(host, endpoint, payload, upstream_error)
        if not upstream_error:
            UPSTREAM_GUARD.cache_set(cache_key, payload, content_type, response.status_code, cache_ttl)
        body = _stock_newestday_payload(payload)
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
                "http_method": self.command,
                "status": "ok" if not upstream_error else "upstream_error",
                "status_code": response.status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "content_type": content_type,
                "overrides": _safe_log_values(overrides),
                "request": request_log,
                "response": _response_log_payload(response, payload),
                "cache": {"hit": False, "ttl": cache_ttl},
                "guard": {**guard_info, **guard_result},
            }
        )
        self._send_json(
            {**body, "cache": {"hit": False, "ttl": cache_ttl}}
            if not upstream_error and isinstance(body, dict)
            else {"error": "upstream_error", "message": upstream_error, "body": body, "cache": {"hit": False, "ttl": cache_ttl}},
            status=200 if not upstream_error else 502,
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
                self._send_json(
                    {"error": error, "message": error, "user": user, "auth_error": True},
                    status=status,
                    extra_headers=headers,
                )
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
                    {"error": error, "message": error, "user": user, "auth_error": True},
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

        if path == "/api/auth/change-password" and self.command == "POST":
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            payload = self._read_json_body()
            old_password = str(payload.get("old_password", ""))
            new_password = str(payload.get("new_password", ""))
            confirm_password = str(payload.get("confirm_password", new_password))
            if not old_password or not new_password:
                self._send_json({"error": "invalid_request", "message": "old_password and new_password are required"}, status=400)
                return
            if new_password != confirm_password:
                self._send_json({"error": "invalid_request", "message": "new passwords do not match"}, status=400)
                return
            if len(new_password) < 6:
                self._send_json({"error": "invalid_request", "message": "password must be at least 6 chars"}, status=400)
                return
            try:
                result = AUTH.change_password(str(user["username"]), old_password, new_password)
            except ValueError as exc:
                self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
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
                            "group": scenario.get("group", ""),
                            "endpoint": scenario["endpoint"],
                            "target_url": scenario["target_url"],
                        }
                        for scenario in _sort_scenarios_for_display(SCENARIOS)
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
            user_path = path[len(prefix) :]
            if user_path.endswith("/reset-password"):
                username = unquote(user_path[: -len("/reset-password")])
                if self.command in {"POST", "PATCH"}:
                    try:
                        user = AUTH.reset_user_password(username)
                    except KeyError as exc:
                        self._send_json({"error": "not_found", "message": str(exc)}, status=404)
                        return
                    except ValueError as exc:
                        self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                        return
                    self._send_json({"user": user, "password": "Kpl@13579"})
                    return
            if user_path.endswith("/activation-code"):
                username = unquote(user_path[: -len("/activation-code")])
                if self.command in {"PUT", "PATCH", "POST"}:
                    try:
                        user = AUTH.assign_activation_code_to_user(username, str(self._read_json_body().get("code", "")))
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
                        user = AUTH.remove_user_activation_code(username)
                    except KeyError as exc:
                        self._send_json({"error": "not_found", "message": str(exc)}, status=404)
                        return
                    except ValueError as exc:
                        self._send_json({"error": "invalid_request", "message": str(exc)}, status=400)
                        return
                    self._send_json({"user": user})
                    return
            username = unquote(user_path)
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

    def _handle_bileila_excel_api(self, user: dict[str, object], path: str) -> None:
        if self.command not in {"GET", "POST"}:
            self._send_json({"error": "method_not_allowed"}, status=405)
            return
        parsed = urlparse(self.path)
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values()
        values = {**query_values, **body_values}
        values.pop("_ts", None)
        if not self._validate_interface_api_key(user):
            return
        for key in LEGACY_INTERFACE_API_KEY_FIELDS:
            values.pop(key, None)

        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at, BEIJING_TZ).isoformat(timespec="seconds")
        force = str(values.get("force") or values.get("refresh") or "").strip().lower() in {"1", "true", "yes", "y"}
        day_value = values.get("date") or values.get("day") or values.get("Day")
        try:
            result = _load_bileila_excel(day_value, force=force)
            status_code = 200
            error_message = ""
        except (RuntimeError, ValueError, zipfile.BadZipFile) as exc:
            result = {}
            status_code = 502 if isinstance(exc, RuntimeError) else 400
            error_message = str(exc)

        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": "bileila:excel",
                "title": "BiLeiLa Excel Download",
                "title_cn": "\u907f\u96f7\u5566-Excel\u4e0b\u8f7d",
                "endpoint": BILEILA_EXCEL_API["endpoint"],
                "target_url": result.get("source_url") or _bileila_excel_url("YYYY.MM.DD"),
                "http_method": self.command,
                "status": "ok" if not error_message else "error",
                "status_code": status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(values),
                "request": {
                    "date": day_value or "",
                    "force": force,
                    "source": "appcdn.longhuvip.com/BiLeiLa",
                },
                "response": {
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "body": {
                        "sheet_count": len(result.get("sheets", [])) if result else 0,
                        "stock_code_count": len(result.get("stock_codes", [])) if result else 0,
                    },
                },
                "error": error_message,
            }
        )
        if error_message:
            self._send_json({"error": "bileila_excel_failed", "message": error_message}, status=status_code)
            return
        if path == BILEILA_EXCEL_API["download_endpoint"]:
            self._serve_file(
                Path(str(result["cached_path"])),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            return
        self._send_json(
            {
                "requested_at": requested_at,
                "bileila_api": BILEILA_EXCEL_API,
                "date": result["date"],
                "source_url": result["source_url"],
                "download_endpoint": result["download_endpoint"],
                "cached_path": result["cached_path"],
                "from_cache": result["from_cache"],
                "file_size": result["file_size"],
                "body": {
                    "sheets": result["sheets"],
                    "stock_codes": result["stock_codes"],
                    "stock_code_count": len(result["stock_codes"]),
                },
            }
        )

    def _handle_topic_rank_api(self, user: dict[str, object], path: str) -> None:
        if self.command not in {"GET", "POST"}:
            self._send_json({"error": "method_not_allowed"}, status=405)
            return
        if path == "/api/topic":
            self._send_json(
                {
                    "apis": [
                        {
                            "name": TOPIC_RANK_API["name"],
                            "source": TOPIC_RANK_API["source"],
                            "packet_code": TOPIC_RANK_API["packet_code"],
                            "endpoint": TOPIC_RANK_API["endpoint"],
                            "alias_endpoint": TOPIC_RANK_API["alias_endpoint"],
                            "description": TOPIC_RANK_API["description"],
                        },
                        {
                            "name": TOPIC_TABLE_API["name"],
                            "source": TOPIC_TABLE_API["source"],
                            "packet_code": TOPIC_TABLE_API["packet_code"],
                            "endpoint": TOPIC_TABLE_API["endpoint"],
                            "alias_endpoint": TOPIC_TABLE_API["alias_endpoint"],
                            "description": TOPIC_TABLE_API["description"],
                        },
                    ],
                    "log": str(TOPIC_RANK_LOG),
                }
            )
            return
        if path in {TOPIC_TABLE_API["endpoint"], TOPIC_TABLE_API["alias_endpoint"]}:
            self._handle_topic_table_content_api(user, path)
            return
        if path not in {TOPIC_RANK_API["endpoint"], TOPIC_RANK_API["alias_endpoint"]}:
            self._send_json({"error": "not_found", "message": f"unknown topic api: {path}"}, status=404)
            return

        parsed = urlparse(self.path)
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values()
        values = {**query_values, **body_values}
        if not self._validate_interface_api_key(user):
            return
        for key in LEGACY_INTERFACE_API_KEY_FIELDS:
            values.pop(key, None)
        day = normalize_topic_rank_day(values.get("date") or values.get("day") or values.get("Day"))
        try:
            limit = int(values.get("limit", "0") or "0")
        except ValueError:
            limit = 0
        limit = max(0, min(limit, 1000))

        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        result = latest_topic_rank_list(day=day, limit=limit or None)
        status_code = 200 if result else 404
        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": "topic_rank:3009",
                "title": "global.3009 Topic Rank List",
                "title_cn": "\u9898\u6750\u5e93-\u6bcf\u65e5\u699c\u5355\u5217\u8868",
                "endpoint": TOPIC_RANK_API["endpoint"],
                "target_url": str(TOPIC_RANK_LOG),
                "http_method": self.command,
                "status": "ok" if result else "not_found",
                "status_code": status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(values),
                "request": {
                    "source": TOPIC_RANK_API["source"],
                    "route": "global|26:20020/3009-0/",
                    "date": day,
                    "limit": limit,
                },
                "response": {
                    "content_type": "application/json",
                    "body": {"count": result.get("count") if result else 0},
                },
                "error": "" if result else "topic rank packet not found",
            }
        )
        if not result:
            self._send_json(
                {
                    "error": "not_found",
                    "message": "No topic rank packet found for requested date.",
                    "date": day,
                    "available_dates": available_topic_rank_days(),
                    "source_log": str(TOPIC_RANK_LOG),
                },
                status=404,
            )
            return
        self._send_json(
            {
                "requested_at": requested_at,
                "topic_api": TOPIC_RANK_API,
                "date": result.get("day"),
                "source_log": str(TOPIC_RANK_LOG),
                "body": result,
            }
        )

    def _handle_topic_table_content_api(self, user: dict[str, object], path: str) -> None:
        parsed = urlparse(self.path)
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values()
        values = {**query_values, **body_values}
        if not self._validate_interface_api_key(user):
            return
        for key in LEGACY_INTERFACE_API_KEY_FIELDS:
            values.pop(key, None)
        topic_id = str(
            values.get("topic_id")
            or values.get("id")
            or values.get("ID")
            or values.get("TopicID")
            or ""
        ).strip()
        if not topic_id:
            self._send_json({"error": "missing_topic_id", "message": "Pass topic_id=395"}, status=400)
            return
        day = normalize_topic_rank_day(values.get("date") or values.get("day") or values.get("Day"))
        try:
            limit = int(values.get("limit", "0") or "0")
        except ValueError:
            limit = 0
        limit = max(0, min(limit, 1000))

        requested_at = time.time()
        started_iso = datetime.fromtimestamp(requested_at).isoformat(timespec="seconds")
        result = latest_topic_table_content(topic_id, day=day, limit=limit or None)
        status_code = 200 if result else 404
        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": "topic_table:3010",
                "title": "global.3010 Topic Table Content",
                "title_cn": "\u9898\u6750\u5e93-\u5c0f\u8868\u683c\u5185\u5bb9",
                "endpoint": TOPIC_TABLE_API["endpoint"],
                "target_url": str(TOPIC_RANK_LOG),
                "http_method": self.command,
                "status": "ok" if result else "not_found",
                "status_code": status_code,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(values),
                "request": {
                    "source": TOPIC_TABLE_API["source"],
                    "route": f"global|26:20020/3010-0/{topic_id}",
                    "topic_id": topic_id,
                    "date": day,
                    "limit": limit,
                },
                "response": {
                    "content_type": "application/json",
                    "body": {"count": (result.get("body") or {}).get("count") if result else 0},
                },
                "error": "" if result else "topic table packet not found",
            }
        )
        if not result:
            self._send_json(
                {
                    "error": "not_found",
                    "message": "No topic small-table packet found for requested topic/date.",
                    "topic_id": topic_id,
                    "date": day,
                    "available_topics": available_topic_table_topics(),
                    "source_log": str(TOPIC_RANK_LOG),
                },
                status=404,
            )
            return
        self._send_json(
            {
                "requested_at": requested_at,
                "topic_api": TOPIC_TABLE_API,
                "topic_id": topic_id,
                "date": result.get("day"),
                "source_log": str(TOPIC_RANK_LOG),
                "body": result,
            }
        )

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
        request_log: dict[str, object] | None = None
        response_log: dict[str, object] | None = None
        error_message = ""
        if name == "five_level":
            packet_code = "2015"
            try:
                result, upstream_response, upstream_body = _fetch_online_five_level(stock_id, values)
                request_log = _request_log_payload(
                    "POST",
                    "https://apphwhq.longhuvip.com/w1/api/index.php",
                    {},
                    {},
                    {"c": "StockL2Data", "a": "GetWeiTuo", "StockID": stock_id},
                    values,
                )
                response_log = _response_log_payload(upstream_response, upstream_body)
            except Exception as exc:
                error_message = str(exc)
                result = latest_five_level(stock_id)
            not_found_payload = _hq_not_found_payload(packet_code, "five-level", stock_id)
            if error_message:
                not_found_payload["online_error"] = error_message
        else:
            try:
                limit = max(1, min(1000, int(values.get("limit", "100"))))
            except ValueError:
                limit = 100
            packet_code = "2006"
            try:
                result, upstream_response, upstream_body = _fetch_online_time_sales(stock_id, values, limit=limit)
                request_log = _request_log_payload(
                    "POST",
                    "https://apphwhq.longhuvip.com/w1/api/index.php",
                    {},
                    {},
                    {"c": "StockL2Data", "a": "GetWeiTuo", "StockID": stock_id},
                    values,
                )
                response_log = _response_log_payload(upstream_response, upstream_body)
            except Exception as exc:
                error_message = str(exc)
                result = latest_time_sales(stock_id, limit=limit)
            not_found_payload = _hq_not_found_payload(packet_code, "time-sales", stock_id)
            if error_message:
                not_found_payload["online_error"] = error_message
        _append_call_log(
            {
                "requested_at": requested_at,
                "requested_at_text": started_iso,
                "username": user.get("username", ""),
                "role": user.get("role", ""),
                "session_id": f"hq:{name}",
                "title": f"hqStock.{packet_code}",
                "title_cn": "五档行情" if name == "five_level" else "分时成交",
                "endpoint": f"/api/hq/{name}",
                "target_url": response_log["url"] if response_log else str(HQSTOCK_LOG),
                "http_method": self.command,
                "status": "ok" if result else "not_found",
                "status_code": 200 if result else 404,
                "duration_ms": int((time.time() - requested_at) * 1000),
                "overrides": _safe_log_values(values),
                "request": request_log,
                "response": response_log,
                "error": error_message,
            }
        )
        if not result:
            self._send_json(not_found_payload, status=404)
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
        request_log: dict[str, object] | None = None
        response_log: dict[str, object] | None = None
        error_message = ""
        if name == "five_level":
            packet_code = "2015"
            try:
                result, upstream_response, upstream_body = _fetch_online_five_level(stock_id, overrides)
                request_log = _request_log_payload(
                    "POST",
                    "https://apphwhq.longhuvip.com/w1/api/index.php",
                    {},
                    {},
                    {"c": "StockL2Data", "a": "GetWeiTuo", "StockID": stock_id},
                    overrides,
                )
                response_log = _response_log_payload(upstream_response, upstream_body)
            except Exception as exc:
                error_message = str(exc)
                result = latest_five_level(stock_id)
            not_found_payload = _hq_not_found_payload(packet_code, "five-level", stock_id)
            if error_message:
                not_found_payload["online_error"] = error_message
        elif name == "time_sales":
            try:
                limit = max(1, min(1000, int(overrides.get("limit", "100"))))
            except ValueError:
                limit = 100
            packet_code = "2006"
            try:
                result, upstream_response, upstream_body = _fetch_online_time_sales(stock_id, overrides, limit=limit)
                request_log = _request_log_payload(
                    "POST",
                    "https://apphwhq.longhuvip.com/w1/api/index.php",
                    {},
                    {},
                    {"c": "StockL2Data", "a": "GetWeiTuo", "StockID": stock_id},
                    overrides,
                )
                response_log = _response_log_payload(upstream_response, upstream_body)
            except Exception as exc:
                error_message = str(exc)
                result = latest_time_sales(stock_id, limit=limit)
            not_found_payload = _hq_not_found_payload(packet_code, "time-sales", stock_id)
            if error_message:
                not_found_payload["online_error"] = error_message
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
                "request": request_log,
                "response": response_log,
                "error": error_message,
            }
        )
        if not result:
            self._send_json(not_found_payload, status=404)
            return
        self._send_json(
            {
                "requested_at": requested_at,
                "status_code": 200,
                "content_type": "application/json",
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
        request_log = _request_log_payload(
            "POST",
            f"https://{host}/w1/api/index.php",
            {},
            {},
            {"controller": controller, "action": action, **overrides},
            overrides,
        )
        identity = _current_upstream_identity()
        core_overrides = {**identity, **overrides}
        endpoint = f"/api/core/{name}"
        cache_ttl = 5
        cache_key = stable_cache_key("CORE", name, core_overrides, endpoint)
        cached = UPSTREAM_GUARD.cache_get(cache_key)
        if cached:
            body, cache_info = cached
            self._send_json(
                {
                    "requested_at": requested_at,
                    "status_code": cache_info.get("status_code", 200),
                    "content_type": cache_info.get("content_type", "application/json"),
                    "core_api": {
                        "name": name,
                        "host": host,
                        "controller": controller,
                        "action": action,
                    },
                    "body": body,
                    "cache": cache_info,
                    "upstream_relogin_attempted": False,
                    "upstream_relogin_succeeded": False,
                }
            )
            return
        try:
            guard_info = UPSTREAM_GUARD.before_request(host, endpoint)
        except (UpstreamCircuitOpen, UpstreamRateLimited) as exc:
            payload, status = _guard_error_payload(exc, requested_at)
            self._send_json(payload, status=status)
            return
        try:
            response = client.request_core(name, **core_overrides)
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
                    "request": request_log,
                    "response": None,
                    "cache": {"hit": False},
                    "guard": guard_info,
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
        relogin_attempted = False
        relogin_succeeded = False
        if _is_upstream_auth_error(body):
            refreshed_identity = _current_upstream_identity(force=True)
            if refreshed_identity and refreshed_identity != identity:
                identity = refreshed_identity
                core_overrides = {**identity, **overrides}
                relogin_attempted = True
                try:
                    response = client.request_core(name, **core_overrides)
                    duration_ms = int((time.time() - requested_at) * 1000)
                    content_type = response.headers.get("Content-Type", "")
                    try:
                        body = response.json()
                    except ValueError:
                        body = response.text
                    relogin_succeeded = not _is_upstream_auth_error(body)
                except Exception:
                    pass
        upstream_error = "" if response.ok else f"upstream HTTP {response.status_code}"
        upstream_body_error = _upstream_error_message(body)
        if upstream_body_error:
            upstream_error = upstream_body_error
        guard_result = UPSTREAM_GUARD.record_result(host, endpoint, body, upstream_error)
        if not upstream_error:
            UPSTREAM_GUARD.cache_set(cache_key, body, content_type, response.status_code, cache_ttl)

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
                "status": "ok" if not upstream_error else "upstream_error",
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "overrides": _safe_log_values(overrides),
                "request": request_log,
                "response": _response_log_payload(response, body),
                "cache": {"hit": False, "ttl": cache_ttl},
                "guard": {**guard_info, **guard_result},
                "upstream_relogin_attempted": relogin_attempted,
                "upstream_relogin_succeeded": relogin_succeeded,
            }
        )
        self._send_json(
            (
                {
                    "requested_at": requested_at,
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "core_api": {
                        "name": name,
                        "host": host,
                        "controller": controller,
                        "action": action,
                    },
                    "body": body,
                    "cache": {"hit": False, "ttl": cache_ttl},
                    "upstream_relogin_attempted": relogin_attempted,
                    "upstream_relogin_succeeded": relogin_succeeded,
                }
                if not upstream_error
                else {
                    "error": "upstream_error",
                    "message": upstream_error,
                    "requested_at": requested_at,
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "core_api": {
                        "name": name,
                        "host": host,
                        "controller": controller,
                        "action": action,
                    },
                    "body": body,
                    "cache": {"hit": False, "ttl": cache_ttl},
                    "upstream_relogin_attempted": relogin_attempted,
                    "upstream_relogin_succeeded": relogin_succeeded,
                }
            ),
            status=200 if not upstream_error else 502,
        )

    def _require_user(self) -> tuple[dict[str, object] | None, str | None]:
        return AUTH.session_user(self._session_token())

    def _require_api_key_user(self) -> tuple[dict[str, object] | None, str | None]:
        return AUTH.user_for_interface_credentials(
            str(self.headers.get("x-username") or ""),
            str(self.headers.get("x-password") or ""),
            self._interface_api_key(),
        )

    def _require_interface_or_session_user(self) -> tuple[dict[str, object] | None, str | None]:
        if self._interface_api_key():
            return self._require_api_key_user()
        return self._require_user()

    def _interface_api_key(self) -> str:
        return str(self.headers.get(INTERFACE_API_KEY_HEADER) or "").strip()

    def _validate_interface_api_key(self, user: dict[str, object]) -> bool:
        ok, error = AUTH.validate_interface_user_activation(
            str(user.get("username", "")),
            str(user.get("role", "")),
        )
        if ok:
            return True
        self._send_json(
            {
                "error": error or "invalid_activation_code",
                "message": "\u5f53\u524d\u8d26\u53f7\u672a\u7ed1\u5b9a\u6709\u6548\u6fc0\u6d3b\u7801\uff0c\u65e0\u6cd5\u8c03\u7528\u63a5\u53e3",
            },
            status=403,
        )
        return False

    def _auth_failure_status(self, error: str) -> int:
        if error in {"disabled", "expired", "activation_code_disabled", "activation_code_not_bound_to_user"}:
            return 403
        return 401

    def _send_auth_failure(self, error: str, json_response: bool) -> None:
        if json_response:
            self._send_json(
                {"error": error, "message": error, "auth_error": True},
                status=self._auth_failure_status(error),
            )
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
        payload = _with_beijing_time_fields(payload)
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
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, X-API-Key, x-api-key, Authorization, activation_code, api_activation_code",
        )


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
