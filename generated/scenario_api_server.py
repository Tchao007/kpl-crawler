# -*- coding: utf-8 -*-
"""HTTP API wrapper for generated Kaipanla capture scenarios."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, unquote, urlparse

from auth_store import AuthStore
from kaipanla_capture_client import KaipanlaCapturedClient, REQUESTS


ROOT = Path(__file__).resolve().parent
TOOLS_DIR = ROOT.parent / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
from crawl_topic_library import crawl_topic_library, write_outputs

CLIENT_FILE = "kaipanla_capture_client.py"
PAGE_FILE = "capture_scenarios.html"
LOGIN_FILE = "login.html"
REGISTER_FILE = "register.html"
EXPIRED_FILE = "expired.html"
ADMIN_FILE = "admin.html"
AUTH_DB_FILE = ROOT / "users.json"
SESSION_COOKIE = "kpl_session"
AUTH = AuthStore(AUTH_DB_FILE)


def _safe_route_part(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


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
                "title": f"{controller}.{action}",
                "method_name": method_name,
                "http_method": spec["method"],
                "target_url": spec["url"],
                "endpoint": endpoint,
                "alias_endpoint": alias_endpoint,
                "params": params,
                "data": data,
            }
        )
    return scenarios


SCENARIOS = _build_scenarios()
ROUTES: dict[str, dict[str, object]] = {}
for scenario, spec in zip(SCENARIOS, REQUESTS):
    ROUTES[scenario["endpoint"]] = {"scenario": scenario, "spec": spec}
    ROUTES[scenario["alias_endpoint"]] = {"scenario": scenario, "spec": spec}


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
            self._send_json({"count": len(SCENARIOS), "scenarios": SCENARIOS, "user": user})
            return

        if path.startswith("/api/topic-library"):
            user, error = self._require_user()
            if error:
                self._send_auth_failure(error, json_response=True)
                return
            self._handle_topic_library_api(path)
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
            self._call_scene(route["scenario"], route["spec"], overrides)
            return

        self._send_json({"error": "not_found", "path": path}, status=404)

    def _call_scene(self, scenario: dict[str, object], spec: dict[str, object], overrides: dict[str, str]) -> None:
        requested_at = time.time()
        client = KaipanlaCapturedClient()
        client.session.trust_env = False
        data = dict(spec.get("data") or {})
        params = dict(spec.get("params") or {})
        upstream_user_id = os.environ.get("KPL_UPSTREAM_USER_ID")
        upstream_token = os.environ.get("KPL_UPSTREAM_TOKEN")
        upstream_device_id = os.environ.get("KPL_UPSTREAM_DEVICE_ID")
        if upstream_user_id and data.get("UserID") in {None, "", "0"}:
            data["UserID"] = upstream_user_id
        if upstream_token and data.get("Token") in {None, "", "0"}:
            data["Token"] = upstream_token
        if upstream_device_id and data.get("DeviceID") in {None, "", "0"}:
            data["DeviceID"] = upstream_device_id

        for key, value in overrides.items():
            if key in params and key not in data:
                params[key] = value
            else:
                data[key] = value
        params["_ts"] = str(int(requested_at * 1000))

        try:
            response = client.request(spec, data=data, params=params)
        except Exception as exc:
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
