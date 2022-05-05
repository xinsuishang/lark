#!/usr/bin/env python3
# coding=utf-8
import requests
import datetime

from settings_lark import LARK_CALENDAR_V4_URI, USER_ID
from lark_common import get_lark_header

calendar_id = ""


def time_format(cur_time):
    cur_time = cur_time.replace("T", " ")
    if len(cur_time) > 19:
        cur_time = cur_time[:19]

    # create 和 edit 是 0 时区的，其它自行设置了时区，所以需要做转换
    if len(cur_time) == 10:
        return int(datetime.datetime.strptime(cur_time, "%Y-%m-%d").timestamp()) + 3600 * 8 + 3600 * 12
    if len(cur_time) == 16:
        return int(datetime.datetime.strptime(cur_time, "%Y-%m-%d %H:%M").timestamp()) + 3600 * 8
    if len(cur_time) == 19:
        return int(datetime.datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S").timestamp())


def build_lark_data(summary, description, start_time, end_time):
    return {
        "summary": summary,
        "description": description,
        "start_time": {
            "timestamp": str(time_format(start_time))
        },
        "end_time": {
            "timestamp": str(time_format(start_time) + 3600 if end_time is None else time_format(end_time))
        },
        "need_notification": False,
        "visibility": "public"
    }


def get_calendar_id():
    """
    飞书获取主日历：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/calendar-v4/calendar/primary
    """
    global calendar_id
    if calendar_id:
        return calendar_id
    url = f"{LARK_CALENDAR_V4_URI}/primary"
    header = get_lark_header()
    resp = requests.post(url, headers=header, json={
    }).json()
    print(resp)
    calendar_id = resp.get("data").get("calendars")[0].get("calendar").get("calendar_id")
    print(f"获取主日历成功: {calendar_id}")
    return calendar_id


def search_calendar_events(description):
    """
    飞书日程搜索：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/calendar-v4/calendar-event/search
    不可用，需要通过用户回调获取 user_access_token
    """
    url = f"{LARK_CALENDAR_V4_URI}/{get_calendar_id()}/events/search"
    header = get_lark_header()
    data = {"query": description}
    resp = requests.post(url, headers=header, json=data).json()
    print("日程搜索结果：")
    print(resp)
    if len(resp["data"]) > 0:
        return resp["data"]["items"][0]["event_id"]


def create_calendar_events(summary, description, start_time, end_time):
    """
    飞书日程创建：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/calendar-v4/calendar-event/create
    """
    print("创建日程入参：")
    print(summary, description, start_time, end_time)
    #   search_event_id = search_calendar_events(description)
    #   if search_event_id:
    #       print("日程已存在：" + search_event_id)
    #       patch_calendar_events(summary, description, start_time, end_time, search_event_id)
    #       return search_event_id

    url = f"{LARK_CALENDAR_V4_URI}/{get_calendar_id()}/events"
    header = get_lark_header()
    data = build_lark_data(summary, description, start_time, end_time)
    print("创建日程参数：")
    print(data)
    resp = requests.post(url, headers=header, json=data).json()
    print("创建日程结果：")
    print(resp)
    lark_event_id = resp["data"]["event"]["event_id"]
    attendees(lark_event_id)
    return lark_event_id


def attendees(event_id):
    """
    邀请加入日程：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/calendar-v4/calendar-event-attendee/create
    """
    url = f"{LARK_CALENDAR_V4_URI}/{get_calendar_id()}/events/{event_id}/attendees?user_id_type=user_id"
    header = get_lark_header()
    data = {"attendees": [{"type": "user", "user_id": USER_ID, "is_optional": True}]}
    resp = requests.post(url, headers=header, json=data)
    print("邀请加入日程：")
    print(resp.json())


def patch_calendar_events(summary, description, start_time, end_time, event_id):
    """
    飞书日程更新：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/calendar-v4/calendar-event/patch
    """

    url = f"{LARK_CALENDAR_V4_URI}/{get_calendar_id()}/events/{event_id}"
    header = get_lark_header()
    data = build_lark_data(summary, description, start_time, end_time)
    resp = requests.patch(url, headers=header, json=data).json()
    print("日程更新：")
    print(resp)


if __name__ == '__main__':
    get_calendar_id()
