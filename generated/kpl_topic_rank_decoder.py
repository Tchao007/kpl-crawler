# -*- coding: utf-8 -*-
"""Decode Kaipanla topic-rank packets captured by Frida."""

from __future__ import annotations

import json
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_LOG = Path(__file__).resolve().parent.parent / "outputs" / "frida" / "kpl_capture.ndjson"
BEIJING_TZ = timezone(timedelta(hours=8))
TOPIC_RANK_ROUTE = b"global|26:20020/3009-0/"
TOPIC_TABLE_ROUTE_PREFIX = b"global|26:20020/3010-0/"

TOPIC_RANK_API = {
    "name": "topic_rank_list",
    "source": "global",
    "packet_code": "3009",
    "endpoint": "/api/topic/rank-list",
    "alias_endpoint": "/api/topic-library/rank-list",
    "description": "Decode latest daily topic-library rank list from captured global 20020/3009 packets.",
}

TOPIC_TABLE_API = {
    "name": "topic_table_content",
    "source": "global",
    "packet_code": "3010",
    "endpoint": "/api/topic/table-content",
    "alias_endpoint": "/api/topic-library/table-content",
    "description": "Decode topic-library small-table content from captured global 20020/3010 packets.",
}

TOPIC_TABLE_OPTION_LABELS = {
    0: "默认",
    1: "供应链",
    2: "股权相关",
    3: "同题材",
    4: "产业链",
    5: "客户相关",
    6: "供应商相关",
    7: "产品相关",
    8: "上游",
    9: "下游",
    10: "合作相关",
    11: "参股控股",
    12: "并购重组",
    13: "业务相关",
    14: "其他相关",
}


class ProtoParseError(ValueError):
    pass


def bytes_from_hex(hex_text: str) -> bytes:
    return bytes(int(x, 16) for x in hex_text.split())


def read_varint(buf: bytes, pos: int) -> tuple[int, int]:
    shift = 0
    value = 0
    while pos < len(buf):
        b = buf[pos]
        pos += 1
        value |= (b & 0x7F) << shift
        if not (b & 0x80):
            return value, pos
        shift += 7
        if shift > 70:
            break
    raise ProtoParseError("bad varint")


def _iter_proto_fields(buf: bytes):
    pos = 0
    while pos < len(buf):
        start = pos
        try:
            key, pos = read_varint(buf, pos)
        except ProtoParseError:
            break
        number = key >> 3
        wire = key & 7
        try:
            if wire == 0:
                value, pos = read_varint(buf, pos)
                yield start, number, wire, value
            elif wire == 1:
                raw = buf[pos : pos + 8]
                pos += 8
                yield start, number, wire, raw
            elif wire == 2:
                size, pos = read_varint(buf, pos)
                raw = buf[pos : pos + size]
                pos += size
                if len(raw) != size:
                    break
                yield start, number, wire, raw
            elif wire == 5:
                raw = buf[pos : pos + 4]
                pos += 4
                if len(raw) != 4:
                    break
                yield start, number, wire, raw
            else:
                break
        except (IndexError, ProtoParseError):
            break


def _decode_text(raw: bytes) -> str:
    return raw.decode("utf-8", errors="ignore")


def _decode_fixed32_float(raw: bytes) -> float | None:
    if len(raw) != 4:
        return None
    try:
        return struct.unpack("<f", raw)[0]
    except struct.error:
        return None


def _decode_child_topic(raw: bytes) -> dict[str, Any]:
    child: dict[str, Any] = {}
    for _, number, wire, value in _iter_proto_fields(raw):
        if wire == 2 and isinstance(value, bytes):
            if number == 1:
                child["id"] = _decode_text(value)
            elif number == 2:
                child["name"] = _decode_text(value)
            elif number == 3:
                child["code"] = _decode_text(value)
        elif wire == 5 and isinstance(value, bytes) and number == 4:
            child["value"] = _decode_fixed32_float(value)
    return child


def decode_topic_rank_entry(raw: bytes, rank: int) -> dict[str, Any]:
    item: dict[str, Any] = {"rank": rank}
    raw_fields: dict[str, Any] = {}
    children: list[dict[str, Any]] = []
    for _, number, wire, value in _iter_proto_fields(raw):
        key = f"f{number}"
        if wire == 0:
            raw_fields[key] = value
            if number == 5:
                item["flag"] = value
            elif number == 6:
                item["heat"] = value
            elif number == 7:
                item["type"] = value
            elif number == 8:
                item["sort_group"] = value
            elif number == 9:
                item["is_top"] = value
        elif wire == 2 and isinstance(value, bytes):
            text = _decode_text(value)
            raw_fields[key] = text
            if number == 1:
                item["id"] = text
            elif number == 2:
                item["name"] = text
            elif number == 3:
                item["subtitle"] = text
            elif number == 4:
                item["code"] = text
            elif number == 10:
                item["status"] = text
            elif number == 11:
                item["update_time"] = text
            elif number == 13:
                child = _decode_child_topic(value)
                if child:
                    children.append(child)
        elif wire == 5 and isinstance(value, bytes):
            fixed_value = _decode_fixed32_float(value)
            raw_fields[key] = fixed_value
            if number == 12:
                item["change"] = fixed_value
    if children:
        item["children"] = children
    item["raw_fields"] = raw_fields
    return item


