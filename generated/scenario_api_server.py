# -*- coding: utf-8 -*-
"""HTTP API wrapper for generated Kaipanla capture scenarios."""

from __future__ import annotations

import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from kaipanla_capture_client import KaipanlaCapturedClient, REQUESTS


ROOT = Path(__file__).resolve().parent
CLIENT_FILE = "kaipanla_capture_client.py"
PAGE_FILE = "capture_scenarios.html"


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

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        print("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format % args))

    def _handle_request(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path.rstrip("/") or "/")

        if path in {"/", "/index.html", f"/{PAGE_FILE}"}:
            self._serve_file(ROOT / PAGE_FILE, "text/html; charset=utf-8")
            return

        if path == f"/{CLIENT_FILE}":
            self._serve_file(ROOT / CLIENT_FILE, "text/plain; charset=utf-8")
            return

        if path == "/api/scenarios":
            self._send_json({"count": len(SCENARIOS), "scenarios": SCENARIOS})
            return

        if path not in ROUTES:
            self._send_json({"error": "not_found", "path": path}, status=404)
            return

        if self.command not in {"GET", "POST"}:
            self._send_json({"error": "method_not_allowed"}, status=405)
            return

        route = ROUTES[path]
        query_values = self._flatten_query(parse_qs(parsed.query, keep_blank_values=True))
        body_values = self._read_body_values()
        overrides = {**query_values, **body_values}
        self._call_scene(route["scenario"], route["spec"], overrides)

    def _call_scene(self, scenario: dict[str, object], spec: dict[str, object], overrides: dict[str, str]) -> None:
        client = KaipanlaCapturedClient()
        client.session.trust_env = False
        data = dict(spec.get("data") or {})
        params = dict(spec.get("params") or {})

        for key, value in overrides.items():
            if key in params and key not in data:
                params[key] = value
            else:
                data[key] = value

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
                "status_code": response.status_code,
                "content_type": content_type,
                "body": payload,
            }
        )

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
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: object, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
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
