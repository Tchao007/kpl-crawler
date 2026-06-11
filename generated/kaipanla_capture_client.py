# -*- coding: utf-8 -*-
"""
Python request client generated from test.saz.

It keeps only business requests for applhb.longhuvip.com and drops duplicate
polling calls found in the capture. Each method returns requests.Response;
call response.json() or response.text to inspect the response body.
"""

from __future__ import annotations

import requests


DEFAULT_TIMEOUT = 15


INDEX_NEWGETLIST = {
    'session_id': '15',
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
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

SYSAPPVERSION_GETLAYOUT = {
    'session_id': '16',
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
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

USERINFO_APPNEWS = {
    'session_id': '17',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "AppNews",
        "st": "1",
        "c": "UserInfo",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
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
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

SYSTEM_MODULESWITCH = {
    'session_id': '23',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ModuleSwitch",
        "c": "System",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

THEME_INFOGR = {
    'session_id': '27',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "InfoGR",
        "c": "Theme",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

SYSTEM_ADGET = {
    'session_id': '28',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "AdGet",
        "c": "System",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Scale": "0.5625",
        "apiv": "w44",
        "Type": "1"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

SYSTEM_WEBJSGET = {
    'session_id': '37',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "WebJsGet",
        "apiv": "w44",
        "c": "System",
        "PhoneOSNew": "1",
        "UserID": "0",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

PUSH_ACTIVEPUSHMESSAGEALL = {
    'session_id': '40',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "ActivePushMessageAll",
        "c": "Push",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

PUSH_GETNEWPUSHMESSAGEALL = {
    'session_id': '41',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetNewPushMessageAll",
        "c": "Push",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

SYSTEM_FOCUSFUNGET = {
    'session_id': '42',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "FocusFunGet",
        "apiv": "w44",
        "c": "System",
        "PhoneOSNew": "1",
        "FWebID": "1",
        "UserID": "0",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANGDONGCAI_GETSTATE = {
    'session_id': '47',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetState",
        "apiv": "w44",
        "c": "LongHuBangDongCai",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANG_TOPTITLE = {
    'session_id': '48',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "TopTitle",
        "apiv": "w44",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANG_GETSTOCKLIST = {
    'session_id': '50',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "st": "500",
        "a": "GetStockList",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
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
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANG_ADD = {
    'session_id': '51',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "Add",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Time": "2026-06-11",
        "apiv": "w44",
        "StockID": "603616"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

STOCK_GETNEWONESTOCKINFO = {
    'session_id': '52',
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
        "Time": "2026-06-11",
        "StockID": "603616",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

STOCK_GETSTOCKCHART = {
    'session_id': '53',
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
        "StockID": "603616",
        "Index": "0",
        "st": "530",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

COMMENTS_GET = {
    'session_id': '62',
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
        "StockID": "603616",
        "Day": "2026-06-11",
        "Type": "1",
        "Tsort": "0",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232"
    },
    'headers': {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.23.0.4",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://apppage.longhuvip.com",
        "X-Requested-With": "com.aiyu.kaipanla",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://apppage.longhuvip.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANG_GETAGENCYLISTV2 = {
    'session_id': '77',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetAgencyListV2",
        "st": "500",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Time": "2026-06-11",
        "Index": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANG_GETAGENCYKLINE = {
    'session_id': '78',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetAgencyKline",
        "st": "499",
        "apiv": "w44",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "index": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

LONGHUBANG_GETBUSINESSLIST = {
    'session_id': '79',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "GetBusinessList",
        "st": "100",
        "c": "LongHuBang",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "Time": "2026-06-11",
        "Index": "0",
        "apiv": "w44",
        "Type": "1",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

SYSTEM_ADGETKHD = {
    'session_id': '80',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "AdGetKHD",
        "apiv": "w44",
        "Type": "8,11",
        "c": "System",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Scale": "0.5625"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

USERXINSHOUZHIYIN_XSZYSTATE = {
    'session_id': '93',
    'method': 'GET',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {
        "a": "XSZYState",
        "c": "UserXinShouZhiYin",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "Token": "0",
        "apiv": "w44",
        "UserID": "0"
    },
    'data': {},
    'headers': {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}

PUSH_DEVICETOKEN = {
    'session_id': '94',
    'method': 'POST',
    'url': 'https://applhb.longhuvip.com/w1/api/index.php',
    'params': {},
    'data': {
        "a": "DeviceToken",
        "c": "Push",
        "PhoneOSNew": "1",
        "DeviceID": "3db60e69-5e48-349e-b8a9-59fb164e3232",
        "VerSion": "5.23.0.4",
        "PhoneOS": "2",
        "Token": "0",
        "apiv": "w44",
        "TokenType": "3",
        "Version": "5.23.0.4",
        "DeviceToken": "c5a3d9d1397b4fbf009d6004d77aee5c",
        "UserID": "0"
    },
    'headers': {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-N976N Build/QP1A.190711.020)"
    },
    'status_line': 'HTTP/1.1 200 OK',
}


REQUESTS = [
    INDEX_NEWGETLIST,
    SYSAPPVERSION_GETLAYOUT,
    USERINFO_APPNEWS,
    SYSTEM_MODULESWITCH,
    THEME_INFOGR,
    SYSTEM_ADGET,
    SYSTEM_WEBJSGET,
    PUSH_ACTIVEPUSHMESSAGEALL,
    PUSH_GETNEWPUSHMESSAGEALL,
    SYSTEM_FOCUSFUNGET,
    LONGHUBANGDONGCAI_GETSTATE,
    LONGHUBANG_TOPTITLE,
    LONGHUBANG_GETSTOCKLIST,
    LONGHUBANG_ADD,
    STOCK_GETNEWONESTOCKINFO,
    STOCK_GETSTOCKCHART,
    COMMENTS_GET,
    LONGHUBANG_GETAGENCYLISTV2,
    LONGHUBANG_GETAGENCYKLINE,
    LONGHUBANG_GETBUSINESSLIST,
    SYSTEM_ADGETKHD,
    USERXINSHOUZHIYIN_XSZYSTATE,
    PUSH_DEVICETOKEN
]


class KaipanlaCapturedClient:
    def __init__(self, timeout=DEFAULT_TIMEOUT, session=None):
        self.timeout = timeout
        self.session = session or requests.Session()

    def request(self, spec, data=None, params=None, headers=None):
        merged_params = dict(spec.get('params') or {})
        if params:
            merged_params.update({key: str(value) for key, value in params.items() if value is not None})

        merged_headers = dict(spec.get('headers') or {})
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

    def index_newgetlist(self, **overrides):
        """Replay session 15: Index.NewGetList."""
        data = dict(INDEX_NEWGETLIST['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(INDEX_NEWGETLIST, data=data)

    def sysappversion_getlayout(self, **overrides):
        """Replay session 16: SysAppVersion.GetLaYout."""
        data = dict(SYSAPPVERSION_GETLAYOUT['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSAPPVERSION_GETLAYOUT, data=data)

    def userinfo_appnews(self, st=None, index=None, **overrides):
        """Replay session 17: UserInfo.AppNews."""
        data = dict(USERINFO_APPNEWS['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERINFO_APPNEWS, data=data)

    def system_moduleswitch(self, **overrides):
        """Replay session 23: System.ModuleSwitch."""
        data = dict(SYSTEM_MODULESWITCH['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_MODULESWITCH, data=data)

    def theme_infogr(self, **overrides):
        """Replay session 27: Theme.InfoGR."""
        data = dict(THEME_INFOGR['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(THEME_INFOGR, data=data)

    def system_adget(self, type=None, **overrides):
        """Replay session 28: System.AdGet."""
        data = dict(SYSTEM_ADGET['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_ADGET, data=data)

    def system_webjsget(self, **overrides):
        """Replay session 37: System.WebJsGet."""
        data = dict(SYSTEM_WEBJSGET['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_WEBJSGET, data=data)

    def push_activepushmessageall(self, **overrides):
        """Replay session 40: Push.ActivePushMessageAll."""
        data = dict(PUSH_ACTIVEPUSHMESSAGEALL['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(PUSH_ACTIVEPUSHMESSAGEALL, data=data)

    def push_getnewpushmessageall(self, **overrides):
        """Replay session 41: Push.GetNewPushMessageAll."""
        data = dict(PUSH_GETNEWPUSHMESSAGEALL['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(PUSH_GETNEWPUSHMESSAGEALL, data=data)

    def system_focusfunget(self, fwebid=None, **overrides):
        """Replay session 42: System.FocusFunGet."""
        data = dict(SYSTEM_FOCUSFUNGET['data'])
        if fwebid is not None:
            data['FWebID'] = str(fwebid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_FOCUSFUNGET, data=data)

    def longhubangdongcai_getstate(self, **overrides):
        """Replay session 47: LongHuBangDongCai.GetState."""
        data = dict(LONGHUBANGDONGCAI_GETSTATE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANGDONGCAI_GETSTATE, data=data)

    def longhubang_toptitle(self, **overrides):
        """Replay session 48: LongHuBang.TopTitle."""
        data = dict(LONGHUBANG_TOPTITLE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_TOPTITLE, data=data)

    def longhubang_getstocklist(self, st=None, time=None, index=None, type=None, **overrides):
        """Replay session 50: LongHuBang.GetStockList."""
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
        """Replay session 51: LongHuBang.Add."""
        data = dict(LONGHUBANG_ADD['data'])
        if time is not None:
            data['Time'] = str(time)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_ADD, data=data)

    def stock_getnewonestockinfo(self, type=None, time=None, stockid=None, **overrides):
        """Replay session 52: Stock.GetNewOneStockInfo."""
        data = dict(STOCK_GETNEWONESTOCKINFO['data'])
        if type is not None:
            data['Type'] = str(type)
        if time is not None:
            data['Time'] = str(time)
        if stockid is not None:
            data['StockID'] = str(stockid)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETNEWONESTOCKINFO, data=data)

    def stock_getstockchart(self, stockid=None, index=None, st=None, **overrides):
        """Replay session 53: Stock.GetStockChart."""
        data = dict(STOCK_GETSTOCKCHART['data'])
        if stockid is not None:
            data['StockID'] = str(stockid)
        if index is not None:
            data['Index'] = str(index)
        if st is not None:
            data['st'] = str(st)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(STOCK_GETSTOCKCHART, data=data)

    def comments_get(self, index=None, st=None, stockid=None, day=None, type=None, tsort=None, **overrides):
        """Replay session 62: Comments.Get."""
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

    def longhubang_getagencylistv2(self, st=None, time=None, index=None, **overrides):
        """Replay session 77: LongHuBang.GetAgencyListV2."""
        data = dict(LONGHUBANG_GETAGENCYLISTV2['data'])
        if st is not None:
            data['st'] = str(st)
        if time is not None:
            data['Time'] = str(time)
        if index is not None:
            data['Index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETAGENCYLISTV2, data=data)

    def longhubang_getagencykline(self, st=None, index=None, **overrides):
        """Replay session 78: LongHuBang.GetAgencyKline."""
        data = dict(LONGHUBANG_GETAGENCYKLINE['data'])
        if st is not None:
            data['st'] = str(st)
        if index is not None:
            data['index'] = str(index)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETAGENCYKLINE, data=data)

    def longhubang_getbusinesslist(self, st=None, time=None, index=None, type=None, **overrides):
        """Replay session 79: LongHuBang.GetBusinessList."""
        data = dict(LONGHUBANG_GETBUSINESSLIST['data'])
        if st is not None:
            data['st'] = str(st)
        if time is not None:
            data['Time'] = str(time)
        if index is not None:
            data['Index'] = str(index)
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(LONGHUBANG_GETBUSINESSLIST, data=data)

    def system_adgetkhd(self, type=None, **overrides):
        """Replay session 80: System.AdGetKHD."""
        data = dict(SYSTEM_ADGETKHD['data'])
        if type is not None:
            data['Type'] = str(type)
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(SYSTEM_ADGETKHD, data=data)

    def userxinshouzhiyin_xszystate(self, **overrides):
        """Replay session 93: UserXinShouZhiYin.XSZYState."""
        data = dict(USERXINSHOUZHIYIN_XSZYSTATE['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(USERXINSHOUZHIYIN_XSZYSTATE, data=data)

    def push_devicetoken(self, **overrides):
        """Replay session 94: Push.DeviceToken."""
        data = dict(PUSH_DEVICETOKEN['data'])
        pass
        data.update({key: str(value) for key, value in overrides.items() if value is not None})
        return self.request(PUSH_DEVICETOKEN, data=data)


if __name__ == '__main__':
    client = KaipanlaCapturedClient()
    response = client.index_newgetlist()
    print(response.status_code)
    print(response.text[:500])
