#!/usr/bin/env python3
# coding=utf-8

# 飞书开发者后台：https://open.feishu.cn/app?lang=zh-CN
LARK_APP_ID = ""
LARK_APP_SECRET = ""

LARK_URI = "https://open.feishu.cn/open-apis"
LARK_CALENDAR_V4_URI = f"{LARK_URI}/calendar/v4/calendars"

LARK_HEADERS = {
    "Authorization": "Bearer ",
    "content-type": "application/json;charset=utf-8",
}

# 飞书的用户唯一 id
USER_ID = ""