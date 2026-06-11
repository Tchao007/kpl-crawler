# -*- coding: utf-8 -*-
"""Convert valid HTTP requests from a Fiddler .saz archive into Python code."""

from __future__ import annotations

import argparse
import json
import keyword
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, urlsplit


BUSINESS_HOSTS = {"applhb.longhuvip.com"}
SKIP_HEADERS = {
    "connection",
    "content-length",
    "host",
    "accept-encoding",
}


@dataclass(frozen=True)
class CapturedRequest:
    session_id: str
    method: str
    url: str
    headers: tuple[tuple[str, str], ...]
    query: tuple[tuple[str, str], ...]
    form: tuple[tuple[str, str], ...]
    body: str
    status_line: str

    @property
    def controller(self) -> str:
        return _first_value(self.form, "c") or _first_value(self.query, "c") or "request"

    @property
    def action(self) -> str:
        return _first_value(self.form, "a") or _first_value(self.query, "a") or self.session_id


def _first_value(items: Iterable[tuple[str, str]], key: str) -> str:
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


def _parse_raw_request(raw: bytes, session_id: str, status_line: str) -> CapturedRequest | None:
    text = raw.decode("utf-8", "replace")
    head, _, body = text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    if not lines:
        return None

    request_line = lines[0].split()
    if len(request_line) < 2:
        return None

    method, target = request_line[0], request_line[1]
    if method == "CONNECT":
        return None

    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        headers[name.strip()] = value.strip()

    host = headers.get("Host", "")
    if host not in BUSINESS_HOSTS:
        return None

    url = target if target.startswith(("http://", "https://")) else f"https://{host}{target}"
    split_url = urlsplit(url)
    base_url = f"{split_url.scheme}://{split_url.netloc}{split_url.path}"
    query = tuple(parse_qsl(split_url.query, keep_blank_values=True))
    form = tuple(parse_qsl(body, keep_blank_values=True))
    kept_headers = tuple(
        (name, value)
        for name, value in headers.items()
        if name.lower() not in SKIP_HEADERS
    )

    return CapturedRequest(
        session_id=session_id,
        method=method,
        url=base_url,
        headers=kept_headers,
        query=query,
        form=form,
        body=body,
        status_line=status_line,
    )


def read_requests(saz_path: Path) -> list[CapturedRequest]:
    requests: list[CapturedRequest] = []
    with zipfile.ZipFile(saz_path) as archive:
        client_files = sorted(
            name for name in archive.namelist() if re.fullmatch(r"raw/\d+_c\.txt", name)
        )
        for client_file in client_files:
            session_id = re.search(r"(\d+)_c\.txt$", client_file).group(1)
            server_file = f"raw/{session_id}_s.txt"
            status_line = ""
            if server_file in archive.namelist():
                response = archive.read(server_file).decode("utf-8", "replace")
                status_line = response.split("\r\n", 1)[0]
            captured = _parse_raw_request(archive.read(client_file), session_id, status_line)
            if captured is not None:
                requests.append(captured)
    return requests


def dedupe_requests(requests: Iterable[CapturedRequest]) -> list[CapturedRequest]:
    seen: set[tuple[object, ...]] = set()
    unique: list[CapturedRequest] = []
    volatile_keys = {"DeviceID", "Token", "UserID", "StockID", "Time", "Day"}

    for request in requests:
        normalized_form = tuple(sorted(
            (name, "<value>" if name in volatile_keys else value)
            for name, value in request.form
        ))
        key = (request.method, request.url, request.query, normalized_form)
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


def _repr_dict(items: tuple[tuple[str, str], ...], indent: int = 8) -> str:
    return json.dumps(dict(items), ensure_ascii=False, indent=4)


def _render_entry_field(name: str, value: str) -> str:
    return f"    {name!r}: {value.replace(chr(10), chr(10) + '    ')},"


def render_client(requests: list[CapturedRequest], source: Path) -> str:
    used: set[str] = set()
    entries: list[str] = []
    methods: list[str] = []

    for request in requests:
        function_name = build_function_name(request, used)
        entry_name = function_name.upper()
        entry = (
            f"{entry_name} = {{\n"
            f"    'session_id': {request.session_id!r},\n"
            f"    'method': {request.method!r},\n"
            f"    'url': {request.url!r},\n"
            f"{_render_entry_field('params', _repr_dict(request.query, 8))}\n"
            f"{_render_entry_field('data', _repr_dict(request.form, 8))}\n"
            f"{_render_entry_field('headers', _repr_dict(request.headers, 8))}\n"
            f"    'status_line': {request.status_line!r},\n"
            f"}}"
        )
        entries.append(entry)

        params = [
            name
            for name, _ in request.form
            if name in {"StockID", "Time", "Day", "Index", "index", "st", "Type", "Tsort", "FWebID"}
        ]
        seen_params: list[str] = []
        for param in params:
            py_name = _safe_name(param)
            if py_name not in seen_params:
                seen_params.append(py_name)
        signature = ", ".join(f"{name}=None" for name in seen_params)
        signature = f", {signature}" if signature else ""

        overrides = []
        for param in seen_params:
            original = next(name for name, _ in request.form if _safe_name(name) == param)
            overrides.append(
                f"        if {param} is not None:\n"
                f"            data[{original!r}] = str({param})"
            )
        override_block = "\n".join(overrides) if overrides else "        pass"
        method = (
            f"    def {function_name}(self{signature}, **overrides):\n"
            f"        \"\"\"Replay session {request.session_id}: {request.controller}.{request.action}.\"\"\"\n"
            f"        data = dict({entry_name}['data'])\n"
            f"{override_block}\n"
            f"        data.update({{key: str(value) for key, value in overrides.items() if value is not None}})\n"
            f"        return self.request({entry_name}, data=data)\n"
        )
        methods.append(method)

    entries_block = "\n\n".join(entries)
    methods_block = "\n".join(methods)
    request_names = ",\n    ".join(entry.split(" = ", 1)[0] for entry in entries)

    return (
        "# -*- coding: utf-8 -*-\n"
        '"""\n'
        f"Python request client generated from {source.name}.\n\n"
        "It keeps only business requests for applhb.longhuvip.com and drops duplicate\n"
        "polling calls found in the capture. Each method returns requests.Response;\n"
        "call response.json() or response.text to inspect the response body.\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "import requests\n\n\n"
        "DEFAULT_TIMEOUT = 15\n\n\n"
        f"{entries_block}\n\n\n"
        "REQUESTS = [\n"
        f"    {request_names}\n"
        "]\n\n\n"
        "class KaipanlaCapturedClient:\n"
        "    def __init__(self, timeout=DEFAULT_TIMEOUT, session=None):\n"
        "        self.timeout = timeout\n"
        "        self.session = session or requests.Session()\n\n"
        "    def request(self, spec, data=None, params=None, headers=None):\n"
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
        f"{methods_block}\n\n"
        "if __name__ == '__main__':\n"
        "    client = KaipanlaCapturedClient()\n"
        "    response = client.index_newgetlist()\n"
        "    print(response.status_code)\n"
        "    print(response.text[:500])\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("saz_path", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("generated/kaipanla_capture_client.py"))
    args = parser.parse_args()

    requests = dedupe_requests(read_requests(args.saz_path))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_client(requests, args.saz_path), encoding="utf-8")
    print(f"Wrote {len(requests)} unique requests to {args.output}")


if __name__ == "__main__":
    main()
