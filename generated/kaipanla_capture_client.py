# -*- coding: utf-8 -*-
"""
Python request client generated from kpl.bat.

It keeps deduplicated Kaipanla business requests from captured curl commands.
Token/UserID defaults are sanitized; pass fresh values via method overrides.
"""

from __future__ import annotations

import random
import time

import requests


DEFAULT_TIMEOUT = 15
DEFAULT_MIN_INTERVAL = 1.2
DEFAULT_JITTER = 0.8


USERINFO_APPNEWS = {
    'session_id': '1',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "AppNews",
        "st": "1",
        "c": "UserInfo",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PhoneOS": "0",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "Version": "5.23.0.4",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

THEME_INFOGR = {
    'session_id': '2',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "InfoGR",
        "UserID": "0",
        "apiv": "w44",
        "c": "Theme",
        "VerSion": "5.23.0.4",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATASTATISTICS_USERLOGIN = {
    'session_id': '4',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "UserLogin",
        "apiv": "w44",
        "c": "DataStatistics",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "UserID": "0",
        "VerSion": "5.23.0.4",
        "PhoneOS": "1",
        "ClientSign": "7149b54c70608759a9c17d59aa9c65eb"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

USERINFO_USERNEWS3 = {
    'session_id': '7',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "UserNews3",
        "st": "1",
        "c": "UserInfo",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PhoneOS": "0",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "Version": "5.23.0.4",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

SYSTEM_ADGET = {
    'session_id': '10',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "AdGet",
        "apiv": "w44",
        "Type": "1",
        "c": "System",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Scale": "0.5625"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

XIANHUODATA_GETXIANHUOLIST = {
    'session_id': '14',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetXianHuoList",
        "apiv": "w44",
        "c": "XianHuoData",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Time": "1781508445"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

COMMENTS_USERLISTNEW = {
    'session_id': '15',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "UserListNew",
        "c": "Comments",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

USERSELECTSTOCK_UPDATESTATE = {
    'session_id': '19',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "UpdateState",
        "UserID": "0",
        "apiv": "w44",
        "c": "UserSelectStock",
        "VerSion": "5.23.0.4",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

REQUEST_23 = {
    'session_id': '23',
    'method': 'GET',
    'url': 'https://getsockip.longhuvip.com/getIPList',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "UserID": "7764559",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "e43352fb3435c5f1fa9ac40cb69b4956",
        "deviceId": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'data': {},
    'headers': {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_GETINFO = {
    'session_id': '52',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "GetInfo",
        "View": "2,3,4,5,7,8,9,10,11",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

SYSAPPVERSION_GETLAYOUT = {
    'session_id': '53',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "SysAppVersion",
        "a": "GetLaYout",
        "apiv": "w44",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

INDEX_NEWGETLIST = {
    'session_id': '54',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "NewGetList",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

INDEXPLATE_GETINDEXLIST = {
    'session_id': '56',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "IndexPlate",
        "a": "GetIndexList",
        "view": "1,2,3",
        "st": "2",
        "Type": "0",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

STOCKLINEDATA_GETKLINEDAY_W14 = {
    'session_id': '108',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "st": "135",
        "a": "GetKLineDay_W14",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "Type": "d",
        "StockID": "SH000001",
        "UserID": "0",
        "Is_FS": "1"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKLINEDATA_GETKLINETODAY_W14 = {
    'session_id': '111',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetKLineToday_W14",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "d",
        "StockID": "SH000001",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HOMEDINGPAN_MODULEVERSATILE = {
    'session_id': '112',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ModuleVersatile",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

TASK_USEFUN = {
    'session_id': '119',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "UseFun",
        "UserID": "0",
        "apiv": "w44",
        "c": "Task",
        "VerSion": "5.23.0.4",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

USERSELECTSTOCK_GETALLUSERSELSTOCK = {
    'session_id': '120',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetAllUserSelStock",
        "c": "UserSelectStock",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ADMIN_L2DATESHOWHID = {
    'session_id': '121',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "L2DateShowHid",
        "UserID": "0",
        "apiv": "w44",
        "c": "Admin",
        "VerSion": "5.23.0.4",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_TOPTITLE = {
    'session_id': '122',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "TopTitle",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANGDONGCAI_GETSTATE = {
    'session_id': '123',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetState",
        "c": "LongHuBangDongCai",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_GETSTOCKLIST = {
    'session_id': '126',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "st": "500",
        "a": "GetStockList",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Time": "",
        "Index": "0",
        "apiv": "w44",
        "Type": "2",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_ADD = {
    'session_id': '128',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "Add",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Time": "2026-06-15",
        "apiv": "w44",
        "StockID": "603335"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCK_GETSTOCKCHART = {
    'session_id': '146',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Stock",
        "a": "GetStockChart",
        "StockID": "600497",
        "Index": "0",
        "st": "530",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

STOCK_GETNEWONESTOCKINFO = {
    'session_id': '147',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Stock",
        "a": "GetNewOneStockInfo",
        "Type": "0",
        "Time": "2026-06-15",
        "StockID": "600497",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

COMMENTS_GET = {
    'session_id': '159',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Comments",
        "a": "Get",
        "Index": "0",
        "st": "30",
        "StockID": "600497",
        "Day": "2026-06-15",
        "Type": "1",
        "Tsort": "0",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

STOCK_GETNEWONESTOCKINFO_2 = {
    'session_id': '193',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Stock",
        "a": "GetNewOneStockInfo",
        "Type": "1",
        "Time": "3",
        "StockID": "603335",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

DATASTATISTICS_CALUSERCLICK = {
    'session_id': '194',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "DataStatistics",
        "a": "CalUserClick",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Param0": "290",
        "Param1": "603335",
        "UserID": "0",
        "Token": "0"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

STOCKL2DATA_GETSTOCKTREND = {
    'session_id': '196',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "StockL2Data",
        "a": "GetStockTrend",
        "StockID": "603335",
        "Day": "20260615",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

DATASTATISTICS_CALUSERCLICK_2 = {
    'session_id': '197',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "DataStatistics",
        "a": "CalUserClick",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Param0": "291",
        "Param1": "603335",
        "UserID": "0",
        "Token": "0"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

STOCK_YYBTTEND = {
    'session_id': '199',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Stock",
        "a": "YYBTtend",
        "LogID": "2026061560333501119427",
        "type": "1",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

SYSTEM_MODULESWITCH = {
    'session_id': '200',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ModuleSwitch",
        "c": "System",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATABATCHSTATISTICS_CALUSERCLICK = {
    'session_id': '209',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "CalUserClick",
        "DataList": "[{\"U\":\"0\",\"Ct\":1781537137,\"P0\":488},{\"U\":\"0\",\"Ct\":1781537137,\"P0\":486},{\"U\":\"0\",\"Ct\":1781537144,\"P0\":536},{\"U\":\"0\",\"Ct\":\"1781537166,1781537174\",\"P0\":543},{\"U\":\"0\",\"Ct\":1781537177,\"P0\":542},{\"U\":\"0\",\"Ct\":1781537197,\"P0\":537},{\"U\":\"7764559\",\"Ct\":\"1781537395,1781537395,1781537395,1781537395,1781537395\",\"P0\":260},{\"U\":\"7764559\",\"Ct\":1781537420,\"P0\":217},{\"U\":\"7764559\",\"Ct\":1781537427,\"P0\":155,\"P1\":\"603335\"}]",
        "apiv": "w44",
        "c": "DataBatchStatistics",
        "PhoneOSNew": "1",
        "Version": "5.23.0.4",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PhoneOS": "1",
        "ChannelID": "129",
        "ClientSign": "8a92a0d46d8122a964b9d97db347c19b"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LOG_LOGUSERADDNEW = {
    'session_id': '210',
    'method': 'POST',
    'url': 'https://appuser.longhuvip.com/index.php',
    'params': {},
    'data': {
        "a": "LogUserAddNew",
        "apiv": "w44",
        "c": "Log",
        "PhoneOSNew": "1",
        "log": "eJztWM1u00AQfhXLvrSS5fzZsVOJQxsEqtRCaBEgtVW0sTfJEmfXsjdNo6oSKkKFCjghUAUS9IJQT1wRKjxN2vQt2LXdJrGd/kFLQc3B3szOrr+Zb2Z27IVVEUMqTohZURYddpekaWzBlVsuqDUhptLBxqu9t1+7m596u7uRqd72y72nzxbxLHAbkHoS/yFM2VSZdhxYdoiHKCL4Rlo+GuqyZ7rEth8xoVSyAYX97TZ2Dp686K1vL+IScWmV2IhI0m2XtJxpi6sPDOehDU0KrXlKzEaxjmyrD/jHVm/r9d7nD4u4WAduiKv3c2f/zcfu5ntmpsntNElTAajTUhoAOQDbQMGwjbh9SgspTYCwMssukyZFy4h22LJKjfkpoxsZLadnCnoma8gitPoyNWukjZws2shjwoXV2IJcenhBrqCpRiZwO9ufs6CdE550vH41dI4yRKC4Jg+DzBUy+WwMZCDjoEZHRgg/e174BBdtZDbGHiDYFpbZZTzF5x+yJaSdKhI/qtiTm3AGdEiLLqSXJIAtlyBrwgxmU3OQhRNaHtBIRVb4AMqhftn25akho5hWagZhCNyBXUrULdrA85AZ2c8lhJZdWHWhVz/cbrRKtVzlc0k4Y4+8D1co9wX/k0CTpupaPJa4LE5TJEv/AFN1aDagxZIL16A1drfymKWiQPybLMwBCxE/UwX3aCgLrC4IZrBw2rpAciuEUqd5SEYfTF/DR1XjstSk4xRJ0wHU15tqUUrwgCIEVpmCSpL/tWwhkvwZwyjkLzyXPQpc6PCyqQTXweQeKqeJqHNXFfUMq5lHEXumQyTRzrz6t+2c58OTCUkEql8BQo5HnRRGIeozcfefhJxvfxKTauCTk/uc66p82qrshZ1f2eOtXxIVhXSUimw6rxoXlVSBMj8s2FkxFGZDTerIhOKIo00Xl2lhZ9jvei8TuwNq0FWOabMHuvFEkzj8UST8iyYx+LlYwx/IOPCzvJBcJ/tpk92ux7sv7vV8LsqEbmjpCz82TZ8+JWBxdEJzgLESdCkAB8P9DmyfBqh2xT2pR3uNSwXoHzIhzKEynk4AqxuqHgerho3R4BeI30r/30DNSse9FqEg8rId1IYgYUvEk4WbHQyayPR1pyDAgr89H41L3efvettf9te/dTe+i2tLa0u/AApQTmU=",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "net": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCK_YYBTTEND_2 = {
    'session_id': '211',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Stock",
        "a": "YYBTtend",
        "LogID": "2026061560333501220959",
        "type": "1",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

STOCK_GETNEWESTDAY = {
    'session_id': '213',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Stock",
        "a": "GetNewestDay",
        "StockID": "603335",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

LONGHUBANG_UPDATELIST = {
    'session_id': '214',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "UpdateList",
        "apiv": "w44",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKMESSAGEBAR_MESSAGEBARINFO = {
    'session_id': '215',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "MessageBarInfo",
        "apiv": "w44",
        "c": "StockMessageBar",
        "StockID": "603335",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKL2DATA_GETZHANGTINGGENE = {
    'session_id': '216',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetZhangTingGene",
        "c": "StockL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "603335"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKL2DATA_GETSTOCKIDPLATE_NEW = {
    'session_id': '217',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetStockIDPlate_New",
        "c": "StockL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "isT": "1",
        "apiv": "w44",
        "StockID": "603335",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_GETARTTITLE = {
    'session_id': '218',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetArtTitle",
        "UserID": "0",
        "apiv": "w44",
        "Type": "1",
        "c": "Index",
        "VerSion": "5.23.0.4",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "StockID": "603335",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATABATCHSTATISTICS_CALUSERPAGE = {
    'session_id': '265',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "CalUserPage",
        "DataList": "[{\"U\":\"0\",\"S\":0,\"Ct\":1781537141,\"P0\":2},{\"U\":\"0\",\"S\":\"0,0\",\"Ct\":\"1781537144,1781537177\",\"P0\":1},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537197,\"P0\":1},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537395,\"P0\":2},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537418,\"P0\":97},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537418,1781537485\",\"P0\":92},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537420,\"P0\":33},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537427,1781537461\",\"P0\":51},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537427,1781537461\",\"P0\":5},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537447,1781537459\",\"P0\":8},{\"U\":\"7764559\",\"S\":\"603,2,301,688,301,0\",\"Ct\":\"1781537450,1781537452,1781537453,1781537454,1781537456,1781537458\",\"P0\":32},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537493,\"P0\":93}]",
        "apiv": "w44",
        "c": "DataBatchStatistics",
        "PhoneOSNew": "1",
        "Version": "5.23.0.4",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PhoneOS": "1",
        "ChannelID": "129",
        "ClientSign": "091747035a0c44aba4ad3ea8d182f145"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LOG_LOGUSERADDNEW_2 = {
    'session_id': '267',
    'method': 'POST',
    'url': 'https://appuser.longhuvip.com/index.php',
    'params': {},
    'data': {
        "a": "LogUserAddNew",
        "apiv": "w44",
        "c": "Log",
        "PhoneOSNew": "1",
        "log": "eJztWt1u40QUfhXk3oCUOmM7/qsUoW0LqGKLFlrgoqmiiT2bjGp7vM6kadX2EroSVFwti8Qiwd6vhIRAQkI8DW3pWzDjnzaJ7TZpksYrfBOrM3PmnO+cOd/Mmc7OkeAhKqwIslARfPb1YRt9Al1Ut4grQnzYE/cg9qHnQNFDfezZ6EC0OjCgXdFGFGKnK25RYu2tR388sijex/SwEiCLBPYMZjqOZvrggAawftTlI5oO7tKmT7qYYuLVZbMy0GxDiuoykLVloC1L6mBXL3DqHUr97kq1Cn2fQxUd4rU7vX3si8zMar9Wq/ZRqzpoiNihrvP+1sZ6vXKy5IY9G3ZdA4qiqMfu+rC6Y/fzKZUMqgA1U5+rCgBkU5PnoeKoITjEaggrDSFyVUOoNAR0ELacPz+9OHv973evzs9eXPx8evnm74ZwMjsRh7SxHTZySECT1KgTSJJk1mQ9HEQPfcTGSKMqzp9/ffHyj3/+/PX87Pv7qJBlYKrmDFQkIl/9dvXyzcW3p+d/vbj65fern15zkUGvfxjAtos8unR8+eqbyx9/OGapbPFcni7x2CytNqMGSTckVdGZ3wxNqwjIHmirGcyhFYFnl7Cyc5QS0PVRAd0ASsQ0808lhoBTmzobfyzdT/w6Og/AHcJJJR0DA2TEoJaKwZy4prgxmBfgzBgoY8RgbmRc1BjMD3AqBoqqKGY+F02+9cQ+lROfMmOGSLnZ7WNqdbZhuwkdJ8MgHai1BRm0TzINksDEBs1yp70TgNVB1t4m9la30tbXAFM5O+sn38Sntl6+72LIOh/cbY1DuuijHrY3VzPM0XUznSxhG5/srrPHkOYpuYZ4aw629t79AqP+O/vs573qJsTel2wG0q+uEY8y5cwIFz2Gh6RHd8DuEvTsgGB7xYp6q58hB7LpBkZUH2MPwWCgIaIk7ylZJZQSdws5yKKrMOCdUQXBlTdbYW+zG3Y3WzDImDwcGDjJWBfbtoOEk13u5rFrrchDAYI2hS2xh0UYeyRy06c9QiEvfsartyadbaTmCtEOH14qT5LqC1S2uTe3YYs11ZclViRFQ5aG5+bOvV4t+atjUlNHT6ksbZh1w2tXBboC8k6pTEAfXeyxALcwwnL3Djqp3bftokz6GR8vhitPvMWPsavTKRwjyEN1e2juSOCJoc4niQNCaJiVGX2JRc1niTE8IzvMZBRwhV22sLFHBwjgke+vEdeHdMNlWcktvUn9m0nwftNDB/R/lc3RKS35LCSp+codPUGrsqIaeUl9iwC3MMLyViZ1MVClpngaGy/yLAjEJ/z3eqKP+ZIaA14EJQ9eyVklZ43LWQqQNAUkn8VwlqxoqR1Y0VU1l7OYwGgJEwtwCyMsheWsmHyykrogqKbirFx4EZQ8eCVnlZw1dtVkGJKmJ5/FcBZbuaM39mrNlOVczmICqS07EgiLpxBLYTkrJp/MpC4Gqqk4KxdeBCUPXslZJWdNcM5SJCX5LIaz2MpN7cAaULVczsoXiE8kDEthOSsmn8ykLgaq6WrDPHgRlDx4JWeVnDX+7TRg2TBPRmLrMnWjbCiKlMtImQLAlJIraG5wYRkpppbMlL0FVfG5KAE2WW6Ur+TKV3JTvpKb8f+l5/AWjOdxqlA0Dd6WQ3GGBFJX16am6eVbsAd7C8ZjMPrCg8fAKN+CPdhbsHFjUL4Fm2sMjFSpdMNFBXsrtHuy+x96d0+J",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "net": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSMSGCOLUMN_GETLIST = {
    'session_id': '272',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetList",
        "st": "10",
        "c": "ForumsMsgColumn",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "UserID": "0",
        "Select": "0,1,2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSMSGJX_GETFOCUSMSG = {
    'session_id': '273',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetFocusMsg",
        "c": "ForumsMsgJX",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "MsgID": "",
        "apiv": "w44",
        "Type": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSMSGJX_GETFOCUSMSG_2 = {
    'session_id': '274',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "st": "15",
        "a": "GetFocusMsg",
        "c": "ForumsMsgJX",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "MsgID": "",
        "apiv": "w44",
        "Type": "1",
        "UserID": "0",
        "Select": "0,1,2",
        "PreIndex": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSMSGJX_GETSELLIST = {
    'session_id': '277',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "st": "15",
        "a": "GetSelList",
        "c": "ForumsMsgJX",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "UserID": "0",
        "Select": "0,1,2",
        "PreIndex": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

SYSTEM_ADGETKHD = {
    'session_id': '278',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "AdGetKHD",
        "c": "System",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Scale": "0.5625",
        "apiv": "w44",
        "Type": "8,11"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSMSGCOLUMN_GETINFO = {
    'session_id': '287',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "ColumnID": "26",
        "a": "GetInfo",
        "st": "15",
        "c": "ForumsMsgColumn",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "UserID": "0",
        "Select": "0,1,2",
        "PreIndex": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_GETINFO_2 = {
    'session_id': '298',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "GetInfo",
        "View": "1,7,8,9,10,11",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST = {
    'session_id': '310',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetFunction_Art_Last",
        "c": "AppFuncExplain",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0",
        "FuncName": "ETF"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

NEWSTOCKRANKING_INDEXCHANGE = {
    'session_id': '311',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "IndexChange",
        "c": "NewStockRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

NEWSTOCKRANKING_ETFSTOCKRANKING = {
    'session_id': '312',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "ETFStockRanking",
        "st": "30",
        "c": "NewStockRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "PidType": "2",
        "apiv": "w44",
        "Type": "1",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUKLINE_GETZHISHUKLINE = {
    'session_id': '313',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetZhiShuKLine",
        "st": "630",
        "c": "ZhiShuKLine",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "Type": "d",
        "StockID": "SH000001",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_2 = {
    'session_id': '319',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetFunction_Art_Last",
        "c": "AppFuncExplain",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0",
        "FuncName": "机构增仓"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATASTATISTICS_CALUSERCLICK_3 = {
    'session_id': '325',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "DataStatistics",
        "a": "CalUserClick",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Param0": "435",
        "Param1": "1",
        "UserID": "0",
        "Token": "0"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

ZHULICHICANG_GGLIST_JGCC = {
    'session_id': '326',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "ZhuLiChiCang",
        "a": "GGList_JGCC",
        "Type": "1",
        "Order": "1",
        "Index": "0",
        "st": "30",
        "IsBX": "0",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

ZHULICHICANG_GGLIST_JGCC_2 = {
    'session_id': '329',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "ZhuLiChiCang",
        "a": "GGList_JGCC",
        "Type": "1",
        "Order": "1",
        "Index": "30",
        "st": "30",
        "Date": "2026-03-31",
        "IsBX": "0",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

DATASTATISTICS_CALUSERCLICK_4 = {
    'session_id': '335',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "DataStatistics",
        "a": "CalUserClick",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Param0": "9",
        "Param1": "1",
        "UserID": "0",
        "Token": "0"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_3 = {
    'session_id': '336',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetFunction_Art_Last",
        "c": "AppFuncExplain",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0",
        "FuncName": "市场情绪"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_GETARTTITLE_2 = {
    'session_id': '337',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetArtTitle",
        "c": "Index",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "3",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATASTATISTICS_CALUSERCLICK_5 = {
    'session_id': '342',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "DataStatistics",
        "a": "CalUserClick",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Param0": "506",
        "Param1": "1",
        "UserID": "0",
        "Token": "0"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_4 = {
    'session_id': '343',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetFunction_Art_Last",
        "c": "AppFuncExplain",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0",
        "FuncName": "题材库"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATABATCHSTATISTICS_CALUSERPAGE_2 = {
    'session_id': '352',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "CalUserPage",
        "DataList": "[{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537517,1781537532\",\"P0\":97},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537517,1781537532\",\"P0\":94},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537518,\"P0\":33},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537523,\"P0\":5},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537523,\"P0\":51},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1781537526,1781537529\",\"P0\":124},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537529,\"P0\":135},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537531,\"P0\":2}]",
        "apiv": "w44",
        "c": "DataBatchStatistics",
        "PhoneOSNew": "1",
        "Version": "5.23.0.4",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PhoneOS": "1",
        "ChannelID": "129",
        "ClientSign": "f6509ab603f832155435cabd2df35282"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LOG_LOGUSERADDNEW_3 = {
    'session_id': '354',
    'method': 'POST',
    'url': 'https://appuser.longhuvip.com/index.php',
    'params': {},
    'data': {
        "a": "LogUserAddNew",
        "apiv": "w44",
        "c": "Log",
        "PhoneOSNew": "1",
        "log": "eJztXO1v28YZ/1cM6UM6QKP4KpIBBCz10sZZ7HiRsXaIDIEizzZnikeQJzuGZaDrugUFmqxDsQDtsqLZgKLo9qFYsTZYsfSfsR3nv+gdX/RyPJJSIitOJH+w5Id3x9/z3O957u053z4suQCVLpfEUqXk4c8y/lkD+8s7ho+Ct3xjuwNcVD579NHpH/7YdFcNfxegAJexXYQftNCBB1oeDGxkQ7fOV/pf1Upg+tBx3sXC8rqxDfxfdyEyyLNf3bBdMNz08ePP2O0Jg/bkcdt7+p8nz977cHr4jh9/ffb+o16vvIGbqv9cyC99+uEnp3//EZfOLXVy79uTb/50+t1XJ79/2BO1Wi+39LN/3j/5+C+nX9ztSXJ+ybhFQS4o9/T9xwSlLOYXO/v+I9KcVPDSB98QAwkFbd39+ukH3/UB8gVt/u1J/HKlsFnc2/j9TXcd+mgLOjbE7Hzbh11vxSJ92wAOMBGwGgiau8s7tmMNDPvk07NP759++bDpRnwn5M+Fdf+rs3sfN91bwIQdLLFIhbJlIKOOBZxhH3S5XcP2DNcxOBfs264F7nDkOYer2+iAu+Ij23TAMnS6HTe4Ggp/YciSDkyxUv6lHZhwD/gHA4jvfXb846PetZsbvRd/j26CdlsGzPd8+eDZo/823WuwA/JtkA4FudwdafewWbKtZulysyQqzVKlWQJ3wr+OH/9w9ueHJ/f+evb9t2f//3ezdISjkUnCUY66XZvrGLbLreJfV0xk72EVcbX2Ng5ngqoJiqTKil5TxUoJWAOZIsmqIFRKjh1g4e3DdAVltIJcE2RBjqIjbp8ES+U54ZXzy2/FVuNSAbh0VGEAVV8KUDNExl14gAFx+Bhm6PwJVj4NFgPj9TRYIiPgCgfEWBvxebWBOAABcxdY+DXuNrDeuNn+HY5aSzD8qCzdMiwbhkFtye9/rSzhQW7JjCquWD+rkibfwW+B+9VlGI5/GG8H3DAOYBfd5jfLhmv50LYum9HT6i3gYJ/dGypRpWqEmFttiJDXaTmhuDoAMygRotomsuoVz1uGHc9AYbk3uwhBd6ggMKwWMtrMPhBqlK8KqiCr506YABk+8LApANcgX9fJ12xmE6A0szVFE7RZAo1+DweNMVBrNGpRE2LzTjJfeqka3sBxu++GE03z0jbB+vN0tI9lRK/iaetr7vdx+cTx085xW9hkNUYsZfhDgtWD39hgP7RniCeanbRM3IQPWnv4mUeeVUcb5zer68hfdowgsE0KoA+2fBDsRIL0C5ch9C3bNRAckpq0cPR9G0a7gXzbG1TYYj5Jv200IvrbZKmQGQf99rXfMqlIRz9Zk1WJz3HPjOXRRXfPLNhpm8iqKKVtQmRF7hmtAhfuuXDPyd3z+rtMKhJXzBrz53P0jPTPssk4mypTcFDHNnffIPRdIjx9FbyNFjjOho2cuAqrhYZjY7/YbpiGAzDXB0+CWMKg/GgrwmaZ2X8StTiWdYmvxUNOst81q4n30Aqt3N9sS6OOEWahHmdzbsG62bBOZLEO95WmM5Z5s109GQgB3+XWo8/sVZNeU3R6rRfLitiW2uSdS9qNPbUY7YmM5secb4wBjJi3Fem65UCjr2m2IySzDGZt9JxBWOF5UaYG0URWRLCRc4EFueabXKxYq/BiLbWlFssKx8rBUdKCWvNNLYlJLUkW6WE8lhWuzfunjwtmzTezZCazZElTaGZFssJN2eTAekGs+SaWwiSWotC7/YmscDRMchwWxJpvYtWYxKrV6NPjRFYYsei0mAXB5ptgKpNgqkafOCeywsg1lEm14NZ8c0tjcYvsvcmM/Th5rOCVSr57zY/cppgJE8SJia0wUYnZMQpPd4wm184tgSoqTBJ0MJlGjo5GcigzN0tDxMLFQBz6NJeT+zmUIspWhE4bHFJkqOqro5Ims/qGyAjwSbJkFy4+ros7O+k8t4RIIz0hSvoM8twmSzENgdLrpdkAHS/F9OUDnCDFlACjT1sTWeEcjk47X3jg2INstx2Yvt0GzA5RGOxRzu0g0kqy7kcccZCLDx0H7mezPcY2ilfX9HNjexHePKT0Ef3LRVps2XQcmT3evnvHlzdyAMuiSp/riDUhoe7ULqTMvKf6JhhMaqanTNqMkcmyzJh7G+dFQ/Ck5dNg0qvxaJwonz64+/RfX+RfJmIaI89pp3b56LXgVF+ZtBl1TaO3amJZBqeGbkgtxvVxx/UdYi2W8elsHUUSxBnf3lohkuzgjQGldotj2RiXDha3jqZ66yikBz2USqJ44W4dhUDpwWrmQMfNmwuRscw6RubJIiBOLyBik6f2ECV51tdZiwIiBpRxSZeAmujS8Ahb9kE7tk5j3/aAvwrcrqiUjjYJBPrfHuRRcgz7ALRFdL668Va/jYxLyURfSaL1VWuimHEpmVRI7RhJqizyE/diDsq8zmRUy+lONXXRMJEVuf4E7p6nyTTOqVJnKRsQOu1hCYoEqZKxvOWALZTBtSFKC7O4B0/sL9G7v2T7Q8uknMrgqC7Jk1PuPAOHLkmpmVSkFRU4iq1cHDgEZmeSXfk1zKS67ZrhCF7x8XrDt0ZkvUh29Q7yjfrh9eB6t+Mddn2nfmkHDwDB5WrV8DzSEudAd3unu2d7HDZRdV+Wq7YbrMNgxTWrSWvcDuo4lypLiOTv1y+dPvzf6ecfnPzj8+MfPsFS26pfcrsOKWAa7tvwTcPcrW8ZTgDws6DR9TzoIzyWNPAAhyGGT46OXjT84V7DRuPwANWB7jugnfR0Lwt/uVy+gHZI+Y0uKXTkJSNTLctv5Jom01tJsWyKwS/L2ud1Qn8+sU+aSejD1k9NgWRdJHsdmV2Y7nO8rtQvUugjgOiVbqzVaOgrNnJh5JPYPTl0YXD9ZmNlY+XmWmvtRuxiZXKnED8JTOg4G3DNSeSrEFqTBJZOuNTt4FpctOolDWT2taan1v+KxCuZMytZ53maHIqoJpteuSpOQIRcJfIYwaw42MfKx5cmjc6nZmZE23hRltFls9BzaIk57ASj2mbhS+lJdKI9OJYRBWgKjht187V7lSad4kwiLzE5PT1TaiLZCmV7oyJqPD3pVGq8dKEiLwGUijGRVtSks9jKxZNOkXTm5k99IhUT",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "net": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKL2DATA_GETSTOCKPERCENTTURNOVERTEN = {
    'session_id': '374',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetStockPercentTurnoverTen",
        "c": "StockL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "StockID": "002636",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKL2DATA_GETWEITUO = {
    'session_id': '375',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetWeiTuo",
        "st": "25",
        "c": "StockL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Tur": "30",
        "apiv": "w44",
        "Type": "0",
        "Vol": "500",
        "StockID": "002636",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LOG_LOGUSERADDNEW_4 = {
    'session_id': '383',
    'method': 'POST',
    'url': 'https://appuser.longhuvip.com/index.php',
    'params': {},
    'data': {
        "a": "LogUserAddNew",
        "apiv": "w44",
        "c": "Log",
        "PhoneOSNew": "1",
        "log": "eJztWF9v40QQ/ypRzMOdZOz8sxNXykOvHKiivSttBQ+lsjb2Nlnq7Po2m7ZR04c7BAXxR5wEuofjEAcPnEBCiAegnBBf5pJevwW7tpM0a9dpeukJnSpLjTs7M/7NzG/s2d3Yz2LIsnPZQlbN+vxXWQF1SN9pEwYYIvjtJYThmxTUmxAzhes4QskhTQ2gTlvbBsgH2AMahrsIu3BPY8RHjgYchnYQ62jrDdiEN/ccsAMYXEItNh+tcFe1On9wvlzJG8WyYZg5o6RmoXtKZhZN01CzHjfLzm3sjxuYxVKCQSATECeEMQh5VuEoBC94yNm+9i6Cu5kd/ue6vgwQfo+7Ibv6AsGMP5kjaMIl0CFttpHbVAB2KUHunBOu6qvQ42h3TmlQQpjtBf/q64R4NUBHiywU6CK2BLntwS2WPdg8UGM1Ti3y88ef9z/86H28DOg2ZC0lXfv43l/9R/92S4VuqtrJj1/2vrrf//6wWyylax7/8t2zp392C1axq4SRr5BWppopdYOK3IAAV/t/POnd/bb309fPjn47+eGR0v/sYe+bj3tfPOj/fnSOoraR1uS10USBzuIjp5Lg3hi9ykWrmE/ho1mW+WhUrHKY84hzxgXhKen6W1H2tEUhGeQyK0o/DtKoVHJxkEI2qWkkWkzRQ4nx8H5pQGcbugsNgOvQvXa79gF0WIYEP2pmFbiIvEVJ28/Q4a2aQZhlnNBw0Z1Ji+mSRYDZrhHG/Oag9UZgRhoBqrqQ6fO+v0CaPmCB3o02YwSfUoTAtRmoJVbDsmIcM/PWpVOmxQCFPk8F1NbE7Yq4TaONlZNp89KB8vwySLG2Ev6moLWsgimTPJRNIvnobTYDfl/C9yCZrJH+gK3xim7kN5OcyR8Ofbkj4AYJCvBQhhwP2g53QaEtovDFmi6V4Az3K4wueKDVQo6EmsItCluNpai54pa3yDppO41V6HT486kAJeQRA2y6Y7cYcbZtzN2ORaEkeVvzkItwfR3U1hhFQQuLetlh8loOJZ4nGjSeD8lZaVOJs62cz1VktkWySWwb+yheEe6KcLKzQjLhygV50IhkE19vo9nqim5XdEtwlkA3/p2X91mRTPDmnCP6i9JtWv20LuC+dOFLH/jSB750vtQkWL8jDPU3Ojz/yFkTpZh3gc9r89ptvMhgU+z8IIaUd0HwDKkVwjF1mBk1E3kKdEV2MsM8XZ864dJe57KyOnnwmkHwSu+TB88fPzm+d9Q7fJq4VRX9eIt3QTUONcQppmvObRHfcJceVGxY/EG0KoUOoe6MvHVDbzf3GAXV/Rb0+K4l0Fx0q2Yub5UNlUePhEk1p64LAvIG5aLq63n1QAlVLnjYMi1WeW/L2VSKjfOGdfZZCzcwizGDcrESFikMZvIuYFrcE7o+6FIteFNKDhbxFhnmMcp1QqOJuBKiOsfkNrnxpo71Eg+QhLeEtQEi+84AjE09u8EhwwsdKo0d1+TNlPOak8P7vV8/7T385/jvn2d0XsOvUkUqZkUcypzJaX7Jr9mKUcwX/m+bb3HJJ1EvHei5N98cWS5eh0AmjwtpFLmaF849L0zIuNRrr9a8sPkf5XDYVA==",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "net": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

DATABATCHSTATISTICS_CALUSERPAGE_3 = {
    'session_id': '387',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "CalUserPage",
        "c": "DataBatchStatistics",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PhoneOS": "1",
        "ChannelID": "129",
        "ClientSign": "049d067fc5b2b8186de2a11e3b583b75",
        "DataList": "[{\"U\":\"7764559\",\"S\":\"0,0,0,0,0\",\"Ct\":\"1781537534,1781537539,1781537548,1781537556,1781537565\",\"P0\":2},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537537,\"P0\":200},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537552,\"P0\":79},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537552,\"P0\":95},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537563,\"P0\":190},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537573,\"P0\":94},{\"U\":\"7764559\",\"S\":0,\"Ct\":1781537573,\"P0\":97}]",
        "apiv": "w44",
        "Version": "5.23.0.4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKL2DATA_GETZSTREND = {
    'session_id': '407',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetZstrend",
        "c": "StockL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "StockID": "SH000001",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKYIDONGKANPAN_STOCKDPREALDATA = {
    'session_id': '413',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "StockDPRealData",
        "c": "StockYiDongKanPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "StockID": "002636",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

USERINFO_GETPERMISSION = {
    'session_id': '414',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetPermission",
        "c": "UserInfo",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "12",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKYIDONGKANPAN_STOCKDPEXPLAIN = {
    'session_id': '415',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "StockDPExplain",
        "c": "StockYiDongKanPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "StockID": "002636",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKF10BASIC_GETINDEX = {
    'session_id': '418',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetIndex",
        "apiv": "w44",
        "c": "StockF10Basic",
        "StockID": "002636",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKF10BASIC_BIGREMINDERW43 = {
    'session_id': '419',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "BigReminderW43",
        "st": "25",
        "c": "StockF10Basic",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "apiv": "w44",
        "StockID": "002636"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HISLIMITRESUMPTION_GETDAYZHANGTING = {
    'session_id': '420',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetDayZhangTing",
        "st": "25",
        "c": "HisLimitResumption",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "StockID": "002636",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKLINEDATA_GETKLINEZHANGTING = {
    'session_id': '421',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetKLineZhangTing",
        "apiv": "w44",
        "c": "StockLineData",
        "StockID": "002636",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

COMPANYNOTICE_CORPORATENEWSSTOCKLIST = {
    'session_id': '422',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "CorporateNewsStockList",
        "st": "25",
        "apiv": "w44",
        "c": "CompanyNotice",
        "StockID": "002636",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

COMPANYNOTICE_COMPANYNEWSREPORTLIST = {
    'session_id': '423',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "CompanyNewsReportList",
        "st": "25",
        "apiv": "w44",
        "Type": "8",
        "c": "CompanyNotice",
        "StockID": "002636",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

COMPANYNOTICE_RESEARCHFIELDEXCEL = {
    'session_id': '424',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ResearchFieldExcel",
        "apiv": "w44",
        "c": "CompanyNotice",
        "StockID": "002636",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

COMPANYNOTICE_RESEARCHFIELDLIST = {
    'session_id': '425',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ResearchFieldList",
        "st": "25",
        "c": "CompanyNotice",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "apiv": "w44",
        "Type": "2",
        "StockID": "002636"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INSTITUTIONALPOSITIONSINFO_INSTITUTIONALSHOWDATE = {
    'session_id': '426',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "InstitutionalShowDate",
        "c": "InstitutionalPositionsInfo",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "002636"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INSTITUTIONALPOSITIONSINFO_STOCKINSTITUTIONALPOSITIONS = {
    'session_id': '427',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "StockInstitutionalPositions",
        "apiv": "w44",
        "c": "InstitutionalPositionsInfo",
        "StockID": "002636",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Season": "2026-03-31"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INSTITUTIONALPOSITIONSINFO_STOCKHOLDINGFUND = {
    'session_id': '428',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "StockHoldingFund",
        "st": "25",
        "c": "InstitutionalPositionsInfo",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "apiv": "w44",
        "Type": "0",
        "StockID": "002636",
        "Season": "2026-03-31"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSTUYERE_GETTAGLIST = {
    'session_id': '429',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetTagList",
        "c": "ForumsTuyere",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSTUYERE_GETBYSTOCK = {
    'session_id': '430',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "st": "25",
        "a": "GetByStock",
        "c": "ForumsTuyere",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "Code": "002636",
        "apiv": "w44",
        "Type": "0",
        "UserID": "0",
        "Select": ""
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

FORUMSTUYERE_GETBYSTOCK_2 = {
    'session_id': '432',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetByStock",
        "st": "25",
        "c": "ForumsTuyere",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "Code": "000510",
        "apiv": "w44",
        "Type": "0",
        "UserID": "0",
        "Select": ""
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LOG_LOGUSERADDNEW_5 = {
    'session_id': '446',
    'method': 'POST',
    'url': 'https://appuser.longhuvip.com/index.php',
    'params': {},
    'data': {
        "a": "LogUserAddNew",
        "c": "Log",
        "PhoneOSNew": "1",
        "log": "eJztWV9v40QQ/ypR8nJIwU6c2EkqRejacqjigONa4KGqrI29lyy1vT57nbQ091AJOKjKATrgOLWCe4CCEKL3gBDqSXyaJm2/Bbtep0ns1E7bFB13ecmf2Znx7Px2Zn+7Xt5IW5CkZ9JSOpu26bcN6vBtYMKqhk0BoHVPWAXIBpYBBGTpcE1wINAJqAkeEoBGUBORdWGRYG31XQ8TQBC2rgfirAM17OgT8tbm3l5fIw6obrjQgBrxNRf0ai4nKQUlewu7iJlUc9mlm8iCS6BGRdVX89l7Ga6SuUWn55z6fpNp3XBA3YQWycQOdj/76vDgp872wcmjP9v8z8n9L9vH+3tHzz7tfvu0+8Uf7Yt7b5/88/j48YPu3m6b4qAxIC6fMeqpVqfY5kvlvFwoyWW5kC9n01Dvy5SiVCpTmYFcKlzeiBgUcxEDSZH5UuEppU9h60eeXNyZqAsLtrgXan2X6QsuMw05WLDu4H6+g/DuZUOzquSlijQ8q56MxR8HUzBXaYJzxdacgbTVa+8j2Eo16ccr4lsAWR9QR7glzmGL0AfTAEx4E6xjjyznVjLA0h2M9BmNj4q3oUGdNgc0HIyJyryJcx7NlMm8+xNjg37q1Lu9UHw9VvaOeHY6qR19jLauGdBhzkb5cZqqDghgQbu0SJFFeECZEQFGbA215rk0164rspQDp69r+L/UlqfrwKqrJrLqa2gErnSxlsK4clkSruMU9xT7/wL7qHaAfhMbnglVh64AOAJ7WSnnw9hz2bSmnwdcL1bTbLcpRrcsX5aE6/CW+hJDzEkSFc5iQn0u+sxpFgz4ZJ7Umj+qcmKl1oAzIj5fkcHKdU2k6watxhWG29g08nQv1xrAIa6gQwKQ4fJMz/M/41HI83gK0Ud/3oz1qHafNA5IPceoNgix3RlRBLbNpiMY2Ko3vCayBRqK2CoWxRasiYMPExrENF5bXJivDviqLnMmskJZqDnMWNvmPCCwanmG0Tbfu+QjYwnm4d9bx/ub3e37dDdrF3MVRSiW4vnq2cVynrSHOCgr3nIhVNByXi5LZ3BQZlBRIgYFOejsV5nQZGZ7nkzEsdoY8z6fvdKpRjuvrCjFcOflsqTOO3KtJffgcyXzavpvZJu6ePMMe/LVjNPWSVVUA94h0cTTxV2sRBc8k12eyjwPOV7C2KgNpoZwgbhg0rn1iEggDJJ0vh3mRb+oONrZP9r5Pr5938jn4hW6258fHvzSebgZr/XXr53N3c6DHzs7TxL8fff05NGzeJ3OJ793vt6K1zl68k136+eEZ+0edH/4uLu9efjs4TiaRwe/He9tXnS/u+S9C6vekhyq6FJZUUpn7XnMILznBQb/33sXRaYfpXBj47KkxhYs+Jebx497VBvUy4gDsWdGYFLKK/kwJlyWhAlrMFNAJg9IIXyJ1ZMlXmL1GvrVoNKA2irU5xrsAka/9k7tQ7qtpbD/lU3dBjrCbzjYs1PO6c9sClkkpXHDBX0IyL6BD09drbsfGeJ1257Dpg2IPzzrUapk+eM1f1yl04lmrCLJkYxxWWLGBje36Vqe9FpW8pIUfn0QyBKR4WRiisnEMZHkSvhYF8iSMAnI2xSTiWNSLCuROuGyRGLEyfIUk4ljouSkSJ1wWWLvGjycTJGZODIlSQqfpgLZeMgEh8EpMpNGJjiinnVsfcFewkXHehENvwJr0JApHOEXaP5V2CnfHbr6CmOBmqrtwCbCnstuwlb+BWvDG44=",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "UserID": "0",
        "net": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_GETINFO_HQ_VIEW_2_7_9_10 = {
    'session_id': '1015',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "GetInfo",
        "View": "2,7,9,10",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

INDEX_GETINFO_HQ_VIEW_3 = {
    'session_id': '1019',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "GetInfo",
        "View": "3",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

INDEX_GETINFO_HQ_VIEW_4_5_11 = {
    'session_id': '1021',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "GetInfo",
        "View": "4,5,11",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

ZHISHUL2DATA_GETVOLTURINCREMENTAL = {
    'session_id': '1031',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetVolTurIncremental",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801001",
        "Day": ""
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUL2DATA_GETTRENDINCREMENTAL = {
    'session_id': '1032',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetTrendIncremental",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801001",
        "Day": ""
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUL2DATA_GETPARENTPLATECODE = {
    'session_id': '1033',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetParentPlateCode",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801001"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_GETPLATE_INFO_QJ = {
    'session_id': '1034',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetPlate_Info_QJ",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Date": "",
        "apiv": "w44",
        "PlateID": "801001"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_GETARTTITLE_HQ_PLATE = {
    'session_id': '1035',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetArtTitle",
        "c": "Index",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "2",
        "StockID": "801001",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_SONPLATE_INFO = {
    'session_id': '1036',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "SonPlate_Info",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "PlateID": "801001"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_GETGPCPHBTS_TAG = {
    'session_id': '1037',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetGPCPHBTS_Tag",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0",
        "PlateID": "801001"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

CONCEPTIONPOINT_BKFENSHIZHIBO = {
    'session_id': '1040',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "BKFenShiZhiBo",
        "c": "ConceptionPoint",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Date": "",
        "apiv": "w44",
        "PlateID": "801001"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

INDEX_YOUZIDONGXIANGBYLIST = {
    'session_id': '1880',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "apiv": "w44",
        "PhoneOSNew": "1",
        "VerSion": "5.23.0.4"
    },
    'data': {
        "c": "Index",
        "a": "YouZiDongXiangByList",
        "Time": "2026-06-26",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

DATASTATISTICS_CALUSERCLICK_HAR_18001 = {
    'session_id': '18001',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "19",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18003 = {
    'session_id': '18003',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetFunction_Art_Last",
    "apiv": "w44",
    "c": "AppFuncExplain",
    "PhoneOSNew": "1",
    "UserID": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "FuncName": "市场风口",
    "VerSion": "5.23.0.4",
    "Token": "0"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

USERSELECTSTOCK_REFRESHSTOCKLIST_HAR_18012 = {
    'session_id': '18012',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "UserSelectStock",
    "a": "RefreshStockList",
    "StockIDList": "SH000001,SZ399001,SZ399006",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

STOCKFENGKDATA_GETFENGKLIST_HAR_18013 = {
    'session_id': '18013',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "StockFengKData",
    "a": "GetFengKList",
    "Index": "0",
    "st": "500",
    "Order": "17",
    "Day": "",
    "Time": "",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

STOCKFENGKDATA_GETFENGKYDPLATE_HAR_18019 = {
    'session_id': '18019',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "StockFengKData",
    "a": "GetFengKYDPlate",
    "Day": "20260626",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

STOCKFENGKDATA_GETFENGKLIST_HAR_18021 = {
    'session_id': '18021',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "StockFengKData",
    "a": "GetFengKList",
    "Index": "0",
    "st": "500",
    "Order": "17",
    "Day": "20260626",
    "Time": "1500",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

DATABATCHSTATISTICS_CALUSERPAGE_HAR_18026 = {
    'session_id': '18026',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "CalUserPage",
    "c": "DataBatchStatistics",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "PhoneOS": "1",
    "ChannelID": "129",
    "ClientSign": "418ee704ca70954075ab32132cbf8963",
    "DataList": "[{\"U\":\"7764559\",\"S\":\"0,0,0,0,0\",\"Ct\":\"1782531378,1782531644,1782531698,1782533827,1782537486\",\"P0\":2},{\"U\":\"7764559\",\"S\":\"0,0,0\",\"Ct\":\"1782531623,1782531691,1782531734\",\"P0\":97},{\"U\":\"7764559\",\"S\":\"0,0,0\",\"Ct\":\"1782531623,1782531691,1782531734\",\"P0\":92}]",
    "apiv": "w44",
    "Version": "5.23.0.4"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18054 = {
    'session_id': '18054',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "41",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18055 = {
    'session_id': '18055',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetFunction_Art_Last",
    "c": "AppFuncExplain",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "UserID": "0",
    "FuncName": "上证指数"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_GETPLATE_INFO_QJ_HAR_18059 = {
    'session_id': '18059',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetPlate_Info_QJ",
    "c": "ZhiShuRanking",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Date": "",
    "apiv": "w44",
    "PlateID": "801225"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_SONPLATE_INFO_HAR_18061 = {
    'session_id': '18061',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "SonPlate_Info",
    "c": "ZhiShuRanking",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "apiv": "w44",
    "PlateID": "801225"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_GETGPCPHBTS_TAG_HAR_18062 = {
    'session_id': '18062',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetGPCPHBTS_Tag",
    "c": "ZhiShuRanking",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "UserID": "0",
    "PlateID": "801225"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

THEME_INFOBKR_HAR_18063 = {
    'session_id': '18063',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "InfoBKR",
    "apiv": "w44",
    "c": "Theme",
    "ZSCode": "801225",
    "PhoneOSNew": "1",
    "UserID": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

CONCEPTIONPOINT_BKFENSHIZHIBO_HAR_18065 = {
    'session_id': '18065',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "BKFenShiZhiBo",
    "c": "ConceptionPoint",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Date": "",
    "apiv": "w44",
    "PlateID": "801225"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

FORUMSTUYERE_GETBYSTOCK_HAR_18071 = {
    'session_id': '18071',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetByStock",
    "st": "30",
    "c": "ForumsTuyere",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "Index": "0",
    "Code": "801225",
    "apiv": "w44",
    "Type": "1",
    "UserID": "0",
    "Select": ""
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18080 = {
    'session_id': '18080',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "85",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18083 = {
    'session_id': '18083',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetFunction_Art_Last",
    "c": "AppFuncExplain",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "UserID": "0",
    "FuncName": "主题机会"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18090 = {
    'session_id': '18090',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "140",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18091 = {
    'session_id': '18091',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "176",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

THEMENEWS_GETLIST_HAR_18092 = {
    'session_id': '18092',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "ThemeNews",
    "a": "GetList",
    "Type": "-1",
    "st": "30",
    "Index": "0",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18124 = {
    'session_id': '18124',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "301",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18125 = {
    'session_id': '18125',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "143",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

THEMENEWS_GETLIST_HAR_18126 = {
    'session_id': '18126',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "ThemeNews",
    "a": "GetList",
    "Type": "3",
    "st": "30",
    "Index": "0",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18127 = {
    'session_id': '18127',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "177",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

THEMENEWS_GETCOLLECTNEWS_HAR_18128 = {
    'session_id': '18128',
    'method': 'POST',
    'url': 'https://apparticle.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "ThemeNews",
    "a": "GetCollectNews",
    "Type": "-1",
    "st": "30",
    "Index": "0",
    "UserID": "0",
    "Token": "0",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18139 = {
    'session_id': '18139',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "40",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

STOCKBIDYIDONG_GETPIANLIZHI_MANY_HAR_18157 = {
    'session_id': '18157',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetPianLiZhi_Many",
    "c": "StockBidYiDong",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "UserID": "0"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

DATABATCHSTATISTICS_CALUSERPAGE_HAR_18162 = {
    'session_id': '18162',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "CalUserPage",
    "c": "DataBatchStatistics",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "PhoneOS": "1",
    "ChannelID": "129",
    "ClientSign": "2aea54e2b6d4cec3b63ed5a4dda6f33f",
    "DataList": "[{\"U\":\"7764559\",\"S\":0,\"Ct\":1782537513,\"P0\":85},{\"U\":\"7764559\",\"S\":\"0,0,0,0,0\",\"Ct\":\"1782537526,1782537559,1782537579,1782537598,1782537625\",\"P0\":2},{\"U\":\"7764559\",\"S\":0,\"Ct\":1782537555,\"P0\":111},{\"U\":\"7764559\",\"S\":\"0,0\",\"Ct\":\"1782537570,1782537589\",\"P0\":91},{\"U\":\"7764559\",\"S\":0,\"Ct\":1782537610,\"P0\":97},{\"U\":\"7764559\",\"S\":0,\"Ct\":1782537610,\"P0\":95}]",
    "apiv": "w44",
    "Version": "5.23.0.4"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18181 = {
    'session_id': '18181',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetFunction_Art_Last",
    "c": "AppFuncExplain",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "UserID": "0",
    "FuncName": "严重异动提醒"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

STOCKBIDYIDONG_GETPIANLIZHI_INDEX_HAR_18182 = {
    'session_id': '18182',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetPianLiZhi_Index",
    "c": "StockBidYiDong",
    "ZDJK_Type": "1",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "UserID": "0"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18190 = {
    'session_id': '18190',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "174",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}

INDEX_GETARTTITLE_HAR_18191 = {
    'session_id': '18191',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
    "a": "GetArtTitle",
    "c": "Index",
    "PhoneOSNew": "1",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "VerSion": "5.23.0.4",
    "Token": "0",
    "apiv": "w44",
    "Type": "4",
    "UserID": "0"
},
    'headers': {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

DATASTATISTICS_CALUSERCLICK_HAR_18207 = {
    'session_id': '18207',
    'method': 'POST',
    'url': 'https://applog.longhuvip.com/w1/api/index.php',
    'params': {
    "apiv": "w44",
    "PhoneOSNew": "1",
    "VerSion": "5.23.0.4"
},
    'data': {
    "c": "DataStatistics",
    "a": "CalUserClick",
    "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
    "Param0": "507",
    "Param1": "1",
    "UserID": "0",
    "Token": "0"
},
    'headers': {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apppage.longhuvip.com",
    "X-Requested-With": "com.aiyu.kaipanla",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://apppage.longhuvip.com/",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
},
}


HISHOMEDINGPAN_CHANGESTATISTICS_EMOTION_HAR_18208 = {
    'session_id': '18208',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ChangeStatistics",
        "st": "100",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HISHOMEDINGPAN_MARKETSCLNKLINE_EMOTION_HAR_18209 = {
    'session_id': '18209',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "MarketSCLNKLine",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HISHOMEDINGPAN_MARKETVOLUMEBENCHMARKLINE_EMOTION_HAR_18210 = {
    'session_id': '18210',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "MarketVolumeBenchmarkLine",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HOMEDINGPAN_MARKETCAPACITYKLINE_EMOTION_HAR_18211 = {
    'session_id': '18211',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "MarketCapacityKLine",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_EMOTION_HAR_18212 = {
    'session_id': '18212',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetFunction_Art_Last",
        "c": "AppFuncExplain",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0",
        "FuncName": "????"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HOMEDINGPAN_DAILYLIMITINDEX_EMOTION_HAR_18213 = {
    'session_id': '18213',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "DailyLimitIndex",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HOMEDINGPAN_MARKETSTOCKZDNUM_EMOTION_HAR_18214 = {
    'session_id': '18214',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "MarketStockZDNum",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

XIANHUODATA_GETXIANHUOLIST_EMOTION_HAR_18215 = {
    'session_id': '18215',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetXianHuoList",
        "apiv": "w44",
        "c": "XianHuoData",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Time": "1782479163"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HOMEDINGPAN_SHARPWITHDRAWALLIST_EMOTION_HAR_18216 = {
    'session_id': '18216',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "0",
        "a": "SharpWithdrawalList",
        "st": "20",
        "apiv": "w44",
        "Type": "5",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HOMEDINGPAN_WEIGHTPERFORMANCELIST_EMOTION_HAR_18217 = {
    'session_id': '18217',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "WeightPerformanceList",
        "st": "20",
        "apiv": "w44",
        "Type": "2",
        "c": "HomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


STOCKL2HISTORY_GETZSREAL_WITHDRAW_HISTORY_18218 = {
    'session_id': '18218',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetZsReal",
        "c": "StockL2History",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


HISHOMEDINGPAN_DAILYLIMITINDEX_HISTORY_18219 = {
    'session_id': '18219',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "DailyLimitIndex",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HISHOMEDINGPAN_DAILYLIMITPERFORMANCE_HISTORY_18220 = {
    'session_id': '18220',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "0",
        "a": "DailyLimitPerformance",
        "st": "2000",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "PidType": "1",
        "apiv": "w44",
        "Type": "4",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

HISHOMEDINGPAN_DAILYLIMITPERFORMANCE2_HISTORY_18221 = {
    'session_id': '18221',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "DailyLimitPerformance2",
        "st": "20",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "PidType": "1",
        "apiv": "w44",
        "Type": "5",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


HISHOMEDINGPAN_HISDABANLIST_HISTORY_18222 = {
    'session_id': '18222',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "HisDaBanList",
        "st": "2000",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "PidType": "2",
        "apiv": "w44",
        "Type": "4",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUL2DATA_GETTRENDINCREMENTAL_HISTORY_18223 = {
    'session_id': '18223',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetTrendIncremental",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801900",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUL2DATA_GETVOLTURINCREMENTAL_HISTORY_18224 = {
    'session_id': '18224',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetVolTurIncremental",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801900",
        "Day": "2026-06-25"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


STOCKLINEDATA_GETDADANKLINE2NEW_MARKET_VOLUME_18225 = {
    'session_id': '18225',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetDaDanKLine2New",
        "st": "850",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0",
        "apiv": "w44",
        "Type": "d",
        "StockID": "SH000001",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUKLINE_GETZHISHUKLINE_LN_MARKET_VOLUME_18226 = {
    'session_id': '18226',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetZhiShuKLine_LN",
        "st": "610",
        "apiv": "w44",
        "Type": "d",
        "c": "ZhiShuKLine",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Index": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKLINEDATA_GETKLINETODAYDADANNEW_MARKET_VOLUME_18227 = {
    'session_id': '18227',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetKLineTodayDaDanNew",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "d",
        "StockID": "SH000001",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHUKLINE_GETZHISHUKLINETODAY_LN_MARKET_VOLUME_18228 = {
    'session_id': '18228',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetZhiShuKLineToday_LN",
        "c": "ZhiShuKLine",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "d",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_HISTORY_18229 = {
    'session_id': '18229',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "GetInterviewsByDateStock",
        "st": "30",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "DEnd": "2026-03-03",
        "Index": "0",
        "DStart": "2024-05-16",
        "apiv": "w44",
        "Type": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_REALTIME_18230 = {
    'session_id': '18230',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "GetInterviewsByDateStock",
        "st": "30",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "DEnd": "2026-06-26",
        "Index": "0",
        "DStart": "2024-05-16",
        "apiv": "w44",
        "Type": "2"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKLINEDATA_GETINTERVIEWSBYDATEZS_HISTORY_18231 = {
    'session_id': '18231',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "a": "GetInterviewsByDateZS",
        "st": "30",
        "c": "StockLineData",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "DEnd": "2026-03-30",
        "Index": "0",
        "DStart": "2024-05-16",
        "apiv": "w44",
        "Type": "9"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


HISHOMEDINGPAN_MARKETSCLNKLINE_MARKET_VOLUME_HISTORY_18232 = {
    'session_id': '18232',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "MarketSCLNKLine",
        "c": "HisHomeDingPan",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "Type": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


PAYFUNCREMINDNEW_GETREMIND_LATEST_THEME_18233 = {
    'session_id': '18233',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://appupchina.longhuvip.com/payw1/api/index.php',
    'params': {},
    'data': {
        "a": "GetRemind",
        "c": "PayFuncRemindNew",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "NID": "26",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

TICAI_READERCOUNT_LATEST_THEME_18234 = {
    'session_id': '18234',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://appres.longhuvip.com/tj/index.php',
    'params': {},
    'data': {
        "c": "TiCai",
        "a": "ReaderCount",
        "u": "0",
        "m": "0",
        "t": "1",
        "UserID": "0",
        "Token": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G988N Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
}

ZHISHUL2DATA_GETPARENTPLATECODE_WINDVANE_18235 = {
    'session_id': '18235',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetParentPlateCode",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801225"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_18236 = {
    'session_id': '18236',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetVolTurIncremental",
        "apiv": "w44",
        "c": "ZhiShuL2Data",
        "StockID": "801225",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Day": ""
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_18237 = {
    'session_id': '18237',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetTrendIncremental",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801225",
        "Day": ""
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

INDEX_GETARTTITLE_WINDVANE_18238 = {
    'session_id': '18238',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetArtTitle",
        "apiv": "w44",
        "Type": "2",
        "c": "Index",
        "StockID": "801225",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_HISTORY_18239 = {
    'session_id': '18239',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetTrendIncremental",
        "c": "ZhiShuL2Data",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44",
        "StockID": "801225",
        "Day": "2026-06-25"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_GETPLATE_INFO_QJ_WINDVANE_HISTORY_18240 = {
    'session_id': '18240',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetPlate_Info_QJ",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Date": "2026-06-25",
        "apiv": "w44",
        "PlateID": "801225"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_HISTORY_18241 = {
    'session_id': '18241',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetVolTurIncremental",
        "apiv": "w44",
        "c": "ZhiShuL2Data",
        "StockID": "801225",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Day": "2026-06-25"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_SONPLATE_INFO_WINDVANE_HISTORY_18242 = {
    'session_id': '18242',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "SonPlate_Info",
        "apiv": "w44",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PlateID": "801225",
        "IsShow": "1",
        "Date": "2026-06-25"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_GETGPCPHBTS_TAG_WINDVANE_HISTORY_18243 = {
    'session_id': '18243',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetGPCPHBTS_Tag",
        "apiv": "w44",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "PlateID": "801225",
        "Date": "2026-06-25"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

HISCONCEPTIONPOINT_BKFENSHIZHIBO_WINDVANE_HISTORY_18244 = {
    'session_id': '18244',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "BKFenShiZhiBo",
        "apiv": "w44",
        "c": "HisConceptionPoint",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "PlateID": "801225",
        "Date": "2026-06-25"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_HISTORY_18245 = {
    'session_id': '18245',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "TSZB": "0",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "old": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "IsZZ": "0",
        "Token": "0",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "6",
        "IsKZZType": "0",
        "UserID": "0",
        "PlateID": "801225",
        "TSZB_Type": "0",
        "filterType": "0"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB72_18246 = {
    'session_id': '18246',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "TSZB": "72",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "SetLog": "1",
        "old": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "IsZZ": "0",
        "Token": "0",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "6",
        "Filed_Type": "0",
        "IsKZZType": "0",
        "UserID": "0",
        "PlateID": "801225",
        "TSZB_Type": "0",
        "filterType": "0"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB73_18247 = {
    'session_id': '18247',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "TSZB": "73",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "SetLog": "1",
        "old": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "IsZZ": "0",
        "Token": "0",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "6",
        "Filed_Type": "0",
        "IsKZZType": "0",
        "UserID": "0",
        "PlateID": "801225",
        "TSZB_Type": "0",
        "filterType": "0"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}

ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB74_18248 = {
    'session_id': '18248',
    'added_time': '2026-06-27',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "TSZB": "74",
        "a": "ZhiShuStockList_W8",
        "st": "30",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "SetLog": "1",
        "old": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "IsZZ": "0",
        "Token": "0",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "6",
        "Filed_Type": "0",
        "IsKZZType": "0",
        "UserID": "0",
        "PlateID": "801225",
        "TSZB_Type": "0",
        "filterType": "0"
},
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
},
}


LONGHUBANG_GETSTOCKLIST_TODAY_BOARD_18249 = {
    'session_id': '18249',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Index": "0",
        "Time": "2026-06-26",
        "Type": "2",
        "st": "500",
        "a": "GetStockList",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_GETAGENCYLISTV2_TODAY_BOARD_18250 = {
    'session_id': '18250',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Index": "0",
        "Time": "2026-06-26",
        "st": "500",
        "a": "GetAgencyListV2",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_GETAGENCYKLINE_TODAY_BOARD_18251 = {
    'session_id': '18251',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "index": "0",
        "st": "499",
        "a": "GetAgencyKline",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_GETBUSINESSLIST_TODAY_BOARD_18252 = {
    'session_id': '18252',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Index": "0",
        "Time": "2026-06-26",
        "Type": "1",
        "st": "100",
        "a": "GetBusinessList",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

LONGHUBANG_GETAGENCYDAYLIST_TODAY_BOARD_18253 = {
    'session_id': '18253',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "SDay": "2026-04-03",
        "EDay": "2026-06-23",
        "a": "GetAgencyDayList",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_YOUZI_GROUP_18254 = {
    'session_id': '18254',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "GID": "41",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_YOUZI_GROUP_18255 = {
    'session_id': '18255',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Day": "3",
        "GID": "41",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

USERBUSINESS_GETOFFICEV2_YOUZI_GROUP_18256 = {
    'session_id': '18256',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetOfficev2",
        "c": "UserBusiness",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCK_GETSTOCKCHART_YOUZI_GROUP_18257 = {
    'session_id': '18257',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "StockID": "000783",
        "index": "0",
        "st": "250",
        "a": "GetStockChart",
        "c": "Stock",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

USERBUSINESS_GETDAY_TOP_YOUZI_18258 = {
    'session_id': '18258',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Day": "",
        "a": "GetDay",
        "c": "UserBusiness",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

STOCKL2HISTORY_GETZSTREND_NARROW_HISTORY_18285 = {
    'session_id': '18285',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Day": "2026-06-25",
        "a": "GetZsTrend_Narrow",
        "c": "StockL2History",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "apiv": "w44"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_REALRANKINGINFO_HISTORY_18286 = {
    'session_id': '18286',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "Order": "1",
        "st": "30",
        "a": "RealRankingInfo",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "1",
        "ZSType": "7"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_REALRANKINGINFO_TYPE1_ZSTYPE7_18287 = {
    'session_id': '18287',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['Type', 'ZSType'],
    'data': {
        "Order": "1",
        "st": "30",
        "a": "RealRankingInfo",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "1",
        "ZSType": "7"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_REALRANKINGINFO_TYPE2_ZSTYPE4_18288 = {
    'session_id': '18288',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['Type', 'ZSType'],
    'data': {
        "Order": "1",
        "st": "30",
        "a": "RealRankingInfo",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "2",
        "ZSType": "4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_REALRANKINGINFO_TYPE2_ZSTYPE6_18289 = {
    'session_id': '18289',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['Type', 'ZSType'],
    'data': {
        "Order": "1",
        "st": "30",
        "a": "RealRankingInfo",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "Date": "2026-06-25",
        "apiv": "w44",
        "Type": "2",
        "ZSType": "6"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_REALRANKINGINFO_TYPENEG4_ZSTYPE4_18290 = {
    'session_id': '18290',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['Type', 'ZSType'],
    'data': {
        "Order": "1",
        "st": "30",
        "a": "RealRankingInfo",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "Date": "2026-06-25",
        "RStart": "0925",
        "REnd": "1445",
        "apiv": "w44",
        "Type": "-4",
        "ZSType": "4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

ZHISHURANKING_REALRANKINGINFO_TYPENEG4_ZSTYPE6_18291 = {
    'session_id': '18291',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://apphis.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['Type', 'ZSType'],
    'data': {
        "Order": "1",
        "st": "30",
        "a": "RealRankingInfo",
        "c": "ZhiShuRanking",
        "PhoneOSNew": "1",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "VerSion": "5.23.0.4",
        "Index": "0",
        "Date": "2026-06-25",
        "RStart": "0925",
        "REnd": "1445",
        "apiv": "w44",
        "Type": "-4",
        "ZSType": "6"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID7_18259 = {
    'session_id': '18259',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "7",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID7_18272 = {
    'session_id': '18272',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "7",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID10_18260 = {
    'session_id': '18260',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "10",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID10_18273 = {
    'session_id': '18273',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "10",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID20_18261 = {
    'session_id': '18261',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "20",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID20_18274 = {
    'session_id': '18274',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "20",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID25_18262 = {
    'session_id': '18262',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "25",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID25_18275 = {
    'session_id': '18275',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "25",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID33_18263 = {
    'session_id': '18263',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "33",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID33_18276 = {
    'session_id': '18276',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "33",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID35_18264 = {
    'session_id': '18264',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "35",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID35_18277 = {
    'session_id': '18277',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "35",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID41_18265 = {
    'session_id': '18265',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "41",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID41_18278 = {
    'session_id': '18278',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "41",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID57_18266 = {
    'session_id': '18266',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "57",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID57_18279 = {
    'session_id': '18279',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "57",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID64_18267 = {
    'session_id': '18267',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "64",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID64_18280 = {
    'session_id': '18280',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "64",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID81_18268 = {
    'session_id': '18268',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "81",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID81_18281 = {
    'session_id': '18281',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "81",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID82_18269 = {
    'session_id': '18269',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "82",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID82_18282 = {
    'session_id': '18282',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "82",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID93_18270 = {
    'session_id': '18270',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "93",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID93_18283 = {
    'session_id': '18283',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "93",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPINFO_GID999_18271 = {
    'session_id': '18271',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "GID": "999",
        "a": "GroupInfo",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}

BUSINESSGROUP_GROUPLOG_GID999_18284 = {
    'session_id': '18284',
    'added_time': '2026-06-28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'hide_url_fields': ['GID'],
    'data': {
        "Day": "3",
        "GID": "999",
        "Index": "0",
        "Money": "5000000",
        "Order": "2",
        "SDay": "0",
        "st": "30",
        "a": "GroupLog",
        "c": "BusinessGroup",
        "DeviceID": "7905c37c-ccc6-3420-afbc-fbc91cd509b2",
        "Token": "0",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G988N Build/NRD90M)"
    },
}


REQUESTS = [
    USERINFO_APPNEWS,
    THEME_INFOGR,
    DATASTATISTICS_USERLOGIN,
    USERINFO_USERNEWS3,
    SYSTEM_ADGET,
    XIANHUODATA_GETXIANHUOLIST,
    COMMENTS_USERLISTNEW,
    USERSELECTSTOCK_UPDATESTATE,
    REQUEST_23,
    INDEX_GETINFO,
    SYSAPPVERSION_GETLAYOUT,
    INDEX_NEWGETLIST,
    INDEXPLATE_GETINDEXLIST,
    STOCKLINEDATA_GETKLINEDAY_W14,
    STOCKLINEDATA_GETKLINETODAY_W14,
    HOMEDINGPAN_MODULEVERSATILE,
    TASK_USEFUN,
    USERSELECTSTOCK_GETALLUSERSELSTOCK,
    ADMIN_L2DATESHOWHID,
    LONGHUBANG_TOPTITLE,
    LONGHUBANGDONGCAI_GETSTATE,
    LONGHUBANG_GETSTOCKLIST,
    LONGHUBANG_ADD,
    STOCK_GETSTOCKCHART,
    STOCK_GETNEWONESTOCKINFO,
    COMMENTS_GET,
    STOCK_GETNEWONESTOCKINFO_2,
    DATASTATISTICS_CALUSERCLICK,
    STOCKL2DATA_GETSTOCKTREND,
    DATASTATISTICS_CALUSERCLICK_2,
    STOCK_YYBTTEND,
    SYSTEM_MODULESWITCH,
    DATABATCHSTATISTICS_CALUSERCLICK,
    LOG_LOGUSERADDNEW,
    STOCK_YYBTTEND_2,
    STOCK_GETNEWESTDAY,
    LONGHUBANG_UPDATELIST,
    STOCKMESSAGEBAR_MESSAGEBARINFO,
    STOCKL2DATA_GETZHANGTINGGENE,
    STOCKL2DATA_GETSTOCKIDPLATE_NEW,
    INDEX_GETARTTITLE,
    DATABATCHSTATISTICS_CALUSERPAGE,
    LOG_LOGUSERADDNEW_2,
    FORUMSMSGCOLUMN_GETLIST,
    FORUMSMSGJX_GETFOCUSMSG,
    FORUMSMSGJX_GETFOCUSMSG_2,
    FORUMSMSGJX_GETSELLIST,
    SYSTEM_ADGETKHD,
    FORUMSMSGCOLUMN_GETINFO,
    INDEX_GETINFO_2,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST,
    NEWSTOCKRANKING_INDEXCHANGE,
    NEWSTOCKRANKING_ETFSTOCKRANKING,
    ZHISHUKLINE_GETZHISHUKLINE,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_2,
    DATASTATISTICS_CALUSERCLICK_3,
    ZHULICHICANG_GGLIST_JGCC,
    ZHULICHICANG_GGLIST_JGCC_2,
    DATASTATISTICS_CALUSERCLICK_4,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_3,
    INDEX_GETARTTITLE_2,
    DATASTATISTICS_CALUSERCLICK_5,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_4,
    DATABATCHSTATISTICS_CALUSERPAGE_2,
    LOG_LOGUSERADDNEW_3,
    STOCKL2DATA_GETSTOCKPERCENTTURNOVERTEN,
    STOCKL2DATA_GETWEITUO,
    LOG_LOGUSERADDNEW_4,
    DATABATCHSTATISTICS_CALUSERPAGE_3,
    STOCKL2DATA_GETZSTREND,
    STOCKYIDONGKANPAN_STOCKDPREALDATA,
    USERINFO_GETPERMISSION,
    STOCKYIDONGKANPAN_STOCKDPEXPLAIN,
    STOCKF10BASIC_GETINDEX,
    STOCKF10BASIC_BIGREMINDERW43,
    HISLIMITRESUMPTION_GETDAYZHANGTING,
    STOCKLINEDATA_GETKLINEZHANGTING,
    COMPANYNOTICE_CORPORATENEWSSTOCKLIST,
    COMPANYNOTICE_COMPANYNEWSREPORTLIST,
    COMPANYNOTICE_RESEARCHFIELDEXCEL,
    COMPANYNOTICE_RESEARCHFIELDLIST,
    INSTITUTIONALPOSITIONSINFO_INSTITUTIONALSHOWDATE,
    INSTITUTIONALPOSITIONSINFO_STOCKINSTITUTIONALPOSITIONS,
    INSTITUTIONALPOSITIONSINFO_STOCKHOLDINGFUND,
    FORUMSTUYERE_GETTAGLIST,
    FORUMSTUYERE_GETBYSTOCK,
    FORUMSTUYERE_GETBYSTOCK_2,
    LOG_LOGUSERADDNEW_5,
    INDEX_GETINFO_HQ_VIEW_2_7_9_10,
    INDEX_GETINFO_HQ_VIEW_3,
    INDEX_GETINFO_HQ_VIEW_4_5_11,
    ZHISHUL2DATA_GETVOLTURINCREMENTAL,
    ZHISHUL2DATA_GETTRENDINCREMENTAL,
    ZHISHUL2DATA_GETPARENTPLATECODE,
    ZHISHURANKING_GETPLATE_INFO_QJ,
    INDEX_GETARTTITLE_HQ_PLATE,
    ZHISHURANKING_SONPLATE_INFO,
    ZHISHURANKING_GETGPCPHBTS_TAG,
    CONCEPTIONPOINT_BKFENSHIZHIBO,
    INDEX_YOUZIDONGXIANGBYLIST,
    DATASTATISTICS_CALUSERCLICK_HAR_18001,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18003,
    USERSELECTSTOCK_REFRESHSTOCKLIST_HAR_18012,
    STOCKFENGKDATA_GETFENGKLIST_HAR_18013,
    STOCKFENGKDATA_GETFENGKYDPLATE_HAR_18019,
    STOCKFENGKDATA_GETFENGKLIST_HAR_18021,
    DATABATCHSTATISTICS_CALUSERPAGE_HAR_18026,
    DATASTATISTICS_CALUSERCLICK_HAR_18054,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18055,
    ZHISHURANKING_GETPLATE_INFO_QJ_HAR_18059,
    ZHISHURANKING_SONPLATE_INFO_HAR_18061,
    ZHISHURANKING_GETGPCPHBTS_TAG_HAR_18062,
    THEME_INFOBKR_HAR_18063,
    CONCEPTIONPOINT_BKFENSHIZHIBO_HAR_18065,
    FORUMSTUYERE_GETBYSTOCK_HAR_18071,
    DATASTATISTICS_CALUSERCLICK_HAR_18080,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18083,
    DATASTATISTICS_CALUSERCLICK_HAR_18090,
    DATASTATISTICS_CALUSERCLICK_HAR_18091,
    THEMENEWS_GETLIST_HAR_18092,
    DATASTATISTICS_CALUSERCLICK_HAR_18124,
    DATASTATISTICS_CALUSERCLICK_HAR_18125,
    THEMENEWS_GETLIST_HAR_18126,
    DATASTATISTICS_CALUSERCLICK_HAR_18127,
    THEMENEWS_GETCOLLECTNEWS_HAR_18128,
    DATASTATISTICS_CALUSERCLICK_HAR_18139,
    STOCKBIDYIDONG_GETPIANLIZHI_MANY_HAR_18157,
    DATABATCHSTATISTICS_CALUSERPAGE_HAR_18162,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_HAR_18181,
    STOCKBIDYIDONG_GETPIANLIZHI_INDEX_HAR_18182,
    DATASTATISTICS_CALUSERCLICK_HAR_18190,
    INDEX_GETARTTITLE_HAR_18191,
    DATASTATISTICS_CALUSERCLICK_HAR_18207,
    HISHOMEDINGPAN_CHANGESTATISTICS_EMOTION_HAR_18208,
    HISHOMEDINGPAN_MARKETSCLNKLINE_EMOTION_HAR_18209,
    HISHOMEDINGPAN_MARKETVOLUMEBENCHMARKLINE_EMOTION_HAR_18210,
    HOMEDINGPAN_MARKETCAPACITYKLINE_EMOTION_HAR_18211,
    APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_EMOTION_HAR_18212,
    HOMEDINGPAN_DAILYLIMITINDEX_EMOTION_HAR_18213,
    HOMEDINGPAN_MARKETSTOCKZDNUM_EMOTION_HAR_18214,
    XIANHUODATA_GETXIANHUOLIST_EMOTION_HAR_18215,
    HOMEDINGPAN_SHARPWITHDRAWALLIST_EMOTION_HAR_18216,
    HOMEDINGPAN_WEIGHTPERFORMANCELIST_EMOTION_HAR_18217,
    STOCKL2HISTORY_GETZSREAL_WITHDRAW_HISTORY_18218,
    HISHOMEDINGPAN_DAILYLIMITINDEX_HISTORY_18219,
    HISHOMEDINGPAN_DAILYLIMITPERFORMANCE_HISTORY_18220,
    HISHOMEDINGPAN_DAILYLIMITPERFORMANCE2_HISTORY_18221,
    HISHOMEDINGPAN_HISDABANLIST_HISTORY_18222,
    ZHISHUL2DATA_GETTRENDINCREMENTAL_HISTORY_18223,
    ZHISHUL2DATA_GETVOLTURINCREMENTAL_HISTORY_18224,
    STOCKLINEDATA_GETDADANKLINE2NEW_MARKET_VOLUME_18225,
    ZHISHUKLINE_GETZHISHUKLINE_LN_MARKET_VOLUME_18226,
    STOCKLINEDATA_GETKLINETODAYDADANNEW_MARKET_VOLUME_18227,
    ZHISHUKLINE_GETZHISHUKLINETODAY_LN_MARKET_VOLUME_18228,
    STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_HISTORY_18229,
    STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_REALTIME_18230,
    STOCKLINEDATA_GETINTERVIEWSBYDATEZS_HISTORY_18231,
    HISHOMEDINGPAN_MARKETSCLNKLINE_MARKET_VOLUME_HISTORY_18232,
    PAYFUNCREMINDNEW_GETREMIND_LATEST_THEME_18233,
    TICAI_READERCOUNT_LATEST_THEME_18234,
    ZHISHUL2DATA_GETPARENTPLATECODE_WINDVANE_18235,
    ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_18236,
    ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_18237,
    INDEX_GETARTTITLE_WINDVANE_18238,
    ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_HISTORY_18239,
    ZHISHURANKING_GETPLATE_INFO_QJ_WINDVANE_HISTORY_18240,
    ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_HISTORY_18241,
    ZHISHURANKING_SONPLATE_INFO_WINDVANE_HISTORY_18242,
    ZHISHURANKING_GETGPCPHBTS_TAG_WINDVANE_HISTORY_18243,
    HISCONCEPTIONPOINT_BKFENSHIZHIBO_WINDVANE_HISTORY_18244,
    ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_HISTORY_18245,
    ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB72_18246,
    ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB73_18247,
    ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB74_18248,
    LONGHUBANG_GETSTOCKLIST_TODAY_BOARD_18249,
    LONGHUBANG_GETAGENCYLISTV2_TODAY_BOARD_18250,
    LONGHUBANG_GETAGENCYKLINE_TODAY_BOARD_18251,
    LONGHUBANG_GETBUSINESSLIST_TODAY_BOARD_18252,
    LONGHUBANG_GETAGENCYDAYLIST_TODAY_BOARD_18253,
    BUSINESSGROUP_GROUPINFO_YOUZI_GROUP_18254,
    BUSINESSGROUP_GROUPLOG_YOUZI_GROUP_18255,
    USERBUSINESS_GETOFFICEV2_YOUZI_GROUP_18256,
    STOCK_GETSTOCKCHART_YOUZI_GROUP_18257,
    USERBUSINESS_GETDAY_TOP_YOUZI_18258,
    STOCKL2HISTORY_GETZSTREND_NARROW_HISTORY_18285,
    ZHISHURANKING_REALRANKINGINFO_HISTORY_18286,
    ZHISHURANKING_REALRANKINGINFO_TYPE1_ZSTYPE7_18287,
    ZHISHURANKING_REALRANKINGINFO_TYPE2_ZSTYPE4_18288,
    ZHISHURANKING_REALRANKINGINFO_TYPE2_ZSTYPE6_18289,
    ZHISHURANKING_REALRANKINGINFO_TYPENEG4_ZSTYPE4_18290,
    ZHISHURANKING_REALRANKINGINFO_TYPENEG4_ZSTYPE6_18291,
    BUSINESSGROUP_GROUPINFO_GID7_18259,
    BUSINESSGROUP_GROUPLOG_GID7_18272,
    BUSINESSGROUP_GROUPINFO_GID10_18260,
    BUSINESSGROUP_GROUPLOG_GID10_18273,
    BUSINESSGROUP_GROUPINFO_GID20_18261,
    BUSINESSGROUP_GROUPLOG_GID20_18274,
    BUSINESSGROUP_GROUPINFO_GID25_18262,
    BUSINESSGROUP_GROUPLOG_GID25_18275,
    BUSINESSGROUP_GROUPINFO_GID33_18263,
    BUSINESSGROUP_GROUPLOG_GID33_18276,
    BUSINESSGROUP_GROUPINFO_GID35_18264,
    BUSINESSGROUP_GROUPLOG_GID35_18277,
    BUSINESSGROUP_GROUPINFO_GID41_18265,
    BUSINESSGROUP_GROUPLOG_GID41_18278,
    BUSINESSGROUP_GROUPINFO_GID57_18266,
    BUSINESSGROUP_GROUPLOG_GID57_18279,
    BUSINESSGROUP_GROUPINFO_GID64_18267,
    BUSINESSGROUP_GROUPLOG_GID64_18280,
    BUSINESSGROUP_GROUPINFO_GID81_18268,
    BUSINESSGROUP_GROUPLOG_GID81_18281,
    BUSINESSGROUP_GROUPINFO_GID82_18269,
    BUSINESSGROUP_GROUPLOG_GID82_18282,
    BUSINESSGROUP_GROUPINFO_GID93_18270,
    BUSINESSGROUP_GROUPLOG_GID93_18283,
    BUSINESSGROUP_GROUPINFO_GID999_18271,
    BUSINESSGROUP_GROUPLOG_GID999_18284,
]


class KaipanlaCapturedClient:
    def __init__(self, timeout=DEFAULT_TIMEOUT, session=None, min_interval=DEFAULT_MIN_INTERVAL, jitter=DEFAULT_JITTER):
        self.timeout = timeout
        self.session = session or requests.Session()
        self.min_interval = min_interval
        self.jitter = jitter
        self._last_request_at = 0.0

    def _throttle(self):
        wait = self.min_interval + random.uniform(0, self.jitter)
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < wait:
            time.sleep(wait - elapsed)
        self._last_request_at = time.monotonic()

    def request(self, spec, data=None, params=None, headers=None):
        self._throttle()
        merged_params = dict(spec.get('params') or {})
        if params:
            merged_params.update({key: str(value) for key, value in params.items() if value is not None})

        merged_headers = dict(spec.get('headers') or {})
        merged_headers.update({
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
        })
        if headers:
            merged_headers.update(headers)

        response = self.session.request(
            spec['method'],
            spec['url'],
            params=merged_params,
            data=data if data is not None else spec.get('data'),
            headers=merged_headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response

    def userinfo_appnews(self, st=None, index=None, **overrides):
        """Replay session 1: UserInfo.AppNews."""
        data = dict(USERINFO_APPNEWS['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERINFO_APPNEWS, data=data)

    def theme_infogr(self, **overrides):
        """Replay session 2: Theme.InfoGR."""
        data = dict(THEME_INFOGR['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(THEME_INFOGR, data=data)

    def datastatistics_userlogin(self, **overrides):
        """Replay session 4: DataStatistics.UserLogin."""
        data = dict(DATASTATISTICS_USERLOGIN['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATASTATISTICS_USERLOGIN, data=data)

    def userinfo_usernews3(self, st=None, index=None, **overrides):
        """Replay session 7: UserInfo.UserNews3."""
        data = dict(USERINFO_USERNEWS3['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERINFO_USERNEWS3, data=data)

    def system_adget(self, type=None, **overrides):
        """Replay session 10: System.AdGet."""
        data = dict(SYSTEM_ADGET['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_ADGET, data=data)

    def xianhuodata_getxianhuolist(self, time=None, **overrides):
        """Replay session 14: XianHuoData.GetXianHuoList."""
        data = dict(XIANHUODATA_GETXIANHUOLIST['data'])
        if time is not None:
            data['Time'] = str(time)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(XIANHUODATA_GETXIANHUOLIST, data=data)

    def comments_userlistnew(self, **overrides):
        """Replay session 15: Comments.UserListNew."""
        data = dict(COMMENTS_USERLISTNEW['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(COMMENTS_USERLISTNEW, data=data)

    def userselectstock_updatestate(self, **overrides):
        """Replay session 19: UserSelectStock.UpdateState."""
        data = dict(USERSELECTSTOCK_UPDATESTATE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERSELECTSTOCK_UPDATESTATE, data=data)

    def request_23(self, **overrides):
        """Replay session 23: request.23."""
        data = dict(REQUEST_23['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(REQUEST_23, data=data)

    def index_getinfo(self, view=None, **overrides):
        """Replay session 52: Index.GetInfo."""
        data = dict(INDEX_GETINFO['data'])
        if view is not None:
            data['View'] = str(view)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_GETINFO, data=data)

    def sysappversion_getlayout(self, **overrides):
        """Replay session 53: SysAppVersion.GetLaYout."""
        data = dict(SYSAPPVERSION_GETLAYOUT['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSAPPVERSION_GETLAYOUT, data=data)

    def index_newgetlist(self, **overrides):
        """Replay session 54: Index.NewGetList."""
        data = dict(INDEX_NEWGETLIST['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_NEWGETLIST, data=data)

    def indexplate_getindexlist(self, view=None, st=None, type=None, **overrides):
        """Replay session 56: IndexPlate.GetIndexList."""
        data = dict(INDEXPLATE_GETINDEXLIST['data'])
        if view is not None:
            data['view'] = str(view)
        if st is not None:
            data['st'] = str(st)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEXPLATE_GETINDEXLIST, data=data)

    def stocklinedata_getklineday_w14(self, st=None, index=None, type=None, stockid=None, **overrides):
        """Replay session 108: StockLineData.GetKLineDay_W14."""
        data = dict(STOCKLINEDATA_GETKLINEDAY_W14['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETKLINEDAY_W14, data=data)

    def stocklinedata_getklinetoday_w14(self, type=None, stockid=None, **overrides):
        """Replay session 111: StockLineData.GetKLineToday_W14."""
        data = dict(STOCKLINEDATA_GETKLINETODAY_W14['data'])
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETKLINETODAY_W14, data=data)

    def homedingpan_moduleversatile(self, **overrides):
        """Replay session 112: HomeDingPan.ModuleVersatile."""
        data = dict(HOMEDINGPAN_MODULEVERSATILE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HOMEDINGPAN_MODULEVERSATILE, data=data)

    def task_usefun(self, **overrides):
        """Replay session 119: Task.UseFun."""
        data = dict(TASK_USEFUN['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(TASK_USEFUN, data=data)

    def userselectstock_getalluserselstock(self, **overrides):
        """Replay session 120: UserSelectStock.GetAllUserSelStock."""
        data = dict(USERSELECTSTOCK_GETALLUSERSELSTOCK['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERSELECTSTOCK_GETALLUSERSELSTOCK, data=data)

    def admin_l2dateshowhid(self, **overrides):
        """Replay session 121: Admin.L2DateShowHid."""
        data = dict(ADMIN_L2DATESHOWHID['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ADMIN_L2DATESHOWHID, data=data)

    def longhubang_toptitle(self, **overrides):
        """Replay session 122: LongHuBang.TopTitle."""
        data = dict(LONGHUBANG_TOPTITLE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_TOPTITLE, data=data)

    def longhubangdongcai_getstate(self, **overrides):
        """Replay session 123: LongHuBangDongCai.GetState."""
        data = dict(LONGHUBANGDONGCAI_GETSTATE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANGDONGCAI_GETSTATE, data=data)

    def longhubang_getstocklist(self, st=None, time=None, index=None, type=None, **overrides):
        """Replay session 126: LongHuBang.GetStockList."""
        data = dict(LONGHUBANG_GETSTOCKLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if time is not None:
            data['Time'] = str(time)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETSTOCKLIST, data=data)

    def longhubang_add(self, time=None, stockid=None, **overrides):
        """Replay session 128: LongHuBang.Add."""
        data = dict(LONGHUBANG_ADD['data'])
        if time is not None:
            data['Time'] = str(time)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_ADD, data=data)

    def stock_getstockchart(self, stockid=None, index=None, st=None, **overrides):
        """Replay session 146: Stock.GetStockChart."""
        data = dict(STOCK_GETSTOCKCHART['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        if index is not None:
            data['Index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETSTOCKCHART, data=data)

    def stock_getnewonestockinfo(self, type=None, time=None, stockid=None, **overrides):
        """Replay session 147: Stock.GetNewOneStockInfo."""
        data = dict(STOCK_GETNEWONESTOCKINFO['data'])
        if type is not None:
            data['Type'] = str(type)
        if time is not None:
            data['Time'] = str(time)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETNEWONESTOCKINFO, data=data)

    def comments_get(self, index=None, st=None, stockid=None, day=None, type=None, tsort=None, **overrides):
        """Replay session 159: Comments.Get."""
        data = dict(COMMENTS_GET['data'])
        if index is not None:
            data['Index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        if stockid is not None:
            data['StockID'] = str(stockid)
        if day is not None:
            data['Day'] = str(day)
        if type is not None:
            data['Type'] = str(type)
        if tsort is not None:
            data['Tsort'] = str(tsort)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(COMMENTS_GET, data=data)

    def stock_getnewonestockinfo_2(self, type=None, time=None, stockid=None, **overrides):
        """Replay session 193: Stock.GetNewOneStockInfo."""
        data = dict(STOCK_GETNEWONESTOCKINFO_2['data'])
        if type is not None:
            data['Type'] = str(type)
        if time is not None:
            data['Time'] = str(time)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETNEWONESTOCKINFO_2, data=data)

    def datastatistics_caluserclick(self, **overrides):
        """Replay session 194: DataStatistics.CalUserClick."""
        data = dict(DATASTATISTICS_CALUSERCLICK['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATASTATISTICS_CALUSERCLICK, data=data)

    def stockl2data_getstocktrend(self, stockid=None, day=None, **overrides):
        """Replay session 196: StockL2Data.GetStockTrend."""
        data = dict(STOCKL2DATA_GETSTOCKTREND['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        if day is not None:
            data['Day'] = str(day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2DATA_GETSTOCKTREND, data=data)

    def datastatistics_caluserclick_2(self, **overrides):
        """Replay session 197: DataStatistics.CalUserClick."""
        data = dict(DATASTATISTICS_CALUSERCLICK_2['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATASTATISTICS_CALUSERCLICK_2, data=data)

    def stock_yybttend(self, **overrides):
        """Replay session 199: Stock.YYBTtend."""
        data = dict(STOCK_YYBTTEND['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_YYBTTEND, data=data)

    def system_moduleswitch(self, **overrides):
        """Replay session 200: System.ModuleSwitch."""
        data = dict(SYSTEM_MODULESWITCH['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_MODULESWITCH, data=data)

    def databatchstatistics_caluserclick(self, **overrides):
        """Replay session 209: DataBatchStatistics.CalUserClick."""
        data = dict(DATABATCHSTATISTICS_CALUSERCLICK['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATABATCHSTATISTICS_CALUSERCLICK, data=data)

    def log_loguseraddnew(self, **overrides):
        """Replay session 210: Log.LogUserAddNew."""
        data = dict(LOG_LOGUSERADDNEW['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LOG_LOGUSERADDNEW, data=data)

    def stock_yybttend_2(self, **overrides):
        """Replay session 211: Stock.YYBTtend."""
        data = dict(STOCK_YYBTTEND_2['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_YYBTTEND_2, data=data)

    def stock_getnewestday(self, stockid=None, **overrides):
        """Replay session 213: Stock.GetNewestDay."""
        data = dict(STOCK_GETNEWESTDAY['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETNEWESTDAY, data=data)

    def longhubang_updatelist(self, **overrides):
        """Replay session 214: LongHuBang.UpdateList."""
        data = dict(LONGHUBANG_UPDATELIST['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_UPDATELIST, data=data)

    def stockmessagebar_messagebarinfo(self, stockid=None, **overrides):
        """Replay session 215: StockMessageBar.MessageBarInfo."""
        data = dict(STOCKMESSAGEBAR_MESSAGEBARINFO['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKMESSAGEBAR_MESSAGEBARINFO, data=data)

    def stockl2data_getzhangtinggene(self, stockid=None, **overrides):
        """Replay session 216: StockL2Data.GetZhangTingGene."""
        data = dict(STOCKL2DATA_GETZHANGTINGGENE['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2DATA_GETZHANGTINGGENE, data=data)

    def stockl2data_getstockidplate_new(self, stockid=None, **overrides):
        """Replay session 217: StockL2Data.GetStockIDPlate_New."""
        data = dict(STOCKL2DATA_GETSTOCKIDPLATE_NEW['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2DATA_GETSTOCKIDPLATE_NEW, data=data)

    def index_getarttitle(self, type=None, stockid=None, **overrides):
        """Replay session 218: Index.GetArtTitle."""
        data = dict(INDEX_GETARTTITLE['data'])
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_GETARTTITLE, data=data)

    def databatchstatistics_caluserpage(self, **overrides):
        """Replay session 265: DataBatchStatistics.CalUserPage."""
        data = dict(DATABATCHSTATISTICS_CALUSERPAGE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATABATCHSTATISTICS_CALUSERPAGE, data=data)

    def log_loguseraddnew_2(self, **overrides):
        """Replay session 267: Log.LogUserAddNew."""
        data = dict(LOG_LOGUSERADDNEW_2['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LOG_LOGUSERADDNEW_2, data=data)

    def forumsmsgcolumn_getlist(self, st=None, index=None, **overrides):
        """Replay session 272: ForumsMsgColumn.GetList."""
        data = dict(FORUMSMSGCOLUMN_GETLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSMSGCOLUMN_GETLIST, data=data)

    def forumsmsgjx_getfocusmsg(self, type=None, **overrides):
        """Replay session 273: ForumsMsgJX.GetFocusMsg."""
        data = dict(FORUMSMSGJX_GETFOCUSMSG['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSMSGJX_GETFOCUSMSG, data=data)

    def forumsmsgjx_getfocusmsg_2(self, st=None, index=None, type=None, preindex=None, **overrides):
        """Replay session 274: ForumsMsgJX.GetFocusMsg."""
        data = dict(FORUMSMSGJX_GETFOCUSMSG_2['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        if preindex is not None:
            data['PreIndex'] = str(preindex)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSMSGJX_GETFOCUSMSG_2, data=data)

    def forumsmsgjx_getsellist(self, st=None, index=None, preindex=None, **overrides):
        """Replay session 277: ForumsMsgJX.GetSelList."""
        data = dict(FORUMSMSGJX_GETSELLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if preindex is not None:
            data['PreIndex'] = str(preindex)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSMSGJX_GETSELLIST, data=data)

    def system_adgetkhd(self, type=None, **overrides):
        """Replay session 278: System.AdGetKHD."""
        data = dict(SYSTEM_ADGETKHD['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_ADGETKHD, data=data)

    def forumsmsgcolumn_getinfo(self, st=None, index=None, preindex=None, **overrides):
        """Replay session 287: ForumsMsgColumn.GetInfo."""
        data = dict(FORUMSMSGCOLUMN_GETINFO['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if preindex is not None:
            data['PreIndex'] = str(preindex)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSMSGCOLUMN_GETINFO, data=data)

    def index_getinfo_2(self, view=None, **overrides):
        """Replay session 298: Index.GetInfo."""
        data = dict(INDEX_GETINFO_2['data'])
        if view is not None:
            data['View'] = str(view)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_GETINFO_2, data=data)

    def appfuncexplain_getfunction_art_last(self, **overrides):
        """Replay session 310: AppFuncExplain.GetFunction_Art_Last."""
        data = dict(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST, data=data)

    def newstockranking_indexchange(self, **overrides):
        """Replay session 311: NewStockRanking.IndexChange."""
        data = dict(NEWSTOCKRANKING_INDEXCHANGE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(NEWSTOCKRANKING_INDEXCHANGE, data=data)

    def newstockranking_etfstockranking(self, order=None, st=None, index=None, type=None, **overrides):
        """Replay session 312: NewStockRanking.ETFStockRanking."""
        data = dict(NEWSTOCKRANKING_ETFSTOCKRANKING['data'])
        if order is not None:
            data['Order'] = str(order)
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(NEWSTOCKRANKING_ETFSTOCKRANKING, data=data)

    def zhishukline_getzhishukline(self, st=None, index=None, type=None, stockid=None, **overrides):
        """Replay session 313: ZhiShuKLine.GetZhiShuKLine."""
        data = dict(ZHISHUKLINE_GETZHISHUKLINE['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUKLINE_GETZHISHUKLINE, data=data)

    def appfuncexplain_getfunction_art_last_2(self, **overrides):
        """Replay session 319: AppFuncExplain.GetFunction_Art_Last."""
        data = dict(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_2['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_2, data=data)

    def datastatistics_caluserclick_3(self, **overrides):
        """Replay session 325: DataStatistics.CalUserClick."""
        data = dict(DATASTATISTICS_CALUSERCLICK_3['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATASTATISTICS_CALUSERCLICK_3, data=data)

    def zhulichicang_gglist_jgcc(self, type=None, order=None, index=None, st=None, **overrides):
        """Replay session 326: ZhuLiChiCang.GGList_JGCC."""
        data = dict(ZHULICHICANG_GGLIST_JGCC['data'])
        if type is not None:
            data['Type'] = str(type)
        if order is not None:
            data['Order'] = str(order)
        if index is not None:
            data['Index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHULICHICANG_GGLIST_JGCC, data=data)

    def zhulichicang_gglist_jgcc_2(self, type=None, order=None, index=None, st=None, **overrides):
        """Replay session 329: ZhuLiChiCang.GGList_JGCC."""
        data = dict(ZHULICHICANG_GGLIST_JGCC_2['data'])
        if type is not None:
            data['Type'] = str(type)
        if order is not None:
            data['Order'] = str(order)
        if index is not None:
            data['Index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHULICHICANG_GGLIST_JGCC_2, data=data)

    def datastatistics_caluserclick_4(self, **overrides):
        """Replay session 335: DataStatistics.CalUserClick."""
        data = dict(DATASTATISTICS_CALUSERCLICK_4['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATASTATISTICS_CALUSERCLICK_4, data=data)

    def appfuncexplain_getfunction_art_last_3(self, **overrides):
        """Replay session 336: AppFuncExplain.GetFunction_Art_Last."""
        data = dict(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_3['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_3, data=data)

    def index_getarttitle_2(self, type=None, **overrides):
        """Replay session 337: Index.GetArtTitle."""
        data = dict(INDEX_GETARTTITLE_2['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_GETARTTITLE_2, data=data)

    def datastatistics_caluserclick_5(self, **overrides):
        """Replay session 342: DataStatistics.CalUserClick."""
        data = dict(DATASTATISTICS_CALUSERCLICK_5['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATASTATISTICS_CALUSERCLICK_5, data=data)

    def appfuncexplain_getfunction_art_last_4(self, **overrides):
        """Replay session 343: AppFuncExplain.GetFunction_Art_Last."""
        data = dict(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_4['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_4, data=data)

    def databatchstatistics_caluserpage_2(self, **overrides):
        """Replay session 352: DataBatchStatistics.CalUserPage."""
        data = dict(DATABATCHSTATISTICS_CALUSERPAGE_2['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATABATCHSTATISTICS_CALUSERPAGE_2, data=data)

    def log_loguseraddnew_3(self, **overrides):
        """Replay session 354: Log.LogUserAddNew."""
        data = dict(LOG_LOGUSERADDNEW_3['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LOG_LOGUSERADDNEW_3, data=data)

    def stockl2data_getstockpercentturnoverten(self, stockid=None, **overrides):
        """Replay session 374: StockL2Data.GetStockPercentTurnoverTen."""
        data = dict(STOCKL2DATA_GETSTOCKPERCENTTURNOVERTEN['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2DATA_GETSTOCKPERCENTTURNOVERTEN, data=data)

    def stockl2data_getweituo(self, st=None, type=None, stockid=None, **overrides):
        """Replay session 375: StockL2Data.GetWeiTuo."""
        data = dict(STOCKL2DATA_GETWEITUO['data'])
        if st is not None:
            data['st'] = str(st)
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2DATA_GETWEITUO, data=data)

    def log_loguseraddnew_4(self, **overrides):
        """Replay session 383: Log.LogUserAddNew."""
        data = dict(LOG_LOGUSERADDNEW_4['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LOG_LOGUSERADDNEW_4, data=data)

    def databatchstatistics_caluserpage_3(self, **overrides):
        """Replay session 387: DataBatchStatistics.CalUserPage."""
        data = dict(DATABATCHSTATISTICS_CALUSERPAGE_3['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(DATABATCHSTATISTICS_CALUSERPAGE_3, data=data)

    def stockl2data_getzstrend(self, stockid=None, **overrides):
        """Replay session 407: StockL2Data.GetZstrend."""
        data = dict(STOCKL2DATA_GETZSTREND['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2DATA_GETZSTREND, data=data)

    def stockyidongkanpan_stockdprealdata(self, stockid=None, **overrides):
        """Replay session 413: StockYiDongKanPan.StockDPRealData."""
        data = dict(STOCKYIDONGKANPAN_STOCKDPREALDATA['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKYIDONGKANPAN_STOCKDPREALDATA, data=data)

    def userinfo_getpermission(self, type=None, **overrides):
        """Replay session 414: UserInfo.GetPermission."""
        data = dict(USERINFO_GETPERMISSION['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERINFO_GETPERMISSION, data=data)

    def stockyidongkanpan_stockdpexplain(self, stockid=None, **overrides):
        """Replay session 415: StockYiDongKanPan.StockDPExplain."""
        data = dict(STOCKYIDONGKANPAN_STOCKDPEXPLAIN['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKYIDONGKANPAN_STOCKDPEXPLAIN, data=data)

    def stockf10basic_getindex(self, stockid=None, **overrides):
        """Replay session 418: StockF10Basic.GetIndex."""
        data = dict(STOCKF10BASIC_GETINDEX['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKF10BASIC_GETINDEX, data=data)

    def stockf10basic_bigreminderw43(self, st=None, index=None, stockid=None, **overrides):
        """Replay session 419: StockF10Basic.BigReminderW43."""
        data = dict(STOCKF10BASIC_BIGREMINDERW43['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKF10BASIC_BIGREMINDERW43, data=data)

    def hislimitresumption_getdayzhangting(self, st=None, index=None, stockid=None, **overrides):
        """Replay session 420: HisLimitResumption.GetDayZhangTing."""
        data = dict(HISLIMITRESUMPTION_GETDAYZHANGTING['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISLIMITRESUMPTION_GETDAYZHANGTING, data=data)

    def stocklinedata_getklinezhangting(self, stockid=None, **overrides):
        """Replay session 421: StockLineData.GetKLineZhangTing."""
        data = dict(STOCKLINEDATA_GETKLINEZHANGTING['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETKLINEZHANGTING, data=data)

    def companynotice_corporatenewsstocklist(self, st=None, stockid=None, index=None, **overrides):
        """Replay session 422: CompanyNotice.CorporateNewsStockList."""
        data = dict(COMPANYNOTICE_CORPORATENEWSSTOCKLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if stockid is not None:
            data['StockID'] = str(stockid)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(COMPANYNOTICE_CORPORATENEWSSTOCKLIST, data=data)

    def companynotice_companynewsreportlist(self, st=None, type=None, stockid=None, index=None, **overrides):
        """Replay session 423: CompanyNotice.CompanyNewsReportList."""
        data = dict(COMPANYNOTICE_COMPANYNEWSREPORTLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(COMPANYNOTICE_COMPANYNEWSREPORTLIST, data=data)

    def companynotice_researchfieldexcel(self, stockid=None, **overrides):
        """Replay session 424: CompanyNotice.ResearchFieldExcel."""
        data = dict(COMPANYNOTICE_RESEARCHFIELDEXCEL['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(COMPANYNOTICE_RESEARCHFIELDEXCEL, data=data)

    def companynotice_researchfieldlist(self, st=None, index=None, type=None, stockid=None, **overrides):
        """Replay session 425: CompanyNotice.ResearchFieldList."""
        data = dict(COMPANYNOTICE_RESEARCHFIELDLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(COMPANYNOTICE_RESEARCHFIELDLIST, data=data)

    def institutionalpositionsinfo_institutionalshowdate(self, stockid=None, **overrides):
        """Replay session 426: InstitutionalPositionsInfo.InstitutionalShowDate."""
        data = dict(INSTITUTIONALPOSITIONSINFO_INSTITUTIONALSHOWDATE['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INSTITUTIONALPOSITIONSINFO_INSTITUTIONALSHOWDATE, data=data)

    def institutionalpositionsinfo_stockinstitutionalpositions(self, stockid=None, season=None, **overrides):
        """Replay session 427: InstitutionalPositionsInfo.StockInstitutionalPositions."""
        data = dict(INSTITUTIONALPOSITIONSINFO_STOCKINSTITUTIONALPOSITIONS['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        if season is not None:
            data['Season'] = str(season)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INSTITUTIONALPOSITIONSINFO_STOCKINSTITUTIONALPOSITIONS, data=data)

    def institutionalpositionsinfo_stockholdingfund(self, st=None, index=None, type=None, stockid=None, season=None, **overrides):
        """Replay session 428: InstitutionalPositionsInfo.StockHoldingFund."""
        data = dict(INSTITUTIONALPOSITIONSINFO_STOCKHOLDINGFUND['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        if stockid is not None:
            data['StockID'] = str(stockid)
        if season is not None:
            data['Season'] = str(season)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INSTITUTIONALPOSITIONSINFO_STOCKHOLDINGFUND, data=data)

    def forumstuyere_gettaglist(self, **overrides):
        """Replay session 429: ForumsTuyere.GetTagList."""
        data = dict(FORUMSTUYERE_GETTAGLIST['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSTUYERE_GETTAGLIST, data=data)

    def forumstuyere_getbystock(self, st=None, index=None, code=None, type=None, **overrides):
        """Replay session 430: ForumsTuyere.GetByStock."""
        data = dict(FORUMSTUYERE_GETBYSTOCK['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if code is not None:
            data['Code'] = str(code)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSTUYERE_GETBYSTOCK, data=data)

    def forumstuyere_getbystock_2(self, st=None, index=None, code=None, type=None, **overrides):
        """Replay session 432: ForumsTuyere.GetByStock."""
        data = dict(FORUMSTUYERE_GETBYSTOCK_2['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        if code is not None:
            data['Code'] = str(code)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(FORUMSTUYERE_GETBYSTOCK_2, data=data)

    def log_loguseraddnew_5(self, **overrides):
        """Replay session 446: Log.LogUserAddNew."""
        data = dict(LOG_LOGUSERADDNEW_5['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LOG_LOGUSERADDNEW_5, data=data)

    def index_youzidongxiangbylist(self, time=None, **overrides):
        """Replay session 1880: Index.YouZiDongXiangByList."""
        data = dict(INDEX_YOUZIDONGXIANGBYLIST['data'])
        if time is not None:
            data['Time'] = str(time)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_YOUZIDONGXIANGBYLIST, data=data)


    def hishomedingpan_changestatistics_emotion(self, st=None, index=None, **overrides):
        """Replay session 18208: HisHomeDingPan.ChangeStatistics."""
        data = dict(HISHOMEDINGPAN_CHANGESTATISTICS_EMOTION_HAR_18208['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_CHANGESTATISTICS_EMOTION_HAR_18208, data=data)

    def hishomedingpan_marketsclnkline_emotion(self, type=None, **overrides):
        """Replay session 18209: HisHomeDingPan.MarketSCLNKLine."""
        data = dict(HISHOMEDINGPAN_MARKETSCLNKLINE_EMOTION_HAR_18209['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_MARKETSCLNKLINE_EMOTION_HAR_18209, data=data)

    def hishomedingpan_marketvolumebenchmarkline_emotion(self, **overrides):
        """Replay session 18210: HisHomeDingPan.MarketVolumeBenchmarkLine."""
        data = dict(HISHOMEDINGPAN_MARKETVOLUMEBENCHMARKLINE_EMOTION_HAR_18210['data'])
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_MARKETVOLUMEBENCHMARKLINE_EMOTION_HAR_18210, data=data)

    def homedingpan_marketcapacitykline_emotion(self, type=None, **overrides):
        """Replay session 18211: HomeDingPan.MarketCapacityKLine."""
        data = dict(HOMEDINGPAN_MARKETCAPACITYKLINE_EMOTION_HAR_18211['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HOMEDINGPAN_MARKETCAPACITYKLINE_EMOTION_HAR_18211, data=data)

    def appfuncexplain_getfunction_art_last_emotion(self, funcname=None, **overrides):
        """Replay session 18212: AppFuncExplain.GetFunction_Art_Last."""
        data = dict(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_EMOTION_HAR_18212['data'])
        if funcname is not None:
            data['FuncName'] = str(funcname)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(APPFUNCEXPLAIN_GETFUNCTION_ART_LAST_EMOTION_HAR_18212, data=data)

    def homedingpan_dailylimitindex_emotion(self, **overrides):
        """Replay session 18213: HomeDingPan.DailyLimitIndex."""
        data = dict(HOMEDINGPAN_DAILYLIMITINDEX_EMOTION_HAR_18213['data'])
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HOMEDINGPAN_DAILYLIMITINDEX_EMOTION_HAR_18213, data=data)

    def homedingpan_marketstockzdnum_emotion(self, **overrides):
        """Replay session 18214: HomeDingPan.MarketStockZDNum."""
        data = dict(HOMEDINGPAN_MARKETSTOCKZDNUM_EMOTION_HAR_18214['data'])
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HOMEDINGPAN_MARKETSTOCKZDNUM_EMOTION_HAR_18214, data=data)

    def xianhuodata_getxianhuolist_emotion(self, time=None, **overrides):
        """Replay session 18215: XianHuoData.GetXianHuoList."""
        data = dict(XIANHUODATA_GETXIANHUOLIST_EMOTION_HAR_18215['data'])
        if time is not None:
            data['Time'] = str(time)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(XIANHUODATA_GETXIANHUOLIST_EMOTION_HAR_18215, data=data)

    def homedingpan_sharpwithdrawallist_emotion(self, index=None, order=None, st=None, type=None, **overrides):
        """Replay session 18216: HomeDingPan.SharpWithdrawalList."""
        data = dict(HOMEDINGPAN_SHARPWITHDRAWALLIST_EMOTION_HAR_18216['data'])
        if index is not None:
            data['Index'] = str(index)
        if order is not None:
            data['Order'] = str(order)
        if st is not None:
            data['st'] = str(st)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HOMEDINGPAN_SHARPWITHDRAWALLIST_EMOTION_HAR_18216, data=data)

    def homedingpan_weightperformancelist_emotion(self, index=None, order=None, st=None, type=None, **overrides):
        """Replay session 18217: HomeDingPan.WeightPerformanceList."""
        data = dict(HOMEDINGPAN_WEIGHTPERFORMANCELIST_EMOTION_HAR_18217['data'])
        if index is not None:
            data['Index'] = str(index)
        if order is not None:
            data['Order'] = str(order)
        if st is not None:
            data['st'] = str(st)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HOMEDINGPAN_WEIGHTPERFORMANCELIST_EMOTION_HAR_18217, data=data)


    def stockl2history_getzsreal_withdraw_history(self, Day=None, **overrides):
        """Replay session 18218: StockL2History.GetZsReal."""
        data = dict(STOCKL2HISTORY_GETZSREAL_WITHDRAW_HISTORY_18218['data'])
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2HISTORY_GETZSREAL_WITHDRAW_HISTORY_18218, data=data)


    def hishomedingpan_dailylimitindex_history(self, Day=None, **overrides):
        """Replay session 18219: HisHomeDingPan.DailyLimitIndex."""
        data = dict(HISHOMEDINGPAN_DAILYLIMITINDEX_HISTORY_18219['data'])
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_DAILYLIMITINDEX_HISTORY_18219, data=data)

    def hishomedingpan_dailylimitperformance_history(self, Day=None, PidType=None, Index=None, Order=None, st=None, Type=None, **overrides):
        """Replay session 18220: HisHomeDingPan.DailyLimitPerformance."""
        data = dict(HISHOMEDINGPAN_DAILYLIMITPERFORMANCE_HISTORY_18220['data'])
        if Day is not None:
            data['Day'] = str(Day)
        if PidType is not None:
            data['PidType'] = str(PidType)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if st is not None:
            data['st'] = str(st)
        if Type is not None:
            data['Type'] = str(Type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_DAILYLIMITPERFORMANCE_HISTORY_18220, data=data)

    def hishomedingpan_dailylimitperformance2_history(self, Day=None, PidType=None, Index=None, Order=None, st=None, Type=None, **overrides):
        """Replay session 18221: HisHomeDingPan.DailyLimitPerformance2."""
        data = dict(HISHOMEDINGPAN_DAILYLIMITPERFORMANCE2_HISTORY_18221['data'])
        if Day is not None:
            data['Day'] = str(Day)
        if PidType is not None:
            data['PidType'] = str(PidType)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if st is not None:
            data['st'] = str(st)
        if Type is not None:
            data['Type'] = str(Type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_DAILYLIMITPERFORMANCE2_HISTORY_18221, data=data)


    def hishomedingpan_hisdabanlist_history(self, Day=None, PidType=None, Index=None, Order=None, st=None, Type=None, **overrides):
        """Replay session 18222: HisHomeDingPan.HisDaBanList."""
        data = dict(HISHOMEDINGPAN_HISDABANLIST_HISTORY_18222['data'])
        if Day is not None:
            data['Day'] = str(Day)
        if PidType is not None:
            data['PidType'] = str(PidType)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if st is not None:
            data['st'] = str(st)
        if Type is not None:
            data['Type'] = str(Type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_HISDABANLIST_HISTORY_18222, data=data)

    def zhishul2data_gettrendincremental_history(self, Day=None, StockID=None, **overrides):
        """Replay session 18223: ZhiShuL2Data.GetTrendIncremental."""
        data = dict(ZHISHUL2DATA_GETTRENDINCREMENTAL_HISTORY_18223['data'])
        if Day is not None:
            data['Day'] = str(Day)
        if StockID is not None:
            data['StockID'] = str(StockID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETTRENDINCREMENTAL_HISTORY_18223, data=data)

    def zhishul2data_getvolturincremental_history(self, Day=None, StockID=None, **overrides):
        """Replay session 18224: ZhiShuL2Data.GetVolTurIncremental."""
        data = dict(ZHISHUL2DATA_GETVOLTURINCREMENTAL_HISTORY_18224['data'])
        if Day is not None:
            data['Day'] = str(Day)
        if StockID is not None:
            data['StockID'] = str(StockID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETVOLTURINCREMENTAL_HISTORY_18224, data=data)


    def stocklinedata_getdadankline2new_market_volume(self, StockID=None, Index=None, Type=None, st=None, **overrides):
        """Replay session 18225: StockLineData.GetDaDanKLine2New."""
        data = dict(STOCKLINEDATA_GETDADANKLINE2NEW_MARKET_VOLUME_18225['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if Index is not None:
            data['Index'] = str(Index)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETDADANKLINE2NEW_MARKET_VOLUME_18225, data=data)

    def zhishukline_getzhishukline_ln_market_volume(self, Index=None, Type=None, st=None, **overrides):
        """Replay session 18226: ZhiShuKLine.GetZhiShuKLine_LN."""
        data = dict(ZHISHUKLINE_GETZHISHUKLINE_LN_MARKET_VOLUME_18226['data'])
        if Index is not None:
            data['Index'] = str(Index)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUKLINE_GETZHISHUKLINE_LN_MARKET_VOLUME_18226, data=data)

    def stocklinedata_getklinetodaydadannew_market_volume(self, StockID=None, Type=None, **overrides):
        """Replay session 18227: StockLineData.GetKLineTodayDaDanNew."""
        data = dict(STOCKLINEDATA_GETKLINETODAYDADANNEW_MARKET_VOLUME_18227['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if Type is not None:
            data['Type'] = str(Type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETKLINETODAYDADANNEW_MARKET_VOLUME_18227, data=data)

    def zhishukline_getzhishuklinetoday_ln_market_volume(self, Type=None, **overrides):
        """Replay session 18228: ZhiShuKLine.GetZhiShuKLineToday_LN."""
        data = dict(ZHISHUKLINE_GETZHISHUKLINETODAY_LN_MARKET_VOLUME_18228['data'])
        if Type is not None:
            data['Type'] = str(Type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUKLINE_GETZHISHUKLINETODAY_LN_MARKET_VOLUME_18228, data=data)

    def stocklinedata_getinterviewsbydatestock_history(self, DStart=None, DEnd=None, Index=None, Order=None, Type=None, st=None, **overrides):
        """Replay session 18229: StockLineData.GetInterviewsByDateStock."""
        data = dict(STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_HISTORY_18229['data'])
        if DStart is not None:
            data['DStart'] = str(DStart)
        if DEnd is not None:
            data['DEnd'] = str(DEnd)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_HISTORY_18229, data=data)

    def stocklinedata_getinterviewsbydatestock_realtime(self, DStart=None, DEnd=None, Index=None, Order=None, Type=None, st=None, **overrides):
        """Replay session 18230: StockLineData.GetInterviewsByDateStock."""
        data = dict(STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_REALTIME_18230['data'])
        if DStart is not None:
            data['DStart'] = str(DStart)
        if DEnd is not None:
            data['DEnd'] = str(DEnd)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETINTERVIEWSBYDATESTOCK_REALTIME_18230, data=data)

    def stocklinedata_getinterviewsbydatezs_history(self, DStart=None, DEnd=None, Index=None, Order=None, Type=None, st=None, **overrides):
        """Replay session 18231: StockLineData.GetInterviewsByDateZS."""
        data = dict(STOCKLINEDATA_GETINTERVIEWSBYDATEZS_HISTORY_18231['data'])
        if DStart is not None:
            data['DStart'] = str(DStart)
        if DEnd is not None:
            data['DEnd'] = str(DEnd)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKLINEDATA_GETINTERVIEWSBYDATEZS_HISTORY_18231, data=data)


    def hishomedingpan_marketsclnkline_market_volume_history(self, Type=None, **overrides):
        """Replay session 18232: HisHomeDingPan.MarketSCLNKLine."""
        data = dict(HISHOMEDINGPAN_MARKETSCLNKLINE_MARKET_VOLUME_HISTORY_18232['data'])
        if Type is not None:
            data['Type'] = str(Type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISHOMEDINGPAN_MARKETSCLNKLINE_MARKET_VOLUME_HISTORY_18232, data=data)


    def payfuncremindnew_getremind_latest_theme(self, NID=None, **overrides):
        """Replay session 18233: PayFuncRemindNew.GetRemind."""
        data = dict(PAYFUNCREMINDNEW_GETREMIND_LATEST_THEME_18233['data'])
        if NID is not None:
            data['NID'] = str(NID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(PAYFUNCREMINDNEW_GETREMIND_LATEST_THEME_18233, data=data)

    def ticai_readercount_latest_theme(self, u=None, m=None, t=None, **overrides):
        """Replay session 18234: TiCai.ReaderCount."""
        data = dict(TICAI_READERCOUNT_LATEST_THEME_18234['data'])
        if u is not None:
            data['u'] = str(u)
        if m is not None:
            data['m'] = str(m)
        if t is not None:
            data['t'] = str(t)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(TICAI_READERCOUNT_LATEST_THEME_18234, data=data)

    def zhishul2data_getparentplatecode_windvane(self, StockID=None, **overrides):
        """Replay session 18235: ZhiShuL2Data.GetParentPlateCode."""
        data = dict(ZHISHUL2DATA_GETPARENTPLATECODE_WINDVANE_18235['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETPARENTPLATECODE_WINDVANE_18235, data=data)

    def zhishul2data_getvolturincremental_windvane(self, StockID=None, Day=None, **overrides):
        """Replay session 18236: ZhiShuL2Data.GetVolTurIncremental."""
        data = dict(ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_18236['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_18236, data=data)

    def zhishul2data_gettrendincremental_windvane(self, StockID=None, Day=None, **overrides):
        """Replay session 18237: ZhiShuL2Data.GetTrendIncremental."""
        data = dict(ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_18237['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_18237, data=data)

    def index_getarttitle_windvane(self, Type=None, StockID=None, **overrides):
        """Replay session 18238: Index.GetArtTitle."""
        data = dict(INDEX_GETARTTITLE_WINDVANE_18238['data'])
        if Type is not None:
            data['Type'] = str(Type)
        if StockID is not None:
            data['StockID'] = str(StockID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_GETARTTITLE_WINDVANE_18238, data=data)

    def zhishul2data_gettrendincremental_windvane_history(self, StockID=None, Day=None, **overrides):
        """Replay session 18239: ZhiShuL2Data.GetTrendIncremental."""
        data = dict(ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_HISTORY_18239['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETTRENDINCREMENTAL_WINDVANE_HISTORY_18239, data=data)

    def zhishuranking_getplate_info_qj_windvane_history(self, Date=None, PlateID=None, **overrides):
        """Replay session 18240: ZhiShuRanking.GetPlate_Info_QJ."""
        data = dict(ZHISHURANKING_GETPLATE_INFO_QJ_WINDVANE_HISTORY_18240['data'])
        if Date is not None:
            data['Date'] = str(Date)
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_GETPLATE_INFO_QJ_WINDVANE_HISTORY_18240, data=data)

    def zhishul2data_getvolturincremental_windvane_history(self, StockID=None, Day=None, **overrides):
        """Replay session 18241: ZhiShuL2Data.GetVolTurIncremental."""
        data = dict(ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_HISTORY_18241['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHUL2DATA_GETVOLTURINCREMENTAL_WINDVANE_HISTORY_18241, data=data)

    def zhishuranking_sonplate_info_windvane_history(self, PlateID=None, IsShow=None, Date=None, **overrides):
        """Replay session 18242: ZhiShuRanking.SonPlate_Info."""
        data = dict(ZHISHURANKING_SONPLATE_INFO_WINDVANE_HISTORY_18242['data'])
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if IsShow is not None:
            data['IsShow'] = str(IsShow)
        if Date is not None:
            data['Date'] = str(Date)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_SONPLATE_INFO_WINDVANE_HISTORY_18242, data=data)

    def zhishuranking_getgpcphbts_tag_windvane_history(self, PlateID=None, Date=None, **overrides):
        """Replay session 18243: ZhiShuRanking.GetGPCPHBTS_Tag."""
        data = dict(ZHISHURANKING_GETGPCPHBTS_TAG_WINDVANE_HISTORY_18243['data'])
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if Date is not None:
            data['Date'] = str(Date)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_GETGPCPHBTS_TAG_WINDVANE_HISTORY_18243, data=data)

    def hisconceptionpoint_bkfenshizhibo_windvane_history(self, PlateID=None, Date=None, **overrides):
        """Replay session 18244: HisConceptionPoint.BKFenShiZhiBo."""
        data = dict(HISCONCEPTIONPOINT_BKFENSHIZHIBO_WINDVANE_HISTORY_18244['data'])
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if Date is not None:
            data['Date'] = str(Date)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(HISCONCEPTIONPOINT_BKFENSHIZHIBO_WINDVANE_HISTORY_18244, data=data)

    def zhishuranking_zhishustocklist_w8_windvane_history(self, Order=None, TSZB=None, st=None, old=None, IsZZ=None, Index=None, Date=None, Type=None, IsKZZType=None, PlateID=None, TSZB_Type=None, filterType=None, **overrides):
        """Replay session 18245: ZhiShuRanking.ZhiShuStockList_W8."""
        data = dict(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_HISTORY_18245['data'])
        if Order is not None:
            data['Order'] = str(Order)
        if TSZB is not None:
            data['TSZB'] = str(TSZB)
        if st is not None:
            data['st'] = str(st)
        if old is not None:
            data['old'] = str(old)
        if IsZZ is not None:
            data['IsZZ'] = str(IsZZ)
        if Index is not None:
            data['Index'] = str(Index)
        if Date is not None:
            data['Date'] = str(Date)
        if Type is not None:
            data['Type'] = str(Type)
        if IsKZZType is not None:
            data['IsKZZType'] = str(IsKZZType)
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if TSZB_Type is not None:
            data['TSZB_Type'] = str(TSZB_Type)
        if filterType is not None:
            data['filterType'] = str(filterType)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_HISTORY_18245, data=data)

    def zhishuranking_zhishustocklist_w8_windvane_tszb72_history(self, Order=None, TSZB=None, st=None, SetLog=None, old=None, IsZZ=None, Index=None, Date=None, Type=None, Filed_Type=None, IsKZZType=None, PlateID=None, TSZB_Type=None, filterType=None, **overrides):
        """Replay session 18246: ZhiShuRanking.ZhiShuStockList_W8 (???-????????)."""
        data = dict(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB72_18246['data'])
        if Order is not None:
            data['Order'] = str(Order)
        if TSZB is not None:
            data['TSZB'] = str(TSZB)
        if st is not None:
            data['st'] = str(st)
        if SetLog is not None:
            data['SetLog'] = str(SetLog)
        if old is not None:
            data['old'] = str(old)
        if IsZZ is not None:
            data['IsZZ'] = str(IsZZ)
        if Index is not None:
            data['Index'] = str(Index)
        if Date is not None:
            data['Date'] = str(Date)
        if Type is not None:
            data['Type'] = str(Type)
        if Filed_Type is not None:
            data['Filed_Type'] = str(Filed_Type)
        if IsKZZType is not None:
            data['IsKZZType'] = str(IsKZZType)
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if TSZB_Type is not None:
            data['TSZB_Type'] = str(TSZB_Type)
        if filterType is not None:
            data['filterType'] = str(filterType)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB72_18246, data=data)

    def zhishuranking_zhishustocklist_w8_windvane_tszb73_history(self, Order=None, TSZB=None, st=None, SetLog=None, old=None, IsZZ=None, Index=None, Date=None, Type=None, Filed_Type=None, IsKZZType=None, PlateID=None, TSZB_Type=None, filterType=None, **overrides):
        """Replay session 18247: ZhiShuRanking.ZhiShuStockList_W8 (???-????????)."""
        data = dict(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB73_18247['data'])
        if Order is not None:
            data['Order'] = str(Order)
        if TSZB is not None:
            data['TSZB'] = str(TSZB)
        if st is not None:
            data['st'] = str(st)
        if SetLog is not None:
            data['SetLog'] = str(SetLog)
        if old is not None:
            data['old'] = str(old)
        if IsZZ is not None:
            data['IsZZ'] = str(IsZZ)
        if Index is not None:
            data['Index'] = str(Index)
        if Date is not None:
            data['Date'] = str(Date)
        if Type is not None:
            data['Type'] = str(Type)
        if Filed_Type is not None:
            data['Filed_Type'] = str(Filed_Type)
        if IsKZZType is not None:
            data['IsKZZType'] = str(IsKZZType)
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if TSZB_Type is not None:
            data['TSZB_Type'] = str(TSZB_Type)
        if filterType is not None:
            data['filterType'] = str(filterType)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB73_18247, data=data)

    def zhishuranking_zhishustocklist_w8_windvane_tszb74_history(self, Order=None, TSZB=None, st=None, SetLog=None, old=None, IsZZ=None, Index=None, Date=None, Type=None, Filed_Type=None, IsKZZType=None, PlateID=None, TSZB_Type=None, filterType=None, **overrides):
        """Replay session 18248: ZhiShuRanking.ZhiShuStockList_W8 (???-????????)."""
        data = dict(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB74_18248['data'])
        if Order is not None:
            data['Order'] = str(Order)
        if TSZB is not None:
            data['TSZB'] = str(TSZB)
        if st is not None:
            data['st'] = str(st)
        if SetLog is not None:
            data['SetLog'] = str(SetLog)
        if old is not None:
            data['old'] = str(old)
        if IsZZ is not None:
            data['IsZZ'] = str(IsZZ)
        if Index is not None:
            data['Index'] = str(Index)
        if Date is not None:
            data['Date'] = str(Date)
        if Type is not None:
            data['Type'] = str(Type)
        if Filed_Type is not None:
            data['Filed_Type'] = str(Filed_Type)
        if IsKZZType is not None:
            data['IsKZZType'] = str(IsKZZType)
        if PlateID is not None:
            data['PlateID'] = str(PlateID)
        if TSZB_Type is not None:
            data['TSZB_Type'] = str(TSZB_Type)
        if filterType is not None:
            data['filterType'] = str(filterType)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_ZHISHUSTOCKLIST_W8_WINDVANE_TSZB74_18248, data=data)


    def longhubang_getstocklist_today_board_18249(self, Index=None, Time=None, Type=None, st=None, **overrides):
        """Replay session 18249: LongHuBang.GetStockList."""
        data = dict(LONGHUBANG_GETSTOCKLIST_TODAY_BOARD_18249['data'])
        if Index is not None:
            data['Index'] = str(Index)
        if Time is not None:
            data['Time'] = str(Time)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETSTOCKLIST_TODAY_BOARD_18249, data=data)

    def longhubang_getagencylistv2_today_board_18250(self, Index=None, Time=None, st=None, **overrides):
        """Replay session 18250: LongHuBang.GetAgencyListV2."""
        data = dict(LONGHUBANG_GETAGENCYLISTV2_TODAY_BOARD_18250['data'])
        if Index is not None:
            data['Index'] = str(Index)
        if Time is not None:
            data['Time'] = str(Time)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETAGENCYLISTV2_TODAY_BOARD_18250, data=data)

    def longhubang_getagencykline_today_board_18251(self, index=None, st=None, **overrides):
        """Replay session 18251: LongHuBang.GetAgencyKline."""
        data = dict(LONGHUBANG_GETAGENCYKLINE_TODAY_BOARD_18251['data'])
        if index is not None:
            data['index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETAGENCYKLINE_TODAY_BOARD_18251, data=data)

    def longhubang_getbusinesslist_today_board_18252(self, Index=None, Time=None, Type=None, st=None, **overrides):
        """Replay session 18252: LongHuBang.GetBusinessList."""
        data = dict(LONGHUBANG_GETBUSINESSLIST_TODAY_BOARD_18252['data'])
        if Index is not None:
            data['Index'] = str(Index)
        if Time is not None:
            data['Time'] = str(Time)
        if Type is not None:
            data['Type'] = str(Type)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETBUSINESSLIST_TODAY_BOARD_18252, data=data)

    def longhubang_getagencydaylist_today_board_18253(self, SDay=None, EDay=None, **overrides):
        """Replay session 18253: LongHuBang.GetAgencyDayList."""
        data = dict(LONGHUBANG_GETAGENCYDAYLIST_TODAY_BOARD_18253['data'])
        if SDay is not None:
            data['SDay'] = str(SDay)
        if EDay is not None:
            data['EDay'] = str(EDay)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETAGENCYDAYLIST_TODAY_BOARD_18253, data=data)

    def businessgroup_groupinfo_youzi_group(self, GID=None, **overrides):
        """Replay session 18254: BusinessGroup.GroupInfo."""
        data = dict(BUSINESSGROUP_GROUPINFO_YOUZI_GROUP_18254['data'])
        if GID is not None:
            data['GID'] = str(GID)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(BUSINESSGROUP_GROUPINFO_YOUZI_GROUP_18254, data=data)

    def businessgroup_grouplog_youzi_group(self, GID=None, Day=None, SDay=None, Money=None, Order=None, Index=None, st=None, **overrides):
        """Replay session 18255: BusinessGroup.GroupLog."""
        data = dict(BUSINESSGROUP_GROUPLOG_YOUZI_GROUP_18255['data'])
        if GID is not None:
            data['GID'] = str(GID)
        if Day is not None:
            data['Day'] = str(Day)
        if SDay is not None:
            data['SDay'] = str(SDay)
        if Money is not None:
            data['Money'] = str(Money)
        if Order is not None:
            data['Order'] = str(Order)
        if Index is not None:
            data['Index'] = str(Index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(BUSINESSGROUP_GROUPLOG_YOUZI_GROUP_18255, data=data)

    def userbusiness_getofficev2_youzi_group(self, **overrides):
        """Replay session 18256: UserBusiness.GetOfficev2."""
        data = dict(USERBUSINESS_GETOFFICEV2_YOUZI_GROUP_18256['data'])
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERBUSINESS_GETOFFICEV2_YOUZI_GROUP_18256, data=data)

    def stock_getstockchart_youzi_group(self, StockID=None, index=None, st=None, **overrides):
        """Replay session 18257: Stock.GetStockChart."""
        data = dict(STOCK_GETSTOCKCHART_YOUZI_GROUP_18257['data'])
        if StockID is not None:
            data['StockID'] = str(StockID)
        if index is not None:
            data['index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETSTOCKCHART_YOUZI_GROUP_18257, data=data)

    def userbusiness_getday_top_youzi(self, Day=None, **overrides):
        """Replay session 18258: UserBusiness.GetDay."""
        data = dict(USERBUSINESS_GETDAY_TOP_YOUZI_18258['data'])
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERBUSINESS_GETDAY_TOP_YOUZI_18258, data=data)

    def stockl2history_getzstrend_narrow_history(self, Day=None, **overrides):
        """Replay session 18285: StockL2History.GetZsTrend_Narrow."""
        data = dict(STOCKL2HISTORY_GETZSTREND_NARROW_HISTORY_18285['data'])
        if Day is not None:
            data['Day'] = str(Day)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCKL2HISTORY_GETZSTREND_NARROW_HISTORY_18285, data=data)

    def zhishuranking_realrankinginfo_history(self, Date=None, Type=None, ZSType=None, RStart=None, REnd=None, Index=None, Order=None, st=None, **overrides):
        """Replay session 18286: ZhiShuRanking.RealRankingInfo."""
        data = dict(ZHISHURANKING_REALRANKINGINFO_HISTORY_18286['data'])
        if Date is not None:
            data['Date'] = str(Date)
        if Type is not None:
            data['Type'] = str(Type)
        if ZSType is not None:
            data['ZSType'] = str(ZSType)
        if RStart is not None:
            data['RStart'] = str(RStart)
        if REnd is not None:
            data['REnd'] = str(REnd)
        if Index is not None:
            data['Index'] = str(Index)
        if Order is not None:
            data['Order'] = str(Order)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(ZHISHURANKING_REALRANKINGINFO_HISTORY_18286, data=data)

if __name__ == '__main__':
    client = KaipanlaCapturedClient()
    response = client.index_newgetlist()
    print(response.status_code)
    print(response.text[:500])
