# -*- coding: utf-8 -*-
"""Decode Kaipanla hqStock binary quote packets captured by Frida."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_LOG = Path(__file__).resolve().parent.parent / "outputs" / "frida" / "kpl_capture.ndjson"
ROUTE_RE = re.compile(rb"hqStock(?:New)?\|[^/]+/(\d+)-([01])/([A-Z0-9:]+)")
PRICE_SCALE = 10000
SHARES_PER_LOT = 100

HQ_API_KEYS = {
    "five_level": {
        "source": "hqStock",
        "packet_code": "2015",
        "endpoint": "/api/hq/five_level",
        "description": "Decode latest five-level order book from captured hqStock packets.",
    },
    "time_sales": {
        "source": "hqStock",
        "packet_code": "2006",
        "endpoint": "/api/hq/time_sales",
        "description": "Decode intraday time-and-sales trades from captured hqStock packets.",
    }
}

@dataclass
class ProtoField:
    number: int
    wire: int
    value: int | None = None
    raw: bytes = b""
    nested: list["ProtoField"] | None = None


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
    raise ValueError("bad varint")


def parse_proto(buf: bytes, *, depth: int = 0, max_depth: int = 4) -> list[ProtoField]:
    fields: list[ProtoField] = []
    pos = 0
    while pos < len(buf):
        try:
            key, pos = read_varint(buf, pos)
        except ValueError:
            break
        number = key >> 3
        wire = key & 7
        try:
            if wire == 0:
                value, pos = read_varint(buf, pos)
                fields.append(ProtoField(number=number, wire=wire, value=value))
            elif wire == 1:
                raw = buf[pos : pos + 8]
                pos += 8
                fields.append(ProtoField(number=number, wire=wire, raw=raw))
            elif wire == 2:
                size, pos = read_varint(buf, pos)
                raw = buf[pos : pos + size]
                pos += size
                nested = parse_proto(raw, depth=depth + 1, max_depth=max_depth) if depth < max_depth else None
                fields.append(ProtoField(number=number, wire=wire, raw=raw, nested=nested))
            elif wire == 5:
                raw = buf[pos : pos + 4]
                pos += 4
                fields.append(ProtoField(number=number, wire=wire, raw=raw))
            else:
                break
        except (IndexError, ValueError):
            break
    return fields


def _message_body(raw: bytes, route_match: re.Match[bytes]) -> bytes:
    pos = route_match.end()
    for candidate in range(pos, min(pos + 8, len(raw))):
        if raw[candidate] == 0x0A:
            return raw[candidate:]
    return raw[pos:]


def _level_from_field(field: ProtoField) -> dict[str, Any] | None:
    if not field.nested:
        return None
    values = {leaf.number: leaf.value for leaf in field.nested if leaf.value is not None}
    price_raw = values.get(1)
    volume = values.get(3)
    if price_raw is None or volume is None:
        return None
    price = price_raw / PRICE_SCALE
    amount = price * volume * SHARES_PER_LOT
    return {
        "price": price,
        "price_raw": price_raw,
        "volume": volume,
        "volume_unit": "lot",
        "amount": round(amount, 2),
        "amount_raw": int(round(amount * 100)),
        "amount_unit": "CNY",
    }


def decode_2015_body(body: bytes) -> dict[str, Any]:
    fields = parse_proto(body)
    stock = ""
    base_price_raw = None
    snapshots: list[dict[str, Any]] = []
    for field in fields:
        if field.number == 1 and field.raw:
            stock = field.raw.decode("ascii", errors="ignore")
        elif field.number == 3 and field.value is not None:
            base_price_raw = field.value
        elif field.number == 10 and field.nested:
            snap: dict[str, Any] = {"sell": [], "buy": []}
            for sub in field.nested:
                if sub.value is not None and sub.number in {1, 2, 3, 4, 5}:
                    snap[f"f{sub.number}"] = sub.value
                elif sub.number == 6:
                    level = _level_from_field(sub)
                    if level:
                        snap["sell"].append(level)
                elif sub.number == 7:
                    level = _level_from_field(sub)
                    if level:
                        snap["buy"].append(level)
            if snap["sell"] or snap["buy"]:
                snapshots.append(snap)
    return {
        "stock": stock,
        "base_price": base_price_raw / PRICE_SCALE if base_price_raw is not None else None,
        "base_price_raw": base_price_raw,
        "snapshots": snapshots,
    }


def _format_hhmmssmmm(value: int | None) -> str:
    if value is None:
        return ""
    text = f"{value:09d}"
    return f"{text[:2]}:{text[2:4]}:{text[4:6]}.{text[6:]}"


def _side_from_flag(value: int | None) -> str:
    if value == 1:
        return "buy"
    if value == 2:
        return "sell"
    return "neutral"


def decode_2006_body(body: bytes) -> dict[str, Any]:
    fields = parse_proto(body)
    stock = ""
    day = None
    trades: list[dict[str, Any]] = []
    for field in fields:
        if field.number == 1 and field.raw:
            stock = field.raw.decode("ascii", errors="ignore")
        elif field.number == 2 and field.value is not None:
            day = str(field.value)
        elif field.number == 10 and field.nested:
            values = {sub.number: sub.value for sub in field.nested if sub.value is not None}
            time_raw = values.get(1)
            price_raw = values.get(2)
            side_flag = values.get(3)
            volume = values.get(4)
            amount_raw = values.get(6)
            if time_raw is None or price_raw is None:
                continue
            price = price_raw / PRICE_SCALE
            amount = amount_raw if amount_raw is not None else (
                price * volume * SHARES_PER_LOT if volume is not None else None
            )
            trades.append(
                {
                    "time": _format_hhmmssmmm(time_raw),
                    "time_raw": time_raw,
                    "price": price,
                    "price_raw": price_raw,
                    "side": _side_from_flag(side_flag),
                    "side_flag": side_flag,
                    "volume": volume,
                    "volume_unit": "lot",
                    "amount": round(amount, 2) if amount is not None else None,
                    "amount_raw": amount_raw,
                    "amount_unit": "CNY",
                }
            )
    return {"stock": stock, "day": day, "trades": trades}


def iter_hqstock_packets(log_path: Path = DEFAULT_LOG):
    if not log_path.exists():
        return
    for line_no, line in enumerate(log_path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
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
        match = ROUTE_RE.search(raw)
        if not match:
            continue
        code = match.group(1).decode("ascii")
        flag = match.group(2).decode("ascii")
        stock = match.group(3).decode("ascii")
        yield {
            "line": line_no,
            "code": code,
            "flag": flag,
            "stock": stock.split(":", 1)[0],
            "stock_route": stock,
            "size": payload.get("size"),
            "truncated": payload.get("truncated"),
            "body": _message_body(raw, match),
        }


def normalize_stock_id(value: str) -> str:
    stock_id = str(value or "").strip().upper()
    if stock_id.startswith(("SH", "SZ", "BJ")) and len(stock_id) > 2:
        stock_id = stock_id[2:]
    return stock_id


def latest_stock_for_code(code: str, *, log_path: Path = DEFAULT_LOG) -> str:
    latest = ""
    for packet in iter_hqstock_packets(log_path) or []:
        if packet["code"] == str(code):
            latest = str(packet["stock"])
    return latest


def latest_five_level(stock_id: str, *, log_path: Path = DEFAULT_LOG) -> dict[str, Any] | None:
    stock_id = normalize_stock_id(stock_id)
    latest: dict[str, Any] | None = None
    for packet in iter_hqstock_packets(log_path) or []:
        if packet["code"] != "2015" or packet["stock"] != stock_id:
            continue
        decoded = decode_2015_body(packet["body"])
        snapshots = decoded.get("snapshots") or []
        if not snapshots:
            continue
        snapshot = snapshots[-1]
        latest = {
            "stock": stock_id,
            "source": "frida_hqstock_2015",
            "line": packet["line"],
            "packet_size": packet["size"],
            "truncated": packet["truncated"],
            "sequence": snapshot.get("f1"),
            "base_price": decoded.get("base_price"),
            "sell": snapshot.get("sell", [])[:5],
            "buy": snapshot.get("buy", [])[:5],
            "raw_fields": {
                key: value for key, value in snapshot.items() if key.startswith("f")
            },
        }
    return latest


def latest_time_sales(stock_id: str, *, log_path: Path = DEFAULT_LOG, limit: int = 100) -> dict[str, Any] | None:
    stock_id = normalize_stock_id(stock_id)
    latest: dict[str, Any] | None = None
    for packet in iter_hqstock_packets(log_path) or []:
        if packet["code"] != "2006" or packet["stock"] != stock_id:
            continue
        decoded = decode_2006_body(packet["body"])
        trades = decoded.get("trades") or []
        if not trades:
            continue
        latest = {
            "stock": stock_id,
            "source": "frida_hqstock_2006",
            "line": packet["line"],
            "packet_size": packet["size"],
            "truncated": packet["truncated"],
            "day": decoded.get("day"),
            "count": len(trades),
            "trades": trades[-limit:] if limit > 0 else trades,
        }
    return latest
