#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
if str(GENERATED) not in sys.path:
    sys.path.insert(0, str(GENERATED))

from kpl_core_client import KaipanlaCoreClient  # noqa: E402


class DummySession:
    trust_env = True


class DummyCapturedClient:
    def __init__(self) -> None:
        self.session = DummySession()
        self.calls: list[dict[str, object]] = []

    def request(self, spec, *, data=None, params=None):
        self.calls.append({"spec": spec, "data": data or {}, "params": params or {}})
        return {"ok": True}


def test_plate_factor_tags_realtime_uses_conception_point() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_factor_tags("801612")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphwhq.longhuvip.com/w1/api/index.php"
    assert call["data"]["c"] == "ConceptionPoint"
    assert call["data"]["a"] == "BKFenShiZhiBo"
    assert call["data"]["PlateID"] == "801612"
    assert call["data"]["Date"] == ""


def test_plate_factor_tags_history_uses_his_conception_point() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_factor_tags("801612", date="2026-07-27")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert call["data"]["c"] == "HisConceptionPoint"
    assert call["data"]["a"] == "BKFenShiZhiBo"
    assert call["data"]["PlateID"] == "801612"
    assert call["data"]["Date"] == "2026-07-27"


def test_plate_factor_stock_list_defaults_to_renqi_jizeng() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_factor_stock_list("801612", date="2026-07-27")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert call["data"]["c"] == "ZhiShuRanking"
    assert call["data"]["a"] == "ZhiShuStockList_W8"
    assert call["data"]["PlateID"] == "801612"
    assert call["data"]["TSZB"] == "17"
    assert call["data"]["Type"] == "42"
    assert call["data"]["Order"] == "1"
    assert call["data"]["Date"] == "2026-07-27"
