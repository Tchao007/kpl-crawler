# -*- coding: utf-8 -*-
"""Small semantic client for reproduced Kaipanla core market APIs.

The raw captured client remains the source of truth for the recorded request
shape. This wrapper gives stable method names for the APIs we verified with
Frida SSL_read/SSL_write captures.
"""

from __future__ import annotations

import os
from typing import Any

from kaipanla_capture_client import KaipanlaCapturedClient, REQUESTS


SENSITIVE_DEFAULTS = {
    "UserID": "0",
    "Token": "0",
}


CORE_API_KEYS = {
    "module_versatile": ("apphwhq.longhuvip.com", "HomeDingPan", "ModuleVersatile"),
    "stock_plates": ("apphwhq.longhuvip.com", "StockL2Data", "GetStockIDPlate_New"),
    "stock_turnover_distribution": (
        "apphwhq.longhuvip.com",
        "StockL2Data",
        "GetStockPercentTurnoverTen",
    ),
    "large_orders": ("apphwhq.longhuvip.com", "StockL2Data", "GetWeiTuo"),
    "large_orders_page": ("apphwhq.longhuvip.com", "StockL2Data", "GetWeiTuo_W14"),
    "limit_up_gene": ("apphwhq.longhuvip.com", "StockL2Data", "GetZhangTingGene"),
    "today_kline": ("apphwhq.longhuvip.com", "StockLineData", "GetKLineToday_W14"),
    "limit_up_kline": ("apphwhq.longhuvip.com", "StockLineData", "GetKLineZhangTing"),
    "stock_dp_real": ("apphwhq.longhuvip.com", "StockYiDongKanPan", "StockDPRealData"),
    "stock_dp_explain": ("apphwhq.longhuvip.com", "StockYiDongKanPan", "StockDPExplain"),
    "xianhuo_list": ("apphwhq.longhuvip.com", "XianHuoData", "GetXianHuoList"),
    "plate_popup_config": ("apphwhq.longhuvip.com", "ZhiShuRanking", "PlateTCConfig"),
    "plate_factor_tags": ("apphwhq.longhuvip.com", "ConceptionPoint", "BKFenShiZhiBo"),
    "plate_factor_stock_list": ("apphwhq.longhuvip.com", "ZhiShuRanking", "ZhiShuStockList_W8"),
    "plate_info": ("apphwhq.longhuvip.com", "ZhiShuRanking", "GetPlate_Info_QJ"),
    "plate_children": ("apphwhq.longhuvip.com", "ZhiShuRanking", "SonPlate_Info"),
    "plate_stock_factor_tags": ("apphwhq.longhuvip.com", "ZhiShuRanking", "GetGPCPHBTS_Tag"),
    "plate_real_ranking": ("apphis.longhuvip.com", "ZhiShuRanking", "RealRankingInfo"),
    "plate_parent": ("apphwhq.longhuvip.com", "ZhiShuL2Data", "GetParentPlateCode"),
    "plate_trend_incremental": ("apphwhq.longhuvip.com", "ZhiShuL2Data", "GetTrendIncremental"),
    "plate_vol_tur_incremental": ("apphwhq.longhuvip.com", "ZhiShuL2Data", "GetVolTurIncremental"),
    "plate_art_title": ("apphwhq.longhuvip.com", "Index", "GetArtTitle"),
    "theme_info_bkr": ("applhb.longhuvip.com", "Theme", "InfoBKR"),
    "conception_point": ("apphwhq.longhuvip.com", "ConceptionPoint", "GetPoint"),
    "index_rqz_data": ("apphwhq.longhuvip.com", "Index", "GetRQZ_Data"),
    "etf_stock_ranking": ("apphwhq.longhuvip.com", "NewStockRanking", "ETFStockRanking"),
    "index_change": ("apphwhq.longhuvip.com", "NewStockRanking", "IndexChange"),
    "five_level": ("local_hqstock", "hqStock", "2015"),
    "time_sales": ("local_hqstock", "hqStock", "2006"),
}


CORE_LOCAL_API_KEYS = {
    "five_level",
    "time_sales",
}


PLATE_HISTORY_SOURCE_KEYS = {
    "plate_factor_tags",
    "plate_factor_stock_list",
    "plate_info",
    "plate_children",
    "plate_stock_factor_tags",
    "plate_real_ranking",
    "plate_trend_incremental",
    "plate_vol_tur_incremental",
}


