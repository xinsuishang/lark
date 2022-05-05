#!/usr/bin/env python3
# coding=utf-8

import time
import requests

from settings_lark import LARK_HEADERS, LARK_URI, LARK_APP_ID, LARK_APP_SECRET
"""
飞书 token 获取
"""
expire = 0
app_access_token = ""


def get_lark_header():
    now = time.time()

    global app_access_token
    global expire

    if now > expire:
        url = f"{LARK_URI}/auth/v3/app_access_token/internal"
        header = {
            "content-type": "application/json;charset=utf-8",
        }
        resp = requests.post(url, headers=header, json={
            "app_id": LARK_APP_ID,
            "app_secret": LARK_APP_SECRET,
        }).json()
        print(resp)
        app_access_token = resp["app_access_token"]
        expire = resp["expire"] + now - 100
        print(f"{app_access_token} expire at {expire}")
        LARK_HEADERS["Authorization"] = LARK_HEADERS["Authorization"] + app_access_token
        return LARK_HEADERS
    else:
        return LARK_HEADERS