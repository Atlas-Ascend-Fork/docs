# Copyright (c) 2026 Huawei Technologies Co., Ltd.
# This program is free software, you can redistribute it and/or modify it under the terms and conditions of
# CANN Open Software License Agreement Version 2.0 (the "License").
# Please refer to the License for details. You may not use this file except in compliance with the License.
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE in the root of the software repository for the full text of the License.
"""Exercise the complete requests client against temporary loopback HTTP pages."""

import importlib.util
import json
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

ROOT = next(parent for parent in Path(__file__).resolve().parents
            if (parent / "skills/md-review-skill/scripts/api_client.py").is_file())
SCRIPT = ROOT / "skills/md-review-skill/scripts/api_client.py"
SPEC = importlib.util.spec_from_file_location("docs_api_client", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


class PageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        page = int(parse_qs(parsed.query).get("page", ["1"])[0])
        pages = {1: [1, 2], 2: [3, 4], 3: [5]}
        items = pages.get(page, [])
        if parsed.path == "/short":
            items = [1]
        if parsed.path == "/empty":
            items = []
        if parsed.path == "/non-list" or (parsed.path == "/invalid-later" and page == 2):
            items = {"data": {"unexpected": True}}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        if parsed.path == "/more-header":
            self.send_header("total_page", "3")
        if parsed.path == "/complete-header":
            self.send_header("total_page", "1")
        self.end_headers()
        self.wfile.write(json.dumps(items).encode("utf-8"))

    def log_message(self, format_string, *arguments):
        pass


@pytest.fixture
def config_path(tmp_path):
    # The only network endpoint in these tests is this ephemeral local server.
    server = HTTPServer(("127.0.0.1", 0), PageHandler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps({"baseUrl": "http://127.0.0.1:" + str(server.server_port)})
    )
    try:
        yield path
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


@pytest.mark.parametrize("endpoint", ["/full", "/more-header"])
def test_capped_full_pages_are_explicitly_incomplete(config_path, endpoint):
    result = CLIENT.make_paginated_request(
        endpoint, config_path=str(config_path), per_page=2, max_pages=1
    )
    assert isinstance(result, dict), (
        "capped output must not look like a complete flat list"
    )
    assert result["incomplete"] is True
    assert result["data"] == [1, 2]
    assert result["next_page"] == 2
    assert result["error"]


def test_zero_page_budget_does_not_report_an_empty_complete_result(config_path):
    result = CLIENT.make_paginated_request(
        "/full", config_path=str(config_path), per_page=2, max_pages=0
    )
    assert isinstance(result, dict) and result["incomplete"] is True
    assert result["data"] == []
    assert result["next_page"] == 1  # First unread page, even with a zero request budget.
    assert result["max_pages"] == 0


def test_cli_capped_result_has_failure_status(config_path):
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "GET",
            "/full",
            "--config",
            str(config_path),
            "--paginate",
            "--per-page",
            "2",
            "--max-pages",
            "1",
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode != 0, result.stdout + result.stderr
    body = json.loads(result.stdout)
    assert body["incomplete"] is True and body["data"] == [1, 2]
    assert "[paginate] done:" not in result.stderr


@pytest.mark.parametrize(
    "endpoint, expected",
    [("/short", [1]), ("/empty", []), ("/complete-header", [1, 2])],
)
def test_verified_completion_keeps_flat_list_contract(config_path, endpoint, expected):
    assert (
        CLIENT.make_paginated_request(
            endpoint, config_path=str(config_path), per_page=2, max_pages=1
        )
        == expected
    )


def test_multiple_pages_keep_full_order(config_path):
    assert CLIENT.make_paginated_request(
        "/full", config_path=str(config_path), per_page=2, max_pages=3
    ) == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("endpoint,partial,next_page", [("/non-list", [], 1), ("/invalid-later", [1, 2], 2)])
def test_unexpected_page_is_not_misreported_as_a_page_limit(config_path, endpoint, partial, next_page):
    result = CLIENT.make_paginated_request(endpoint, config_path=str(config_path), per_page=2, max_pages=4)
    assert result["incomplete"] is True and result["data"] == partial
    assert result["next_page"] == next_page
    assert "Expected a list" in result["error"]
    assert "limit reached" not in result["error"].lower()


def test_first_page_handler_accepts_request_without_page(config_path):
    result = CLIENT.make_request("GET", "/full", config_path=str(config_path))
    assert result["data"] == [1, 2]
