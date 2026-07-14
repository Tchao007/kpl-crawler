# -*- coding: utf-8 -*-
"""Local user, role, expiration and session management."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,32}$")
PASSWORD_ITERATIONS = 260_000
SESSION_TTL_DAYS = 7
ACTIVATION_CODE_BYTES = 12
DEFAULT_RESET_PASSWORD = "Kpl@13579"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def today_utc() -> date:
    return utcnow().date()


def now_iso() -> str:
    return utcnow().replace(microsecond=0).isoformat()


def parse_expiration(value: Any) -> date | None:
    if value in {None, ""}:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text:
        return None
    if "T" in text:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    return date.fromisoformat(text)


def normalize_expiration(value: Any, role: str) -> str | None:
    expires = parse_expiration(value)
    return expires.isoformat() if expires else None


def normalize_remaining_calls(value: Any) -> int | None:
    if value in {None, ""}:
        return None
    if isinstance(value, str) and value.strip().lower() in {"unlimited", "none", "null", "-1"}:
        return None
    try:
        calls = int(value)
    except (TypeError, ValueError):
        raise ValueError("remaining_calls must be a non-negative integer or empty for unlimited")
    if calls < 0:
        return None
    return calls


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return "pbkdf2_sha256${}${}${}".format(
        PASSWORD_ITERATIONS,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def session_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def normalize_code(code: str) -> str:
    return "".join(ch for ch in str(code).upper() if ch.isalnum())


def activation_code_hash(code: str) -> str:
    return hashlib.sha256(normalize_code(code).encode("utf-8")).hexdigest()


def new_activation_code() -> str:
    raw = secrets.token_hex(ACTIVATION_CODE_BYTES).upper()
    return "-".join(raw[index : index + 4] for index in range(0, len(raw), 4))


class AuthStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.lock = threading.RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file()

    def _ensure_file(self) -> None:
        with self.lock:
            if self.path.exists():
                self._cleanup_expired_sessions()
                return

            admin_password = os.environ.get("KPL_ADMIN_PASSWORD", "admin123456")
            data = {
                "users": {
                    "admin": {
                        "id": str(uuid.uuid4()),
                        "username": "admin",
                        "password_hash": hash_password(admin_password),
                        "role": "admin",
                        "disabled": False,
                        "expires_at": None,
                        "created_at": now_iso(),
                        "updated_at": now_iso(),
                    }
                },
                "sessions": {},
                "activation_codes": {},
            }
            self._write(data)

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"users": {}, "sessions": {}}
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        data.setdefault("users", {})
        data.setdefault("sessions", {})
        data.setdefault("activation_codes", {})
        return data

    def _write(self, data: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

    def _cleanup_expired_sessions(self) -> None:
        with self.lock:
            data = self._read()
            now = utcnow()
            sessions = data.get("sessions", {})
            live_sessions = {}
            for key, session in sessions.items():
                try:
                    expires_at = datetime.fromisoformat(session.get("expires_at", ""))
                except ValueError:
                    continue
                if expires_at > now:
                    live_sessions[key] = session
            if live_sessions != sessions:
                data["sessions"] = live_sessions
                self._write(data)

    def public_user(self, user: dict[str, Any]) -> dict[str, Any]:
        expires_at = user.get("expires_at")
        remaining_calls = normalize_remaining_calls(user.get("remaining_calls"))
        return {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role"),
            "disabled": bool(user.get("disabled")),
            "expires_at": expires_at,
            "expired": self.is_expired(user),
            "remaining_calls": remaining_calls,
            "call_limit_enabled": user.get("role") != "admin" and remaining_calls is not None,
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
        }

    def _user_activation_summary(self, data: dict[str, Any], username: str) -> dict[str, Any] | None:
        for record in data.get("activation_codes", {}).values():
            if record.get("used_by") == username and not record.get("disabled"):
                public_record = self.public_activation_code(record)
                public_record["code"] = record.get("code") or ""
                public_record["has_plain_code"] = bool(record.get("code"))
                return public_record
        return None

    def is_expired(self, user: dict[str, Any]) -> bool:
        if user.get("role") == "admin":
            return False
        expires_at = parse_expiration(user.get("expires_at"))
        return expires_at is None or expires_at < today_utc()

    def login(self, username: str, password: str) -> tuple[str | None, dict[str, Any] | None, str | None]:
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user or not verify_password(password, user.get("password_hash", "")):
                return None, None, "invalid_credentials"
            token = secrets.token_urlsafe(32)
            data["sessions"][session_hash(token)] = {
                "username": username,
                "created_at": now_iso(),
                "expires_at": (utcnow() + timedelta(days=SESSION_TTL_DAYS)).replace(microsecond=0).isoformat(),
            }
            self._write(data)
            if user.get("disabled"):
                return token, self.public_user(user), "disabled"
            if self.is_expired(user):
                return token, self.public_user(user), "expired"
            return token, self.public_user(user), None

    def logout(self, token: str | None) -> None:
        if not token:
            return
        with self.lock:
            data = self._read()
            data["sessions"].pop(session_hash(token), None)
            self._write(data)

    def session_user(self, token: str | None) -> tuple[dict[str, Any] | None, str | None]:
        if not token:
            return None, "missing_session"
        with self.lock:
            data = self._read()
            session = data["sessions"].get(session_hash(token))
            if not session:
                return None, "invalid_session"
            try:
                expires_at = datetime.fromisoformat(session.get("expires_at", ""))
            except ValueError:
                expires_at = utcnow() - timedelta(seconds=1)
            if expires_at <= utcnow():
                data["sessions"].pop(session_hash(token), None)
                self._write(data)
                return None, "invalid_session"
            user = data["users"].get(session.get("username"))
            if not user:
                return None, "invalid_session"
            public_user = self.public_user(user)
            if user.get("disabled"):
                return public_user, "disabled"
            if self.is_expired(user):
                return public_user, "expired"
            return public_user, None

    def session_identity(self, token: str | None) -> tuple[dict[str, Any] | None, str | None]:
        if not token:
            return None, "missing_session"
        with self.lock:
            data = self._read()
            session = data["sessions"].get(session_hash(token))
            if not session:
                return None, "invalid_session"
            user = data["users"].get(session.get("username"))
            if not user:
                return None, "invalid_session"
            if user.get("disabled"):
                return self.public_user(user), "disabled"
            return self.public_user(user), None

    def list_users(self) -> list[dict[str, Any]]:
        with self.lock:
            data = self._read()
            users = []
            for user in data["users"].values():
                public_user = self.public_user(user)
                public_user["activation_code"] = self._user_activation_summary(data, str(user.get("username", "")))
                users.append(public_user)
            return users

    def create_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        role = str(payload.get("role", "user")).strip().lower()
        if not USERNAME_RE.match(username):
            raise ValueError("用户名需为 3-32 位字母、数字、下划线、点或横线")
        if role not in {"admin", "user"}:
            raise ValueError("角色只能是 admin 或 user")
        if len(password) < 6:
            raise ValueError("密码至少 6 位")

        expires_at = normalize_expiration(payload.get("expires_at"), role)
        remaining_calls = None if role == "admin" else normalize_remaining_calls(payload.get("remaining_calls"))
        with self.lock:
            data = self._read()
            if username in data["users"]:
                raise ValueError("用户已存在")
            data["users"][username] = {
                "id": str(uuid.uuid4()),
                "username": username,
                "password_hash": hash_password(password),
                "role": role,
                "disabled": bool(payload.get("disabled", False)),
                "expires_at": expires_at,
                "remaining_calls": remaining_calls,
                "created_at": now_iso(),
                "updated_at": now_iso(),
            }
            self._write(data)
            return self.public_user(data["users"][username])

    def register_trial_user(self, payload: dict[str, Any]) -> dict[str, Any]:
        username = str(payload.get("username", "")).strip()
        password = str(payload.get("password", ""))
        if not USERNAME_RE.match(username):
            raise ValueError("username must be 3-32 chars: letters, numbers, dot, dash or underscore")
        if len(password) < 6:
            raise ValueError("password must be at least 6 chars")
        with self.lock:
            data = self._read()
            if username in data["users"]:
                raise ValueError("username already exists")
            data["users"][username] = {
                "id": str(uuid.uuid4()),
                "username": username,
                "password_hash": hash_password(password),
                "role": "user",
                "disabled": False,
                "expires_at": None,
                "remaining_calls": None,
                "created_at": now_iso(),
                "updated_at": now_iso(),
                "trial": False,
            }
            self._write(data)
            return self.public_user(data["users"][username])

    def update_user(self, username: str, payload: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                raise KeyError("用户不存在")
            if username == "admin" and payload.get("disabled") is True:
                raise ValueError("不能禁用内置管理员")

            role = str(payload.get("role", user.get("role", "user"))).strip().lower()
            if role not in {"admin", "user"}:
                raise ValueError("角色只能是 admin 或 user")
            user["role"] = role

            if "disabled" in payload:
                user["disabled"] = bool(payload.get("disabled"))
            if "expires_at" in payload:
                user["expires_at"] = normalize_expiration(payload.get("expires_at"), role)
            elif role == "user":
                user["expires_at"] = normalize_expiration(user.get("expires_at"), role)
            else:
                user["expires_at"] = user.get("expires_at")
            if role == "admin":
                user["remaining_calls"] = None
            elif "remaining_calls" in payload:
                user["remaining_calls"] = normalize_remaining_calls(payload.get("remaining_calls"))
            if payload.get("password"):
                password = str(payload["password"])
                if len(password) < 6:
                    raise ValueError("密码至少 6 位")
                user["password_hash"] = hash_password(password)
            user["updated_at"] = now_iso()
            self._write(data)
            return self.public_user(user)

    def consume_api_call(self, username: str, role: str) -> tuple[bool, str | None, int | None]:
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                return False, "invalid_session", None
            remaining_calls = normalize_remaining_calls(user.get("remaining_calls"))
            if user.get("disabled"):
                return False, "disabled", remaining_calls
            if user.get("role") == "admin" or role == "admin":
                return True, None, None
            if self.is_expired(user):
                return False, "expired", remaining_calls
            if remaining_calls is None:
                return True, None, None
            if remaining_calls <= 0:
                return False, "call_quota_exhausted", 0
            remaining_calls -= 1
            user["remaining_calls"] = remaining_calls
            user["updated_at"] = now_iso()
            self._write(data)
            return True, None, remaining_calls

    def change_password(self, username: str, old_password: str, new_password: str) -> dict[str, Any]:
        if len(new_password) < 6:
            raise ValueError("password must be at least 6 chars")
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                raise KeyError("user not found")
            if not verify_password(old_password, user.get("password_hash", "")):
                raise ValueError("old password is incorrect")
            user["password_hash"] = hash_password(new_password)
            user["updated_at"] = now_iso()
            self._write(data)
            return self.public_user(user)

    def reset_user_password(self, username: str, new_password: str = DEFAULT_RESET_PASSWORD) -> dict[str, Any]:
        if len(new_password) < 6:
            raise ValueError("password must be at least 6 chars")
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                raise KeyError("user not found")
            user["password_hash"] = hash_password(new_password)
            user["updated_at"] = now_iso()
            data["sessions"] = {
                key: session
                for key, session in data["sessions"].items()
                if session.get("username") != username
            }
            self._write(data)
            return self.public_user(user)

    def delete_user(self, username: str) -> None:
        if username == "admin":
            raise ValueError("不能删除内置管理员")
        with self.lock:
            data = self._read()
            if username not in data["users"]:
                raise KeyError("用户不存在")
            del data["users"][username]
            data["sessions"] = {
                key: session
                for key, session in data["sessions"].items()
                if session.get("username") != username
            }
            self._write(data)

    def public_activation_code(self, code: dict[str, Any]) -> dict[str, Any]:
        user_expires_at = None
        remaining_days = -1
        used_by = code.get("used_by")
        if used_by and not code.get("disabled"):
            data = self._read()
            user = data.get("users", {}).get(used_by)
            if user and not user.get("disabled"):
                user_expires_at = user.get("expires_at")
                expires = parse_expiration(user_expires_at)
                if expires and expires >= today_utc():
                    remaining_days = (expires - today_utc()).days
        return {
            "id": code.get("id"),
            "code_hash": code.get("code_hash", ""),
            "code": code.get("code", ""),
            "has_plain_code": bool(code.get("code")),
            "days": int(code.get("days", 0)),
            "disabled": bool(code.get("disabled")),
            "used": bool(used_by),
            "used_by": used_by,
            "used_at": code.get("used_at"),
            "created_at": code.get("created_at"),
            "note": code.get("note", ""),
            "user_expires_at": user_expires_at,
            "remaining_days": remaining_days,
        }

    def list_activation_codes(self) -> list[dict[str, Any]]:
        with self.lock:
            data = self._read()
            codes = [self.public_activation_code(code) for code in data["activation_codes"].values()]
            return sorted(codes, key=lambda item: str(item.get("created_at", "")), reverse=True)

    def create_activation_codes(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        days = int(payload.get("days") or 0)
        count = int(payload.get("count") or 1)
        note = str(payload.get("note") or "").strip()
        if days <= 0 or days > 3650:
            raise ValueError("days must be between 1 and 3650")
        if count <= 0 or count > 100:
            raise ValueError("count must be between 1 and 100")
        with self.lock:
            data = self._read()
            created: list[dict[str, Any]] = []
            for _ in range(count):
                code_text = new_activation_code()
                code_hash = activation_code_hash(code_text)
                while code_hash in data["activation_codes"]:
                    code_text = new_activation_code()
                    code_hash = activation_code_hash(code_text)
                record = {
                    "id": str(uuid.uuid4()),
                    "code_hash": code_hash,
                    "code": code_text,
                    "days": days,
                    "disabled": False,
                    "used_by": None,
                    "used_at": None,
                    "created_at": now_iso(),
                    "note": note,
                }
                data["activation_codes"][code_hash] = record
                public_record = self.public_activation_code(record)
                public_record["code"] = code_text
                created.append(public_record)
            self._write(data)
            return created

    def update_activation_code(self, code_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        with self.lock:
            data = self._read()
            for record in data["activation_codes"].values():
                if record.get("id") == code_id:
                    if "disabled" in payload:
                        record["disabled"] = bool(payload.get("disabled"))
                    if "note" in payload:
                        record["note"] = str(payload.get("note") or "").strip()
                    self._write(data)
                    return self.public_activation_code(record)
            raise KeyError("activation code not found")

    def delete_activation_code(self, code_id: str) -> None:
        with self.lock:
            data = self._read()
            for key, record in list(data["activation_codes"].items()):
                if record.get("id") == code_id:
                    if record.get("used_by"):
                        raise ValueError("used activation code cannot be deleted")
                    del data["activation_codes"][key]
                    self._write(data)
                    return
            raise KeyError("activation code not found")

    def redeem_activation_code(self, username: str, code_text: str) -> dict[str, Any]:
        code_hash = activation_code_hash(code_text)
        if not code_hash:
            raise ValueError("activation code is required")
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                raise KeyError("user not found")
            if user.get("role") != "user":
                raise ValueError("admin accounts do not need activation codes")
            if user.get("disabled"):
                raise ValueError("account disabled")
            record = data["activation_codes"].get(code_hash)
            if not record:
                raise ValueError("invalid activation code")
            if record.get("disabled"):
                raise ValueError("activation code disabled")
            if record.get("used_by"):
                raise ValueError("activation code already used")
            current = parse_expiration(user.get("expires_at")) or today_utc()
            base = current if current >= today_utc() else today_utc()
            user["expires_at"] = (base + timedelta(days=int(record["days"]))).isoformat()
            user["updated_at"] = now_iso()
            record["used_by"] = username
            record["used_at"] = now_iso()
            self._write(data)
            return {
                "user": self.public_user(user),
                "days": int(record["days"]),
                "expires_at": user["expires_at"],
            }

    def assign_activation_code_to_user(self, username: str, code_text: str) -> dict[str, Any]:
        code_hash = activation_code_hash(code_text)
        if not code_hash:
            raise ValueError("activation code is required")
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                raise KeyError("user not found")
            if user.get("role") != "user":
                raise ValueError("admin accounts do not need activation codes")
            if user.get("disabled"):
                raise ValueError("account disabled")
            record = data["activation_codes"].get(code_hash)
            if not record:
                raise ValueError("invalid activation code")
            if record.get("disabled"):
                raise ValueError("activation code disabled")
            if record.get("used_by") and record.get("used_by") != username:
                raise ValueError("activation code already used")
            for existing in data["activation_codes"].values():
                if existing is not record and existing.get("used_by") == username:
                    existing["used_by"] = None
                    existing["used_at"] = None
            user["expires_at"] = (today_utc() + timedelta(days=int(record["days"]))).isoformat()
            user["updated_at"] = now_iso()
            record["used_by"] = username
            record["used_at"] = now_iso()
            record["code"] = normalize_code(code_text)
            self._write(data)
            public_user = self.public_user(user)
            public_user["activation_code"] = self._user_activation_summary(data, username)
            return public_user

    def remove_user_activation_code(self, username: str) -> dict[str, Any]:
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                raise KeyError("user not found")
            if user.get("role") != "user":
                raise ValueError("admin accounts do not need activation codes")
            for record in data["activation_codes"].values():
                if record.get("used_by") == username:
                    record["used_by"] = None
                    record["used_at"] = None
            user["expires_at"] = None
            user["updated_at"] = now_iso()
            self._write(data)
            public_user = self.public_user(user)
            public_user["activation_code"] = None
            return public_user

    def validate_interface_activation_code(
        self,
        username: str,
        role: str,
        code_text: str,
    ) -> tuple[bool, str | None]:
        code_hash = activation_code_hash(code_text)
        if not code_hash:
            return False, "missing_activation_code"
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                return False, "invalid_session"
            if user.get("disabled"):
                return False, "disabled"
            if user.get("role") != "admin" and self.is_expired(user):
                return False, "expired"

            record = data["activation_codes"].get(code_hash)
            if not record:
                return False, "invalid_activation_code"
            if record.get("disabled"):
                return False, "activation_code_disabled"

            if role == "admin":
                return True, None
            if record.get("used_by") != username:
                return False, "activation_code_not_bound_to_user"
            return True, None

    def validate_interface_user_activation(self, username: str, role: str) -> tuple[bool, str | None]:
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user:
                return False, "invalid_session"
            if user.get("disabled"):
                return False, "disabled"
            if user.get("role") == "admin" or role == "admin":
                return True, None
            if self.is_expired(user):
                return False, "expired"
            for record in data["activation_codes"].values():
                if record.get("used_by") == username and not record.get("disabled"):
                    return True, None
            return False, "missing_bound_activation_code"

    def user_for_interface_activation_code(self, code_text: str) -> tuple[dict[str, Any] | None, str | None]:
        code_hash = activation_code_hash(code_text)
        if not code_hash:
            return None, "missing_activation_code"
        with self.lock:
            data = self._read()
            record = data["activation_codes"].get(code_hash)
            if not record:
                return None, "invalid_activation_code"
            if record.get("disabled"):
                return None, "activation_code_disabled"
            username = record.get("used_by")
            if not username:
                return None, "activation_code_not_bound_to_user"
            user = data["users"].get(username)
            if not user:
                return None, "invalid_session"
            if user.get("disabled"):
                return None, "disabled"
            if user.get("role") != "admin" and self.is_expired(user):
                return None, "expired"
            return self.public_user(user), None

    def user_for_interface_credentials(
        self,
        username: str,
        password: str,
        code_text: str,
    ) -> tuple[dict[str, Any] | None, str | None]:
        username = str(username or "").strip()
        if not username or not password:
            return None, "missing_credentials"
        code_hash = activation_code_hash(code_text)
        if not code_hash:
            return None, "missing_activation_code"
        with self.lock:
            data = self._read()
            user = data["users"].get(username)
            if not user or not verify_password(password, user.get("password_hash", "")):
                return None, "invalid_credentials"
            if user.get("disabled"):
                return None, "disabled"
            if user.get("role") != "admin" and self.is_expired(user):
                return None, "expired"
            record = data["activation_codes"].get(code_hash)
            if not record:
                return None, "invalid_activation_code"
            if record.get("disabled"):
                return None, "activation_code_disabled"
            if user.get("role") != "admin" and record.get("used_by") != username:
                return None, "activation_code_not_bound_to_user"
            return self.public_user(user), None
