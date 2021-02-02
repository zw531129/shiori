import datetime
import json
import re

import aiohttp
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from arrow.arrow import Arrow

from .yobot_exceptions import InputError, ServerError

_calender_url = {
    "jp": "https://tools.yobot.win/calender/#jp",
    "tw": "https://pcredivewiki.tw/",
    "cn": "https://mahomaho-insight.info/",
}

_region_name = {"cn": "国服", "jp": "日服", "tw": "台服"}

class Event_timeline:
    def __init__(self):
        self._tineline = dict()

    def add_event(self, start_t: Arrow, end_t: Arrow, name):
        t = start_t
        while t <= end_t:
            daystr = t.format(fmt="YYYYMMDD", locale="zh_cn")
            if daystr not in self._tineline:
                self._tineline[daystr] = list()
            self._tineline[daystr].append(name)
            t += datetime.timedelta(days=1)

    def at(self, day: Arrow):
        daystr = day.format(fmt="YYYYMMDD", locale="zh_cn")
        return self._tineline.get(daystr, ())


class Event:
    Passive = True
    Active = True
    Request = False

    def __init__(self, glo_setting: dict, *args, **kwargs):
        self.setting = glo_setting

        # # 时区：东8区
        # self.timezone = datetime.timezone(datetime.timedelta(hours=8))

        # 。。。屁东8区，Arrow这个库解析的时候把时区略了，加东8区会有bug，导致每天早上8点前获取的calendar会延后一天
        self.timezone = datetime.timezone(datetime.timedelta(hours=0))

        self.timeline = None

        self.timeline_cn = None
        self.timeline_jp = None
        self.timeline_tw = None

    def load_timeline(self, rg):
        raise RuntimeError("no more sync calling")

    async def load_timeline_async(self, rg=None):
        if rg is None:
            rg = self.setting.get("calender_region", "default")
        if self.setting.get("calender_cn", False) or rg == "cn":
            self.timeline_cn = await self.load_timeline_cn_async()
            print("刷新国服日程表成功")
        if self.setting.get("calender_jp", False) or rg == "jp":
            self.timeline_jp = await self.load_timeline_jp_async()
            print("刷新日服日程表成功")
        if self.setting.get("calender_tw", False) or rg == "tw":
            self.timeline_tw = await self.load_timeline_tw_async()
            print("刷新台服日程表成功")

    # def load_time_jp(self, timestamp) -> Arrow:
    #     tz = datetime.timezone(datetime.timedelta(hours=8))
    #     d_time = datetime.datetime.fromtimestamp(timestamp, tz)
    #     a_time = Arrow.fromdatetime(d_time)
    #     if a_time.hour < 4:
    #         a_time -= datetime.timedelta(hours=4)
    #     return a_time

    # async def load_timeline_jp_async(self):
    #     event_source = "https://gamewith.jp/pricone-re/article/show/93857"
    #     try:
    #         async with aiohttp.request("GET", url=event_source) as response:
    #             if response.status != 200:
    #                 raise ServerError(f"服务器状态错误：{response.status}")
    #             res = await response.text()
    #     except aiohttp.client_exceptions.ClientError:
    #         print("日程表加载失败")
    #         return
    #     soup = BeautifulSoup(res, features="html.parser")
    #     events_ids = set()
    #     timeline = Event_timeline()
    #     for event in soup.select("[data-calendar]"):
    #         e = json.loads(event["data-calendar"])
    #         if e["id"] in events_ids:
    #             continue
    #         events_ids.add(e["id"])
    #         timeline.add_event(
    #             self.load_time_jp(e["start_time"]),
    #             self.load_time_jp(e["end_time"]),
    #             e["event_name"],
    #         )
    #     return timeline

    def load_time_jp(self, timestr) -> Arrow:
        d_time = datetime.datetime.strptime(timestr, r"%Y/%m/%d %H:%M:%S")
        a_time = Arrow.fromdatetime(d_time)
        if a_time.time() < datetime.time(hour=4):
            a_time -= datetime.timedelta(hours=4)
        return a_time

    async def load_timeline_jp_async(self):
        event_source = "http://toolscdn.yobot.win/calender/jp.json"
        async with aiohttp.request("GET", url=event_source) as response:
            if response.status != 200:
                raise ServerError(f"服务器状态错误：{response.status}")
            res = await response.text()
        events = json.loads(res)
        timeline = Event_timeline()
        for e in events:
            timeline.add_event(
                self.load_time_jp(e["start_time"]),
                self.load_time_jp(e["end_time"]),
                e["name"],
            )
        return timeline

    def load_time_tw(self, timestr) -> Arrow:
        d_time = datetime.datetime.strptime(timestr, r"%Y/%m/%d %H:%M")
        a_time = Arrow.fromdatetime(d_time)
        if a_time.time() < datetime.time(hour=5):
            a_time -= datetime.timedelta(hours=5)
        return a_time

    async def load_timeline_tw_async(self):
        event_source = "https://pcredivewiki.tw/static/data/event.json"
        async with aiohttp.request("GET", url=event_source) as response:
            if response.status != 200:
                raise ServerError(f"服务器状态错误：{response.status}")
            res = await response.text()
        events = json.loads(res)
        timeline = Event_timeline()
        for e in events:
            timeline.add_event(
                self.load_time_tw(e["start_time"]),
                self.load_time_tw(e["end_time"]),
                e["campaign_name"],
            )
        return timeline

    def load_time_cn(self, timestamp) -> Arrow:
        d_time = datetime.datetime.strptime(timestamp, r"%Y/%m/%d %H:%M") #mahomaho
        #d_time = datetime.datetime.fromtimestamp(timestamp) #bigfun
        a_time = Arrow.fromdatetime(d_time)
        if a_time.time() < datetime.time(hour=5):
            a_time -= datetime.timedelta(hours=5)
        return a_time
    
    async def load_timeline_cn_async(self):
        event_source = "https://mahomaho-insight.info/cached/gameevents.json"
        async with aiohttp.request("GET", url=event_source) as response:
            if response.status != 200:
                raise ServerError(f"服务器状态错误：{response.status}")
            res = await response.text()
        events = json.loads(res)["cn"]
        timeline = Event_timeline()
        for e in events:
            timeline.add_event(
                self.load_time_cn(e["start"]),
                self.load_time_cn(e["end"]),
                e["title"],
            )
        return timeline

    def get_day_events(self, match_num, region) -> tuple:
        if match_num == 2:
            daystr = "今天"
            date = Arrow.now(tzinfo=self.timezone)
        elif match_num == 3:
            daystr = "明天"
            date = Arrow.now(tzinfo=self.timezone) + datetime.timedelta(days=1)
        elif match_num & 0xf00000 == 0x100000:
            year = (match_num & 0xff000) >> 12
            month = (match_num & 0xf00) >> 8
            day = match_num & 0xff
            daystr = "{}年{}月{}日".format(2000+year, month, day)
            try:
                date = Arrow(2000+year, month, day)
            except ValueError as v:
                raise InputError("日期错误：{}".format(v))

        timeline = self.timeline_cn
        if region == "jp":
            timeline = self.timeline_jp
        elif region == "tw":
            timeline = self.timeline_tw
        if not timeline:
            events = None
        else:
            events = timeline.at(date)

        return (daystr, events)

    def get_week_events(self) -> str:
        tl = self.timeline_cn
        rg = self.setting.get("calender_region", "default")
        if rg == "jp":
            tl = self.timeline_jp
        elif rg == "tw":
            tl = self.timeline_tw
        if tl is None:
            reply = "日程表未初始化\n\n更多日程：{}".format(_calender_url.get(self.setting["calender_region"]))
            return reply
        reply = "一周日程："
        date = Arrow.now(tzinfo=self.timezone)
        for i in range(7):
            events = tl.at(date)
            events_str = "\n⨠".join(events)
            if events_str == "":
                events_str = "没有记录"
            daystr = date.format("MM月DD日")
            reply += "\n======{}======\n⨠{}".format(daystr, events_str)
            date += datetime.timedelta(days=1)
        reply += "\n\n更多日程：{}".format(
            _calender_url.get(self.setting["calender_region"]))
        return reply

    @staticmethod
    def match(cmd: str) -> int:
        if not cmd.startswith("日程"):
            return 0
        if cmd == "日程" or cmd == "日程今日" or cmd == "日程今天":
            return 2
        if cmd == "日程明日" or cmd == "日程明天":
            return 3
        if cmd == "日程表" or cmd == "日程一周" or cmd == "日程本周":
            return 4
        match = re.match(r"日程 ?(\d{1,2})月(\d{1,2})[日号]", cmd)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            return (0x114000 + 0x100*month + day)
        match = re.match(r"日程 ?(?:20)?(\d{2})年(\d{1,2})月(\d{1,2})[日号]", cmd)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return (0x100000 + 0x1000*year + 0x100*month + day)
        return 1
    
    def get_day_events_reply(self, match_num: int) -> str:
        reply = ""
        for k in ("cn", "jp", "tw"):
            rg =  self.setting.get("calender_" + k, False)
            if not rg:
                continue
            try:
                daystr, events = self.get_day_events(match_num, k)
            except InputError as e:
                continue
            if events == None:
                events_str = "未初始化"
            else:
                events_str = "\n".join(events)
                if events_str == "":
                    events_str = "没有记录"
            reply += "{}{}活动：\n{}".format(daystr, _region_name[k], events_str)
            reply += "\n\n"
        reply = reply.rstrip()
        return reply

    def execute(self, match_num: int, msg: dict) -> dict:
        if match_num == 1:
            return {"reply": "", "block": True}
        # self.check_and_update()
        elif match_num == 4:
            reply = self.get_week_events()
            return {"reply": reply, "block": True}
        else:
            reply = self.get_day_events_reply(match_num)
            return {"reply": reply, "block": True}

    async def send_daily_async(self):
        print("正在刷新日程表")
        try:
            await self.load_timeline_async()
        except Exception as e:
            print("刷新日程表失败，失败原因："+str(e))
        if not self.setting['calender_on']:
            return
        sub_groups = self.setting.get("notify_groups", [])
        sub_users = self.setting.get("notify_privates", [])
        if not (sub_groups or sub_users):
            return

        msg = self.get_day_events_reply(2)

        sends = []
        for group in sub_groups:
            sends.append({
                "message_type": "group",
                "group_id": group,
                "message": msg
            })
        for userid in sub_users:
            sends.append({
                "message_type": "private",
                "user_id": userid,
                "message": msg
            })
        return sends

    async def send_tomorrow_async(self):
        print("正在刷新日程表")
        try:
            await self.load_timeline_async()
        except Exception as e:
            print("刷新日程表失败，失败原因："+str(e))
        if not self.setting['calender_tomorrow_on']:
            return
        sub_groups = self.setting.get("notify_groups", [])
        sub_users = self.setting.get("notify_privates", [])
        if not (sub_groups or sub_users):
            return

        msg = self.get_day_events_reply(3)

        sends = []
        for group in sub_groups:
            sends.append({
                "message_type": "group",
                "group_id": group,
                "message": msg
            })
        for userid in sub_users:
            sends.append({
                "message_type": "private",
                "user_id": userid,
                "message": msg
            })
        return sends

    def jobs(self):
        time = self.setting.get("calender_time", "08:00")
        hour, minute = time.split(":")
        trigger = CronTrigger(hour=hour, minute=minute)
        job = (trigger, self.send_daily_async)
        init_trigger = DateTrigger(
            datetime.datetime.now() +
            datetime.timedelta(seconds=5)
        )  # 启动5秒后初始化
        init_job = (init_trigger, self.load_timeline_async)

        time = self.setting.get("calender_tomorrow_time", "20:00")
        hour, minute = time.split(":")
        job_tomorrow = (CronTrigger(hour=hour, minute=minute), self.send_tomorrow_async)
        return (job, init_job, job_tomorrow)