COMMON_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)",
}


COMMON_FORM_FIELDS = {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
}


CORE_FALLBACK_SPECS: dict[str, dict[str, Any]] = {
    "large_orders_page": {
        "session_id": "core_large_orders_page",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            "a": "GetWeiTuo_W14",
            "st": "50",
            "c": "StockL2Data",
            "PhoneOSNew": "1",
            "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
            "VerSion": "5.23.0.4",
            "Token": "0",
            "Tur": "30",
            "apiv": "w44",
            "Type": "2",
            "Vol": "500",
            "StockID": "001399",
            "UserID": "0",
            "VType": "1",
            "VOrder": "0",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_popup_config": {
        "session_id": "core_plate_popup_config",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            "a": "PlateTCConfig",
            "apiv": "w44",
            "c": "ZhiShuRanking",
            "PhoneOSNew": "1",
            "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
            "VerSion": "5.23.0.4",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_factor_tags": {
        "session_id": "core_plate_factor_tags",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            "a": "BKFenShiZhiBo",
            "apiv": "w44",
            "c": "ConceptionPoint",
            "PhoneOSNew": "1",
            "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
            "VerSion": "5.23.0.4",
            "Date": "",
            "PlateID": "801612",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_factor_stock_list": {
        "session_id": "core_plate_factor_stock_list",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            "a": "ZhiShuStockList_W8",
            "apiv": "w44",
            "c": "ZhiShuRanking",
            "PhoneOSNew": "1",
            "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
            "VerSion": "5.23.0.4",
            "Index": "0",
            "IsKZZType": "0",
            "IsZZ": "0",
            "Order": "1",
            "PlateID": "801612",
            "TSZB": "17",
            "Type": "42",
            "old": "1",
            "st": "30",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_info": {
        "session_id": "core_plate_info",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetPlate_Info_QJ",
            "c": "ZhiShuRanking",
            "Date": "",
            "PlateID": "801225",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_children": {
        "session_id": "core_plate_children",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "SonPlate_Info",
            "c": "ZhiShuRanking",
            "PlateID": "801225",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_stock_factor_tags": {
        "session_id": "core_plate_stock_factor_tags",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetGPCPHBTS_Tag",
            "c": "ZhiShuRanking",
            "Date": "",
            "PlateID": "801225",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_real_ranking": {
        "session_id": "core_plate_real_ranking",
        "method": "POST",
        "url": "https://apphis.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "RealRankingInfo",
            "c": "ZhiShuRanking",
            "Date": "",
            "Index": "0",
            "Order": "1",
            "Type": "1",
            "ZSType": "7",
            "st": "30",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_parent": {
        "session_id": "core_plate_parent",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetParentPlateCode",
            "c": "ZhiShuL2Data",
            "StockID": "801225",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_trend_incremental": {
        "session_id": "core_plate_trend_incremental",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetTrendIncremental",
            "c": "ZhiShuL2Data",
            "StockID": "803023",
            "Day": "",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_vol_tur_incremental": {
        "session_id": "core_plate_vol_tur_incremental",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetVolTurIncremental",
            "c": "ZhiShuL2Data",
            "StockID": "803023",
            "Day": "",
        },
        "headers": COMMON_HEADERS,
    },
    "plate_art_title": {
        "session_id": "core_plate_art_title",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetArtTitle",
            "c": "Index",
            "Type": "2",
            "StockID": "803023",
            "Token": "0",
            "UserID": "0",
        },
        "headers": COMMON_HEADERS,
    },
    "theme_info_bkr": {
        "session_id": "core_theme_info_bkr",
        "method": "POST",
        "url": "https://applhb.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "InfoBKR",
            "c": "Theme",
            "ZSCode": "803023",
            "Token": "0",
            "UserID": "0",
        },
        "headers": COMMON_HEADERS,
    },
    "conception_point": {
        "session_id": "core_conception_point",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetPoint",
            "c": "ConceptionPoint",
        },
        "headers": COMMON_HEADERS,
    },
    "index_rqz_data": {
        "session_id": "core_index_rqz_data",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "GetRQZ_Data",
            "c": "Index",
        },
        "headers": COMMON_HEADERS,
    },
    "etf_stock_ranking": {
        "session_id": "core_etf_stock_ranking",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "ETFStockRanking",
            "c": "NewStockRanking",
            "Index": "0",
            "Order": "1",
            "PidType": "2",
            "Type": "1",
            "st": "30",
        },
        "headers": COMMON_HEADERS,
    },
    "index_change": {
        "session_id": "core_index_change",
        "method": "POST",
        "url": "https://apphwhq.longhuvip.com/w1/api/index.php",
        "params": {},
        "data": {
            **COMMON_FORM_FIELDS,
            "a": "IndexChange",
            "c": "NewStockRanking",
        },
        "headers": COMMON_HEADERS,
    },
}


