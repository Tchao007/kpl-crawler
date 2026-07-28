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


def test_plate_info_switches_to_history_by_date() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_info("801225", date="2026-06-25")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert call["data"]["c"] == "ZhiShuRanking"
    assert call["data"]["a"] == "GetPlate_Info_QJ"
    assert call["data"]["PlateID"] == "801225"
    assert call["data"]["Date"] == "2026-06-25"


def test_plate_children_history_adds_is_show() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_children("801225", date="2026-06-25")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert call["data"]["c"] == "ZhiShuRanking"
    assert call["data"]["a"] == "SonPlate_Info"
    assert call["data"]["PlateID"] == "801225"
    assert call["data"]["Date"] == "2026-06-25"
    assert call["data"]["IsShow"] == "1"


def test_plate_stock_factor_tags_history() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_stock_factor_tags("801225", date="2026-06-25")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert call["data"]["a"] == "GetGPCPHBTS_Tag"
    assert call["data"]["PlateID"] == "801225"
    assert call["data"]["Date"] == "2026-06-25"


def test_plate_real_ranking_keeps_variable_ranking_params() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_real_ranking(date="2026-06-25", ranking_type="2", zs_type="4", RStart="0925", REnd="1445")

    call = captured.calls[-1]
    assert call["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert call["data"]["c"] == "ZhiShuRanking"
    assert call["data"]["a"] == "RealRankingInfo"
    assert call["data"]["Date"] == "2026-06-25"
    assert call["data"]["Type"] == "2"
    assert call["data"]["ZSType"] == "4"
    assert call["data"]["RStart"] == "0925"
    assert call["data"]["REnd"] == "1445"


def test_plate_parent_uses_stock_id_parameter() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_parent("801225")

    call = captured.calls[-1]
    assert call["data"]["c"] == "ZhiShuL2Data"
    assert call["data"]["a"] == "GetParentPlateCode"
    assert call["data"]["StockID"] == "801225"


def test_new_plate_detail_helpers_from_latest_capture() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.plate_trend_incremental("803023", day="2026-07-27")
    client.plate_vol_tur_incremental("803023", day="2026-07-27")
    client.plate_art_title("803023")
    client.theme_info_bkr("803023")

    trend, vol_tur, art_title, info_bkr = captured.calls[-4:]
    assert trend["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert trend["data"]["c"] == "ZhiShuL2Data"
    assert trend["data"]["a"] == "GetTrendIncremental"
    assert trend["data"]["StockID"] == "803023"
    assert trend["data"]["Day"] == "2026-07-27"
    assert vol_tur["spec"]["url"] == "https://apphis.longhuvip.com/w1/api/index.php"
    assert vol_tur["data"]["c"] == "ZhiShuL2Data"
    assert vol_tur["data"]["a"] == "GetVolTurIncremental"
    assert vol_tur["data"]["Day"] == "2026-07-27"
    assert art_title["spec"]["url"] == "https://apphwhq.longhuvip.com/w1/api/index.php"
    assert art_title["data"]["c"] == "Index"
    assert art_title["data"]["a"] == "GetArtTitle"
    assert art_title["data"]["StockID"] == "803023"
    assert art_title["data"]["Type"] == "2"
    assert info_bkr["spec"]["url"] == "https://applhb.longhuvip.com/w1/api/index.php"
    assert info_bkr["data"]["c"] == "Theme"
    assert info_bkr["data"]["a"] == "InfoBKR"
    assert info_bkr["data"]["ZSCode"] == "803023"


def test_second_batch_core_helpers() -> None:
    captured = DummyCapturedClient()
    client = KaipanlaCoreClient(client=captured)

    client.conception_point()
    client.index_rqz_data()
    client.etf_stock_ranking(ranking_type="2", pid_type="3")
    client.index_change()

    conception, rqz, etf, index_change = captured.calls[-4:]
    assert conception["data"]["c"] == "ConceptionPoint"
    assert conception["data"]["a"] == "GetPoint"
    assert rqz["data"]["c"] == "Index"
    assert rqz["data"]["a"] == "GetRQZ_Data"
    assert etf["data"]["c"] == "NewStockRanking"
    assert etf["data"]["a"] == "ETFStockRanking"
    assert etf["data"]["Type"] == "2"
    assert etf["data"]["PidType"] == "3"
    assert index_change["data"]["c"] == "NewStockRanking"
    assert index_change["data"]["a"] == "IndexChange"
