# -*- coding: utf-8 -*-
"""Convert captured curl commands from a .bat export into a Kaipanla client."""

from __future__ import annotations

import argparse
import json
import keyword
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit


BUSINESS_HOSTS = {
    "applhb.longhuvip.com",
    "apphwhq.longhuvip.com",
    "apphis.longhuvip.com",
    "apparticle.longhuvip.com",
    "applog.longhuvip.com",
    "appuser.longhuvip.com",
    "getsockip.longhuvip.com",
}
STATIC_EXTENSIONS = {
    ".css",
    ".js",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ttf",
    ".ico",
    ".html",
    ".json",
}
SKIP_HEADERS = {"connection", "content-length", "host", "accept-encoding"}
SENSITIVE_DEFAULTS = {"Token": "0", "UserID": "0"}


@dataclass(frozen=True)
class CapturedRequest:
    session_id: str
    method: str
    url: str
    headers: tuple[tuple[str, str], ...]
    query: tuple[tuple[str, str], ...]
    form: tuple[tuple[str, str], ...]

    @property
    def controller(self) -> str:
        return _first_value(self.form, "c") or _first_value(self.query, "c") or "request"

    @property
    def action(self) -> str:
        return _first_value(self.form, "a") or _first_value(self.query, "a") or self.session_id


def _first_value(items: tuple[tuple[str, str], ...], key: str) -> str:
    for name, value in items:
        if name == key:
            return value
    return ""


def _safe_name(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z_]+", "_", value).strip("_").lower()
    value = re.sub(r"_+", "_", value)
    if not value:
        value = "request"
    if value[0].isdigit():
        value = f"request_{value}"
    if keyword.iskeyword(value):
        value = f"{value}_"
    return value


def _decode_curl_escaped(value: str) -> str:
    return value.replace("%%", "%")