def _host_from_url(url: str) -> str:
    return url.split("//", 1)[-1].split("/", 1)[0]


def _index_specs() -> dict[tuple[str, str, str], dict[str, Any]]:
    index: dict[tuple[str, str, str], dict[str, Any]] = {}
    for spec in REQUESTS:
        data = spec.get("data") or {}
        key = (_host_from_url(str(spec.get("url", ""))), str(data.get("c", "")), str(data.get("a", "")))
        index.setdefault(key, spec)
    return index


SPEC_BY_KEY = _index_specs()


def _core_spec(name: str) -> dict[str, Any]:
    if name in CORE_LOCAL_API_KEYS:
        raise KeyError(f"Core API {name} is decoded locally and has no HTTP replay spec")
    key = CORE_API_KEYS[name]
    spec = SPEC_BY_KEY.get(key) or CORE_FALLBACK_SPECS.get(name)
    if spec is None:
        raise KeyError(f"Core API spec not found for {name}: {key}")
    return spec


class KaipanlaCoreClient:
    """Replays verified Kaipanla market APIs with environment-backed auth."""

    def __init__(self, *, client: KaipanlaCapturedClient | None = None) -> None:
        self.client = client or KaipanlaCapturedClient()
        self.client.session.trust_env = False

    def request_core(self, name: str, **overrides: Any):
        spec = dict(_core_spec(name))
        data = dict(spec.get("data") or {})
        params = dict(spec.get("params") or {})
        if name in PLATE_HISTORY_SOURCE_KEYS:
            self._apply_plate_history_source(name, spec, data, overrides)
        self._apply_env_auth(data)
        for key, value in overrides.items():
            if value is None:
                continue
            if key in params and key not in data:
                params[key] = str(value)
            else:
                data[key] = str(value)
        return self.client.request(spec, data=data, params=params)

    @staticmethod
    def _apply_plate_history_source(
        name: str,
        spec: dict[str, Any],
        data: dict[str, Any],
        overrides: dict[str, Any],
    ) -> None:
        date = str(
            overrides.get("Date")
            or overrides.get("date")
            or overrides.get("Day")
            or overrides.get("day")
            or data.get("Date")
            or data.get("Day")
            or ""
        ).strip()
        if name == "plate_factor_tags":
            if date:
                spec["url"] = "https://apphis.longhuvip.com/w1/api/index.php"
                data["c"] = "HisConceptionPoint"
                data["Date"] = date
            else:
                data["c"] = "ConceptionPoint"
                data["Date"] = ""
            return
        if date:
            spec["url"] = "https://apphis.longhuvip.com/w1/api/index.php"
            if "Day" in data and "Date" not in data:
                data["Day"] = date
            else:
                data["Date"] = date
            if name == "plate_children":
                data.setdefault("IsShow", "1")
        elif "Date" in data:
            data["Date"] = ""
        elif "Day" in data:
            data["Day"] = ""

    @staticmethod
    def _apply_env_auth(data: dict[str, Any]) -> None:
        env_map = {
            "UserID": "KPL_UPSTREAM_USER_ID",
            "Token": "KPL_UPSTREAM_TOKEN",
            "DeviceID": "KPL_UPSTREAM_DEVICE_ID",
        }
        for key, env_name in env_map.items():
            env_value = os.environ.get(env_name)
            if env_value and data.get(key) in {None, "", "0"}:
                data[key] = env_value

    def module_versatile(self, **overrides: Any):
        return self.request_core("module_versatile", **overrides)

    def stock_plates(self, stock_id: str, **overrides: Any):
        return self.request_core("stock_plates", StockID=stock_id, **overrides)

    def stock_turnover_distribution(self, stock_id: str, **overrides: Any):
        return self.request_core("stock_turnover_distribution", StockID=stock_id, **overrides)

    def large_orders(self, stock_id: str, **overrides: Any):
        return self.request_core("large_orders", StockID=stock_id, **overrides)

    def large_orders_page(self, stock_id: str, **overrides: Any):
        return self.request_core("large_orders_page", StockID=stock_id, **overrides)

    def limit_up_gene(self, stock_id: str, **overrides: Any):
        return self.request_core("limit_up_gene", StockID=stock_id, **overrides)

    def today_kline(self, stock_id: str, **overrides: Any):
        return self.request_core("today_kline", StockID=stock_id, **overrides)

    def limit_up_kline(self, stock_id: str, **overrides: Any):
        return self.request_core("limit_up_kline", StockID=stock_id, **overrides)

    def stock_dp_real(self, stock_id: str, **overrides: Any):
        return self.request_core("stock_dp_real", StockID=stock_id, **overrides)

    def stock_dp_explain(self, stock_id: str, **overrides: Any):
        return self.request_core("stock_dp_explain", StockID=stock_id, **overrides)

    def xianhuo_list(self, **overrides: Any):
        return self.request_core("xianhuo_list", **overrides)

    def plate_popup_config(self, **overrides: Any):
        return self.request_core("plate_popup_config", **overrides)

    def plate_factor_tags(self, plate_id: str, date: str | None = None, **overrides: Any):
        return self.request_core("plate_factor_tags", PlateID=plate_id, Date=date, **overrides)

    def plate_factor_stock_list(
        self,
        plate_id: str,
        *,
        tszb: str = "17",
        factor_type: str = "42",
        order: str = "1",
        date: str | None = None,
        **overrides: Any,
    ):
        return self.request_core(
            "plate_factor_stock_list",
            PlateID=plate_id,
            TSZB=tszb,
            Type=factor_type,
            Order=order,
            Date=date,
            **overrides,
        )

    def plate_info(self, plate_id: str, date: str | None = None, **overrides: Any):
        return self.request_core("plate_info", PlateID=plate_id, Date=date, **overrides)

    def plate_children(self, plate_id: str, date: str | None = None, **overrides: Any):
        return self.request_core("plate_children", PlateID=plate_id, Date=date, **overrides)

    def plate_stock_factor_tags(self, plate_id: str, date: str | None = None, **overrides: Any):
        return self.request_core("plate_stock_factor_tags", PlateID=plate_id, Date=date, **overrides)

    def plate_real_ranking(
        self,
        *,
        date: str | None = None,
        ranking_type: str = "1",
        zs_type: str = "7",
        order: str = "1",
        index: str = "0",
        st: str = "30",
        **overrides: Any,
    ):
        return self.request_core(
            "plate_real_ranking",
            Date=date,
            Type=ranking_type,
            ZSType=zs_type,
            Order=order,
            Index=index,
            st=st,
            **overrides,
        )

    def plate_parent(self, plate_id: str, **overrides: Any):
        return self.request_core("plate_parent", StockID=plate_id, **overrides)

    def plate_trend_incremental(self, plate_id: str, day: str | None = None, **overrides: Any):
        return self.request_core("plate_trend_incremental", StockID=plate_id, Day=day, **overrides)

    def plate_vol_tur_incremental(self, plate_id: str, day: str | None = None, **overrides: Any):
        return self.request_core("plate_vol_tur_incremental", StockID=plate_id, Day=day, **overrides)

    def plate_art_title(self, plate_id: str, art_type: str = "2", **overrides: Any):
        return self.request_core("plate_art_title", StockID=plate_id, Type=art_type, **overrides)

    def theme_info_bkr(self, zs_code: str, **overrides: Any):
        return self.request_core("theme_info_bkr", ZSCode=zs_code, **overrides)

    def conception_point(self, **overrides: Any):
        return self.request_core("conception_point", **overrides)

    def index_rqz_data(self, **overrides: Any):
        return self.request_core("index_rqz_data", **overrides)

    def etf_stock_ranking(
        self,
        *,
        ranking_type: str = "1",
        order: str = "1",
        index: str = "0",
        st: str = "30",
        pid_type: str = "2",
        **overrides: Any,
    ):
        return self.request_core(
            "etf_stock_ranking",
            Type=ranking_type,
            Order=order,
            Index=index,
            st=st,
            PidType=pid_type,
            **overrides,
        )

    def index_change(self, **overrides: Any):
        return self.request_core("index_change", **overrides)
