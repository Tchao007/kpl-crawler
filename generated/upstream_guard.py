# -*- coding: utf-8 -*-
"""SQLite-backed upstream safety controls: rate limiting, cache and circuit breaker."""

from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
import threading
import time
from pathlib import Path
from urllib.parse import urlparse


SENSITIVE_KEYS = {
    "_ts",
    "token",
    "userid",
    "deviceid",
    "device_id",
    "clientsign",
    "x-api-key",
    "password",
}

AUTH_ERROR_MARKERS = (
    "登录状态失效",
    "登录",
    "登陆",
    "失效",
    "过期",
    "未授权",
    "验证码",
    "风控",
    "频繁",
    "异常",
    "login",
    "token",
    "auth",
    "captcha",
    "forbidden",
)

GLOBAL_SCOPE = "global"


class UpstreamCircuitOpen(Exception):
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


class UpstreamRateLimited(Exception):
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


class UpstreamGuard:
    def __init__(
        self,
        min_interval: float = 2.0,
        max_per_minute: int = 24,
        max_per_hour: int = 300,
        db_path: str | Path | None = None,
    ) -> None:
        self.min_interval = min_interval
        self.max_per_minute = max_per_minute
        self.max_per_hour = max_per_hour
        self.db_path = Path(db_path) if db_path else Path(__file__).with_name("upstream_guard.sqlite3")
        self._lock = threading.RLock()
        self._init_db()

    def cache_get(self, key: str) -> tuple[object, dict[str, object]] | None:
        now = time.time()
        with self._lock, self._connect() as conn:
            self._prune_cache(conn, now)
            row = conn.execute(
                """
                SELECT payload, content_type, status_code, created_at, ttl
                FROM upstream_cache
                WHERE cache_key = ?
                """,
                (key,),
            ).fetchone()
            if not row:
                return None
            payload_text, content_type, status_code, created_at, ttl = row
            age = now - float(created_at)
            if age > int(ttl):
                conn.execute("DELETE FROM upstream_cache WHERE cache_key = ?", (key,))
                return None
            try:
                payload = json.loads(payload_text)
            except json.JSONDecodeError:
                payload = payload_text
            return (
                copy.deepcopy(payload),
                {
                    "hit": True,
                    "ttl": int(ttl),
                    "age_seconds": round(age, 3),
                    "stale": False,
                    "status_code": int(status_code),
                    "content_type": content_type or "application/json",
                    "store": "sqlite",
                },
            )

    def cache_set(self, key: str, payload: object, content_type: str, status_code: int, ttl: int) -> None:
        if ttl <= 0:
            return
        now = time.time()
        payload_text = json.dumps(payload, ensure_ascii=False, default=str, separators=(",", ":"))
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO upstream_cache(cache_key, created_at, ttl, status_code, content_type, payload)
                VALUES(?, ?, ?, ?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    created_at = excluded.created_at,
                    ttl = excluded.ttl,
                    status_code = excluded.status_code,
                    content_type = excluded.content_type,
                    payload = excluded.payload
                """,
                (key, now, int(ttl), int(status_code), str(content_type or ""), payload_text),
            )
            self._prune_cache(conn, now)

    def before_request(self, host: str, endpoint: str) -> dict[str, object]:
        host = str(host or "")
        endpoint = str(endpoint or "")
        scopes = self._circuit_keys(host, endpoint)
        with self._lock, self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            now = time.time()
            self._prune_requests(conn, now)
            retry_after = self._circuit_retry_after(conn, scopes, now)
            if retry_after > 0:
                raise UpstreamCircuitOpen("upstream circuit is open", retry_after)

            minute_count = self._request_count_since(conn, now - 60)
            if minute_count >= self.max_per_minute:
                retry_after = self._retry_after_oldest(conn, now, 60)
                raise UpstreamRateLimited("upstream request per-minute limit exceeded", retry_after)

            hour_count = self._request_count_since(conn, now - 3600)
            if hour_count >= self.max_per_hour:
                retry_after = self._retry_after_oldest(conn, now, 3600)
                raise UpstreamRateLimited("upstream request per-hour limit exceeded", retry_after)

            last_ts = self._last_request_ts(conn)
            wait = max(0.0, self.min_interval - (now - last_ts)) if last_ts else 0.0
            if wait:
                time.sleep(wait)

            actual = time.time()
            conn.execute(
                "INSERT INTO upstream_requests(ts, host, endpoint) VALUES(?, ?, ?)",
                (actual, host, endpoint),
            )
            return {"rate_limited_ms": int(wait * 1000), "host": host, "store": "sqlite"}

    def record_result(self, host: str, endpoint: str, payload: object, upstream_error: str = "") -> dict[str, object]:
        host = str(host or "")
        endpoint = str(endpoint or "")
        text = _search_text(payload)
        is_auth_error = (
            bool(upstream_error)
            or _has_risk_errcode(payload)
            or any(marker.lower() in text for marker in AUTH_ERROR_MARKERS)
        )
        circuit_opened = False
        retry_after = 0
        scopes = self._circuit_keys(host, endpoint)

        with self._lock, self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            for scope in scopes:
                if is_auth_error:
                    conn.execute(
                        """
                        INSERT INTO upstream_failures(scope, count, updated_at)
                        VALUES(?, 1, ?)
                        ON CONFLICT(scope) DO UPDATE SET
                            count = count + 1,
                            updated_at = excluded.updated_at
                        """,
                        (scope, time.time()),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO upstream_failures(scope, count, updated_at)
                        VALUES(?, 0, ?)
                        ON CONFLICT(scope) DO UPDATE SET
                            count = 0,
                            updated_at = excluded.updated_at
                        """,
                        (scope, time.time()),
                    )

            if is_auth_error:
                global_break = any(marker in text for marker in ("验证码", "风控", "频繁", "captcha"))
                duration = 1800 if global_break else 300
                endpoint_failures = self._failure_count(conn, f"endpoint:{endpoint}")
                if global_break or endpoint_failures >= 3:
                    until_ts = time.time() + duration
                    target_scopes = [GLOBAL_SCOPE] if global_break else scopes
                    for scope in target_scopes:
                        conn.execute(
                            """
                            INSERT INTO upstream_circuit(scope, until_ts, reason, updated_at)
                            VALUES(?, ?, ?, ?)
                            ON CONFLICT(scope) DO UPDATE SET
                                until_ts = MAX(until_ts, excluded.until_ts),
                                reason = excluded.reason,
                                updated_at = excluded.updated_at
                            """,
                            (scope, until_ts, upstream_error or "auth_or_risk_marker", time.time()),
                        )
                    circuit_opened = True
                    retry_after = duration

        return {"circuit_opened": circuit_opened, "retry_after": retry_after, "store": "sqlite"}

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path), timeout=10, isolation_level=None)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA busy_timeout=10000")
        return conn

    def _init_db(self) -> None:
        with self._lock, self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS upstream_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL NOT NULL,
                    host TEXT NOT NULL,
                    endpoint TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_upstream_requests_ts
                    ON upstream_requests(ts);

                CREATE TABLE IF NOT EXISTS upstream_cache (
                    cache_key TEXT PRIMARY KEY,
                    created_at REAL NOT NULL,
                    ttl INTEGER NOT NULL,
                    status_code INTEGER NOT NULL,
                    content_type TEXT,
                    payload TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_upstream_cache_expiry
                    ON upstream_cache(created_at, ttl);

                CREATE TABLE IF NOT EXISTS upstream_circuit (
                    scope TEXT PRIMARY KEY,
                    until_ts REAL NOT NULL,
                    reason TEXT,
                    updated_at REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS upstream_failures (
                    scope TEXT PRIMARY KEY,
                    count INTEGER NOT NULL,
                    updated_at REAL NOT NULL
                );
                """
            )

    def _circuit_keys(self, host: str, endpoint: str) -> list[str]:
        return [GLOBAL_SCOPE, f"host:{host}", f"endpoint:{endpoint}"]

    def _circuit_retry_after(self, conn: sqlite3.Connection, scopes: list[str], now: float) -> int:
        placeholders = ",".join("?" for _ in scopes)
        rows = conn.execute(
            f"SELECT until_ts FROM upstream_circuit WHERE scope IN ({placeholders})",
            tuple(scopes),
        ).fetchall()
        retry_after = 0
        for (until_ts,) in rows:
            retry_after = max(retry_after, int(float(until_ts) - now))
        return retry_after

    def _request_count_since(self, conn: sqlite3.Connection, since_ts: float) -> int:
        return int(conn.execute("SELECT COUNT(*) FROM upstream_requests WHERE ts >= ?", (since_ts,)).fetchone()[0])

    def _retry_after_oldest(self, conn: sqlite3.Connection, now: float, window_seconds: int) -> int:
        row = conn.execute(
            "SELECT MIN(ts) FROM upstream_requests WHERE ts >= ?",
            (now - window_seconds,),
        ).fetchone()
        oldest = float(row[0]) if row and row[0] is not None else now
        return max(1, int(window_seconds - (now - oldest)))

    def _last_request_ts(self, conn: sqlite3.Connection) -> float:
        row = conn.execute("SELECT MAX(ts) FROM upstream_requests").fetchone()
        return float(row[0]) if row and row[0] is not None else 0.0

    def _failure_count(self, conn: sqlite3.Connection, scope: str) -> int:
        row = conn.execute("SELECT count FROM upstream_failures WHERE scope = ?", (scope,)).fetchone()
        return int(row[0]) if row else 0

    def _prune_requests(self, conn: sqlite3.Connection, now: float) -> None:
        conn.execute("DELETE FROM upstream_requests WHERE ts < ?", (now - 3700,))
        conn.execute("DELETE FROM upstream_circuit WHERE until_ts < ?", (now,))

    def _prune_cache(self, conn: sqlite3.Connection, now: float) -> None:
        conn.execute("DELETE FROM upstream_cache WHERE created_at + ttl < ?", (now,))


def host_from_url(url: object) -> str:
    try:
        return urlparse(str(url or "")).netloc
    except ValueError:
        return ""


def stable_cache_key(*parts: object) -> str:
    clean_parts = [_sanitize(value) for value in parts]
    raw = json.dumps(clean_parts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _sanitize(value: object) -> object:
    if isinstance(value, dict):
        return {
            str(key): _sanitize(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            if str(key).lower() not in SENSITIVE_KEYS
        }
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


def _search_text(value: object) -> str:
    parts: list[str] = []

    def walk(item: object) -> None:
        if isinstance(item, dict):
            for key, nested in item.items():
                parts.append(str(key))
                walk(nested)
        elif isinstance(item, list):
            for nested in item:
                walk(nested)
        else:
            parts.append(str(item))

    walk(value)
    try:
        parts.append(json.dumps(value, ensure_ascii=False, default=str))
    except TypeError:
        pass
    return " ".join(parts).lower()


def _has_risk_errcode(value: object) -> bool:
    if isinstance(value, dict):
        errcode = str(
            value.get("errcode")
            or value.get("code")
            or value.get("status_code")
            or value.get("status")
            or ""
        ).strip()
        if errcode in {"1001", "1002", "401", "403"}:
            return True
        return any(_has_risk_errcode(item) for item in value.values())
    if isinstance(value, list):
        return any(_has_risk_errcode(item) for item in value)
    return False