def _normalize_items(items: list[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    normalized: list[tuple[str, str]] = []
    for name, value in items:
        normalized.append((name, SENSITIVE_DEFAULTS.get(name, value)))
    return tuple(normalized)


def _parse_headers(line: str) -> tuple[tuple[str, str], ...]:
    headers: list[tuple[str, str]] = []
    for name, value in re.findall(r'-H\s+"([^":]+):\s*([^"]*)"', line):
        if name.lower() in SKIP_HEADERS:
            continue
        headers.append((name, value))
    return tuple(headers)


def _parse_line(line: str) -> CapturedRequest | None:
    if "longhuvip.com" not in line:
        return None

    url_match = re.search(r'"(https?://[^" ]+)"', line)
    if not url_match:
        return None

    raw_url = _decode_curl_escaped(url_match.group(1))
    split_url = urlsplit(raw_url)
    if split_url.netloc not in BUSINESS_HOSTS:
        return None
    if any(split_url.path.lower().endswith(ext) for ext in STATIC_EXTENSIONS):
        return None

    base_url = f"{split_url.scheme}://{split_url.netloc}{split_url.path}"
    query = parse_qsl(split_url.query, keep_blank_values=True)
    body_match = re.search(r'--data-raw\s+"([^"]*)"', line)
    body = _decode_curl_escaped(body_match.group(1)) if body_match else ""
    form = parse_qsl(body, keep_blank_values=True)

    if not (dict(query).get("c") or dict(form).get("c") or split_url.netloc == "getsockip.longhuvip.com"):
        return None

    output_match = re.search(r"-o\s+(\d+)\.dat", line)
    session_id = output_match.group(1) if output_match else "0"
    method = "POST" if "-X POST" in line or body_match else "GET"
    return CapturedRequest(
        session_id=session_id,
        method=method,
        url=base_url,
        headers=_parse_headers(line),
        query=tuple(query),
        form=_normalize_items(form),
    )


def read_requests(path: Path) -> list[CapturedRequest]:
    requests: list[CapturedRequest] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        request = _parse_line(line)
        if request is not None:
            requests.append(request)
    return requests


def dedupe_requests(requests: list[CapturedRequest]) -> list[CapturedRequest]:
    unique: list[CapturedRequest] = []
    seen: set[tuple[object, ...]] = set()
    volatile_keys = {"DeviceID", "Token", "UserID", "StockID", "Time", "Day", "Index", "PreIndex"}
    for request in requests:
        normalized_form = tuple(sorted(
            (name, "<value>" if name in volatile_keys else value)
            for name, value in request.form
        ))
        normalized_query = tuple(sorted(
            (name, "<value>" if name in volatile_keys else value)
            for name, value in request.query
        ))
        key = (request.method, request.url, normalized_query, normalized_form)
        if key in seen:
            continue
        seen.add(key)
        unique.append(request)
    return unique


def build_function_name(request: CapturedRequest, used: set[str]) -> str:
    base = _safe_name(f"{request.controller}_{request.action}")
    name = base
    suffix = 2
    while name in used:
        name = f"{base}_{suffix}"
        suffix += 1
    used.add(name)
    return name


def _repr_dict(items: tuple[tuple[str, str], ...]) -> str:
    return json.dumps(dict(items), ensure_ascii=False, indent=4)


def _render_entry_field(name: str, value: str) -> str:
    return f"    {name!r}: {value.replace(chr(10), chr(10) + '    ')},"


def _method_signature(request: CapturedRequest) -> tuple[str, str]:
    override_names = {
        "StockID",
        "Time",
        "Day",
        "Index",
        "PreIndex",
        "index",
        "st",
        "Type",
        "Tsort",
        "View",
        "view",
        "Season",
        "Order",
        "Code",
    }
    names: list[str] = []
    original_by_name: dict[str, str] = {}
    for name, _ in request.form:
        if name not in override_names:
            continue
        py_name = _safe_name(name)
        if py_name not in names:
            names.append(py_name)
            original_by_name[py_name] = name
    signature = ", ".join(f"{name}=None" for name in names)
    signature = f", {signature}" if signature else ""
    overrides = [
        f"        if {name} is not None:\n"
        f"            data[{original_by_name[name]!r}] = str({name})"
        for name in names
    ]
    return signature, "\n".join(overrides) if overrides else "        pass"


def render_client(requests: list[CapturedRequest], source: Path) -> str:
    used: set[str] = set()
    entries: list[str] = []
    methods: list[str] = []
    request_names: list[str] = []

    for request in requests:
        function_name = build_function_name(request, used)
        entry_name = function_name.upper()
        request_names.append(entry_name)
        entries.append(
            f"{entry_name} = {{\n"
            f"    'session_id': {request.session_id!r},\n"
            f"    'method': {request.method!r},\n"
            f"    'url': {request.url!r},\n"
            f"{_render_entry_field('params', _repr_dict(request.query))}\n"
            f"{_render_entry_field('data', _repr_dict(request.form))}\n"
            f"{_render_entry_field('headers', _repr_dict(request.headers))}\n"
            f"}}"
        )
        signature, override_block = _method_signature(request)
        methods.append(
            f"    def {function_name}(self{signature}, **overrides):\n"
            f"        \"\"\"Replay session {request.session_id}: {request.controller}.{request.action}.\"\"\"\n"
            f"        data = dict({entry_name}['data'])\n"
            f"{override_block}\n"
            f"        data.update({{key: str(value) for key, value in overrides.items() if value is not None}})\n"
            f"        return self.request({entry_name}, data=data)\n"
        )

    return (
        "# -*- coding: utf-8 -*-\n"
        '"""\n'
        f"Python request client generated from {source.name}.\n\n"
        "It keeps deduplicated Kaipanla business requests from captured curl commands.\n"
        "Token/UserID defaults are sanitized; pass fresh values via method overrides.\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "import random\n"
        "import time\n\n"
        "import requests\n\n\n"
        "DEFAULT_TIMEOUT = 15\n"
        "DEFAULT_MIN_INTERVAL = 1.2\n"
        "DEFAULT_JITTER = 0.8\n\n\n"
        + "\n\n".join(entries)
        + "\n\n\nREQUESTS = [\n    "
        + ",\n    ".join(request_names)
        + "\n]\n\n\n"
        "class KaipanlaCapturedClient:\n"
        "    def __init__(self, timeout=DEFAULT_TIMEOUT, session=None, min_interval=DEFAULT_MIN_INTERVAL, jitter=DEFAULT_JITTER):\n"
        "        self.timeout = timeout\n"
        "        self.session = session or requests.Session()\n"
        "        self.min_interval = min_interval\n"
        "        self.jitter = jitter\n"
        "        self._last_request_at = 0.0\n\n"
        "    def _throttle(self):\n"
        "        wait = self.min_interval + random.uniform(0, self.jitter)\n"
        "        elapsed = time.monotonic() - self._last_request_at\n"
        "        if elapsed < wait:\n"
        "            time.sleep(wait - elapsed)\n"
        "        self._last_request_at = time.monotonic()\n\n"
        "    def request(self, spec, data=None, params=None, headers=None):\n"
        "        self._throttle()\n"
        "        merged_params = dict(spec.get('params') or {})\n"
        "        if params:\n"
        "            merged_params.update({key: str(value) for key, value in params.items() if value is not None})\n\n"
        "        merged_headers = dict(spec.get('headers') or {})\n"
        "        if headers:\n"
        "            merged_headers.update(headers)\n\n"
        "        response = self.session.request(\n"
        "            spec['method'],\n"
        "            spec['url'],\n"
        "            params=merged_params,\n"
        "            data=data if data is not None else spec.get('data'),\n"
        "            headers=merged_headers,\n"
        "            timeout=self.timeout,\n"
        "        )\n"
        "        response.raise_for_status()\n"
        "        return response\n\n"
        + "\n".join(methods)
        + "\n\nif __name__ == '__main__':\n"
        "    client = KaipanlaCapturedClient()\n"
        "    response = client.index_newgetlist()\n"
        "    print(response.status_code)\n"
        "    print(response.text[:500])\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bat_path", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("generated/kaipanla_capture_client.py"))
    args = parser.parse_args()

    requests = dedupe_requests(read_requests(args.bat_path))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_client(requests, args.bat_path), encoding="utf-8")
    print(f"Wrote {len(requests)} unique requests to {args.output}")


if __name__ == "__main__":
    main()
