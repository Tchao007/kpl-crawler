# -*- coding: utf-8 -*-
"""Shared upstream safety controls: rate limiting, cache and circuit breaker."""

from __future__ import annotations

import copy
import hashlib
import json
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
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


class UpstreamCircuitOpen(Exception):
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


class UpstreamRateLimited(Exception):
    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


@dataclass
class CacheEntry:
    payload: object
    content_type: str
    status_code: int
    created_at: float
    ttl: int


class UpstreamGuard:
    def __init__(
        self,
        min_interval: float = 2.0,
        max_per_minute: int = 24,
        max_per_hour: int = 300,
    ) -> None:
        self.min_interval = min_interval
        self.max_per_minute = max_per_minute
        self.max_per_hour = max_per_hour
        self._lock = threading.RLock()
        self._last_request_at = 0.0
        self._minute_window: deque[float] = deque()
        self._hour_window: deque[float] = deque()
        self._cache: dict[str, CacheEntry] = {}
        self._circuit_until: dict[str, float] = defaultdict(float)
        self._failures: dict[str, int] = defaultdict(int)

    def cache_get(self, key: str) -> tuple[object, dict[str, object]] | None:
        now = time.time()
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None
            age = now - entry.created_at
            if age > entry.ttl:
                self._cache.pop(key, None)
                return None
            return (
                copy.deepcopy(entry.payload),
                {
                    "hit": True,
                    "ttl": entry.ttl,
                    "age_seconds": round(age, 3),
                    "stale": False,
                    "status_code": entry.status_code,
                    "content_type": entry.content_type,
                },
            )

    def cache_set(self, key: str, payload: object, content_type: str, status_code: int, ttl: int) -> None:
        if ttl <= 0:
            return
        with self._lock:
            self._cache[key] = CacheEntry(
                payload=copy.deepcopy(payload),
                content_type=content_type,
                status_code=status_code,
                created_at=time.time(),
                ttl=ttl,
            )

    def before_request(self, host: str, endpoint: str) -> dict[str, object]:
        now = time.time()
        circuit_keys = self._circuit_keys(host, endpoint)
        with self._lock:
            retry_after = max(int(self._circuit_until[key] - now) for key in circuit_keys)
            if retry_after > 0:
                raise UpstreamCircuitOpen("上游接口已熔断", retry_after)

            self._prune_windows(now)
            if len(self._minute_window) >= self.max_per_minute:
                retry_after = max(1, int(60 - (now - self._minute_window[0])))
                raise UpstreamRateLimited("上游请求超过每分钟限额", retry_after)
            if len(self._hour_window) >= self.max_per_hour:
                retry_after = max(1, int(3600 - (now - self._hour_window[0])))
                raise UpstreamRateLimited("上游请求超过每小时限额", retry_after)

            wait = max(0.0, self.min_interval - (now - self._last_request_at))
            if wait:
                time.sleep(wait)
            actual = time.time()
            self._last_request_at = actual
            self._minute_window.append(actual)
            self._hour_window.append(actual)
            return {"rate_limited_ms": int(wait * 1000), "host": host}

    def record_result(self, host: str, endpoint: str, payload: object, upstream_error: str = "") -> dict[str, object]:
        text = json.dumps(payload, ensure_ascii=False).lower() if not isinstance(payload, str) else payload.lower()
        is_auth_error = bool(upstream_error) or any(marker.lower() in text for marker in AUTH_ERROR_MARKERS)
        circuit_opened = False
        retry_after = 0
        with self._lock:
            for key in self._circuit_keys(host, endpoint):
                if is_auth_error:
                    self._failures[key] += 1
                else:
                    self._failures[key] = 0

            if is_auth_error:
                global_break = any(marker in text for marker in ("验证码", "风控", "频繁", "captcha"))
                duration = 1800 if global_break else 300
                if global_break or self._failures[f"endpoint:{endpoint}"] >= 3:
                    keys = ["global"] if global_break else self._circuit_keys(host, endpoint)
                    until = time.time() + duration
                    for key in keys:
                        self._circuit_until[key] = max(self._circuit_until[key], until)
                    circuit_opened = True
                    retry_after = duration
        return {"circuit_opened": circuit_opened, "retry_after": retry_after}

    def _circuit_keys(self, host: str, endpoint: str) -> list[str]:
        return ["global", f"host:{host}", f"endpoint:{endpoint}"]

    def _prune_windows(self, now: float) -> None:
        while self._minute_window and now - self._minute_window[0] > 60:
            self._minute_window.popleft()
        while self._hour_window and now - self._hour_window[0] > 3600:
            self._hour_window.popleft()


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
