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
    "five_level": ("local_hqstock", "hqStock", "2015"),
    "time_sales": ("local_hqstock", "hqStock", "2006"),
}


CORE_LOCAL_API_KEYS = {
    "five_level",
    "time_sales",
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
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)",
        },
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
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)",
        },
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
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)",
        },
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
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)",
        },
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
        if name in {"plate_factor_tags", "plate_factor_stock_list"}:
            self._apply_plate_factor_source(name, spec, data, overrides)
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
    def _apply_plate_factor_source(
        name: str,
        spec: dict[str, Any],
        data: dict[str, Any],
        overrides: dict[str, Any],
    ) -> None:
        date = str(overrides.get("Date") or overrides.get("date") or data.get("Date") or "").strip()
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
            data["Date"] = date

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