def decode_topic_rank_body(body: bytes) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for _, number, wire, value in _iter_proto_fields(body):
        if number == 10 and wire == 2 and isinstance(value, bytes):
            items.append(decode_topic_rank_entry(value, len(items) + 1))
    return items


def _decode_table_row_payload(raw: bytes) -> dict[str, Any]:
    row: dict[str, Any] = {}
    raw_fields: dict[str, Any] = {}
    for _, number, wire, value in _iter_proto_fields(raw):
        key = f"f{number}"
        if wire == 0:
            raw_fields[key] = value
            if number == 2:
                row["option_index"] = value
                row["option_label"] = TOPIC_TABLE_OPTION_LABELS.get(value, f"维度{value}")
            elif number == 3:
                row["order"] = value
            elif number == 4:
                row["relation_type"] = value
                row["relation_label"] = TOPIC_TABLE_OPTION_LABELS.get(value, f"关系{value}")
        elif wire == 5 and isinstance(value, bytes):
            fixed_value = _decode_fixed32_float(value)
            raw_fields[key] = fixed_value
            if number == 5:
                row["change"] = fixed_value
    row["raw_fields"] = raw_fields
    return row


def decode_topic_table_row(raw: bytes, rank: int) -> dict[str, Any]:
    item: dict[str, Any] = {"rank": rank}
    raw_fields: dict[str, Any] = {}
    for _, number, wire, value in _iter_proto_fields(raw):
        key = f"f{number}"
        if wire == 0:
            raw_fields[key] = value
            if number == 1:
                item["row_id"] = str(value)
        elif wire == 2 and isinstance(value, bytes):
            raw_fields[key] = value.hex()
            if number == 2:
                item.update(_decode_table_row_payload(value))
        elif wire == 5 and isinstance(value, bytes):
            raw_fields[key] = _decode_fixed32_float(value)
    item["raw_fields"] = raw_fields
    return item


def decode_topic_table_body(body: bytes, topic_id: str) -> dict[str, Any]:
    result: dict[str, Any] = {"topic_id": topic_id, "rows": []}
    rows: list[dict[str, Any]] = []
    raw_fields: dict[str, Any] = {}
    for _, number, wire, value in _iter_proto_fields(body):
        key = f"f{number}"
        if wire == 0:
            raw_fields[key] = value
            if number == 1:
                result["topic_id"] = str(value)
            elif number == 2:
                result["total"] = value
            elif number == 3:
                result["active_count"] = value
            elif number == 4:
                result["selected_option"] = value
                result["selected_option_label"] = TOPIC_TABLE_OPTION_LABELS.get(value, f"维度{value}")
        elif wire == 2 and isinstance(value, bytes):
            raw_fields[key] = f"<{len(value)} bytes>"
            if number == 6:
                rows.append(decode_topic_table_row(value, len(rows) + 1))
        elif wire == 5 and isinstance(value, bytes):
            fixed_value = _decode_fixed32_float(value)
            raw_fields[key] = fixed_value
            if number == 5:
                result["score"] = fixed_value
    result["rows"] = rows
    result["count"] = len(rows)
    result["raw_fields"] = raw_fields
    return result


def _packet_body(raw: bytes) -> bytes | None:
    pos = raw.find(TOPIC_RANK_ROUTE)
    if pos < 0:
        return None
    return raw[pos + len(TOPIC_RANK_ROUTE) :]


def _table_packet_parts(raw: bytes) -> tuple[str, bytes] | None:
    pos = raw.find(TOPIC_TABLE_ROUTE_PREFIX)
    if pos < 0:
        return None
    topic_start = pos + len(TOPIC_TABLE_ROUTE_PREFIX)
    topic_end = topic_start
    while topic_end < len(raw) and 48 <= raw[topic_end] <= 57:
        topic_end += 1
    topic_id = raw[topic_start:topic_end].decode("ascii", errors="ignore")
    if not topic_id:
        return None
    return topic_id, raw[topic_end:]


def _parse_packet_ts(ts: object) -> tuple[str, str]:
    if not isinstance(ts, str) or not ts:
        now = datetime.now(BEIJING_TZ)
    else:
        text = ts.replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            parsed = datetime.now(timezone.utc)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        now = parsed.astimezone(BEIJING_TZ)
    return now.strftime("%Y%m%d"), now.strftime("%Y-%m-%d %H:%M:%S")


def normalize_day(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    digits = "".join(ch for ch in text if ch.isdigit())
    if len(digits) != 8:
        return ""
    return digits


def iter_topic_rank_packets(log_path: Path = DEFAULT_LOG):
    if not log_path.exists():
        return
    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line_no, line in enumerate(lines, 1):
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = msg.get("payload") or {}
        if payload.get("direction") != "ssl_read":
            continue
        hex_text = payload.get("hex")
        if not isinstance(hex_text, str) or not hex_text:
            continue
        raw = bytes_from_hex(hex_text)
        body = _packet_body(raw)
        if body is None:
            continue
        items = decode_topic_rank_body(body)
        if not items:
            continue
        day, ts_beijing = _parse_packet_ts(payload.get("ts"))
        yield {
            "line": line_no,
            "source": "frida_global_20020_3009",
            "route": TOPIC_RANK_ROUTE.decode("ascii"),
            "packet_code": "3009",
            "day": day,
            "ts": payload.get("ts"),
            "ts_beijing": ts_beijing,
            "packet_size": payload.get("size"),
            "truncated": payload.get("truncated"),
            "count": len(items),
            "items": items,
        }


def iter_topic_table_packets(log_path: Path = DEFAULT_LOG):
    if not log_path.exists():
        return
    lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line_no, line in enumerate(lines, 1):
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = msg.get("payload") or {}
        if payload.get("direction") != "ssl_read":
            continue
        hex_text = payload.get("hex")
        if not isinstance(hex_text, str) or not hex_text:
            continue
        raw = bytes_from_hex(hex_text)
        parts = _table_packet_parts(raw)
        if parts is None:
            continue
        topic_id, body = parts
        decoded = decode_topic_table_body(body, topic_id)
        if not decoded.get("rows"):
            continue
        day, ts_beijing = _parse_packet_ts(payload.get("ts"))
        yield {
            "line": line_no,
            "source": "frida_global_20020_3010",
            "route": f"{TOPIC_TABLE_ROUTE_PREFIX.decode('ascii')}{topic_id}",
            "packet_code": "3010",
            "day": day,
            "ts": payload.get("ts"),
            "ts_beijing": ts_beijing,
            "packet_size": payload.get("size"),
            "truncated": payload.get("truncated"),
            "body": decoded,
        }


def latest_topic_rank_list(
    *,
    day: str = "",
    log_path: Path = DEFAULT_LOG,
    limit: int | None = None,
) -> dict[str, Any] | None:
    normalized_day = normalize_day(day)
    latest: dict[str, Any] | None = None
    for packet in iter_topic_rank_packets(log_path) or []:
        if normalized_day and packet["day"] != normalized_day:
            continue
        latest = packet
    if latest is None:
        return None
    result = dict(latest)
    items = list(result.get("items") or [])
    if limit is not None and limit > 0:
        items = items[:limit]
    result["items"] = items
    result["count"] = len(items)
    result["total"] = latest.get("count", len(items))
    return result


def latest_topic_table_content(
    topic_id: str,
    *,
    day: str = "",
    log_path: Path = DEFAULT_LOG,
    limit: int | None = None,
) -> dict[str, Any] | None:
    target_topic_id = str(topic_id or "").strip()
    normalized_day = normalize_day(day)
    latest: dict[str, Any] | None = None
    for packet in iter_topic_table_packets(log_path) or []:
        body = packet.get("body") or {}
        if target_topic_id and str(body.get("topic_id") or "") != target_topic_id:
            continue
        if normalized_day and packet["day"] != normalized_day:
            continue
        latest = packet
    if latest is None:
        return None
    result = dict(latest)
    body = dict(result.get("body") or {})
    rows = list(body.get("rows") or [])
    if limit is not None and limit > 0:
        rows = rows[:limit]
    body["rows"] = rows
    body["count"] = len(rows)
    result["body"] = body
    return result


def available_topic_rank_days(*, log_path: Path = DEFAULT_LOG) -> list[str]:
    days: set[str] = set()
    for packet in iter_topic_rank_packets(log_path) or []:
        day = str(packet.get("day") or "")
        if day:
            days.add(day)
    return sorted(days)


def available_topic_table_topics(*, log_path: Path = DEFAULT_LOG) -> list[dict[str, str]]:
    seen: dict[str, str] = {}
    for packet in iter_topic_table_packets(log_path) or []:
        body = packet.get("body") or {}
        topic_id = str(body.get("topic_id") or "")
        if topic_id:
            seen[topic_id] = str(packet.get("day") or "")
    return [{"topic_id": topic_id, "latest_day": day} for topic_id, day in sorted(seen.items())]
