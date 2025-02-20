import logging
import os
import json
from .holiday import Holiday
from .hot_handler.v2ex_hot_handler import V2exHotHandler
from .hot_handler.nga_qfx_hot_handler import NGAQFXHotHandler
from astrbot.api.all import Context, AstrMessageEvent, CommandResult
from astrbot.api.message_components import Node, Plain, Image
import apscheduler
import apscheduler.schedulers
import apscheduler.schedulers.asyncio
import asyncio


class AstrbotPluginMofish:
    def __init__(self, context: Context) -> None:
        self.NAMESPACE = "astrbot_plugin_mofish"
        self.context = context
        self.logger = logging.getLogger("astrbot")
        self.context.register_commands(self.NAMESPACE, "mofish", "每日摸鱼", 1, self.mofish)
        # 节假日
        self.holiday = Holiday()
        # v2ex热榜
        self.v2ex = V2exHotHandler()
        # NGA晴风村热帖
        self.ngq_qfc = NGAQFXHotHandler()

        self.scheduler = apscheduler.schedulers.asyncio.AsyncIOScheduler()

        # 加载订阅了每日摸鱼的会话号
        self.config_data_file = f"data/{self.NAMESPACE}_data.json"
        if not os.path.exists(self.config_data_file):
            with open(self.config_data_file, "w") as f:
                json.dump({}, f)
        with open(self.config_data_file, "r") as f:
            self.data = json.load(f)
        self.auto_daily_mofish_ids = self.data.get("auto_daily_mofish_ids", [])

        if self.auto_daily_mofish_ids:
            self._start_cron_if_not()

    async def mofish(self, event: AstrMessageEvent, context: Context):
        args = event.message_str.split(" ")
        help_msg = '\n\n'.join(['每日摸鱼 指令描述',
                                '/mofish today 今日信息',
                                '/mofish hot_nga NGA晴风村',
                                '/mofish hot_v2ex v2ex',
                                # '/mofish 喜加一 EPIC 喜加一'
                                # '/mofish hot_all 所有鱼塘热榜'
                                '/mofish auto 启动/关闭每日 9 点发送摸鱼信息'
                                ])
        if len(args) < 2:
            return CommandResult().message(help_msg)
        if args[1] == "today":
            return self.today_info_desc(event, context)
        if args[1] == "hot_nga":
            return await self.send_nga_hot(event, context)
        if args[1] == "hot_v2ex":
            return await self.send_v2ex_hot(event, context)
        if args[1] == "auto":
            return await self.auto_daily_problem(event, context)
        if args[1] == "test":
            await self.test(event, context)
            return CommandResult().message("test~")
        if args[1] == "help":
            return CommandResult().message(help_msg)
        return CommandResult().message("指令错误喵~")

    def today_info_desc(self, event: AstrMessageEvent, context: Context):
        return CommandResult().message('\n'.join(self.holiday.getTodayDesc()))

    async def send_nga_hot(self, event: AstrMessageEvent, context: Context):
        hot_arr = await self.ngq_qfc.get_hot()
        content = []
        for hot in hot_arr:
            content.append(Plain(hot + "\n\n"))
        return CommandResult(chain=[Node(
            uin=905617992,
            name="Soulter",
            content=content
        )])

    async def test(self, event: AstrMessageEvent, context: Context):
        message_arr = await self.ngq_qfc.get_hot()
        await self._send_forward_msg(event, context, message_arr, "NGA晴风村热帖")
        return None

    async def send_v2ex_hot(self, event: AstrMessageEvent, context: Context):
        hot_arr = await self.v2ex.get_hot()
        content = []
        for hot in hot_arr:
            content.append(Plain(hot + "\n\n"))
        return CommandResult(chain=[Node(
            uin=905617992,
            name="Soulter",
            content=content
        )])

    async def _send_daily_mofish(self):
        self.logger.info(f"正在推送每日摸鱼信息给 {len(self.auto_daily_mofish_ids)} 个会话...")
        # 今日信息
        today_desc_arr = self.holiday.getTodayDesc()
        # 鱼塘热榜
        # v2ex_hot_arr = await self.v2ex.get_hot()
        # ngq_qfc_hot_arr = await self.ngq_qfc.get_hot()
        for session_id in self.auto_daily_mofish_ids:
            await self.context.send_message(session_id, CommandResult().message('\n'.join(today_desc_arr)))
            await asyncio.sleep(1)

    # 启动每日摸鱼定时任务
    def _start_cron_if_not(self):
        if not self.scheduler.get_jobs():
            self.scheduler.add_job(self._send_daily_mofish, "cron", hour=9, minute=0)
            self.scheduler.start()

    async def auto_daily_problem(self, event: AstrMessageEvent, context: Context):
        # 启动/关闭每日 9 点发送摸鱼信息
        umo_id = event.unified_msg_origin
        opened = False
        if umo_id in self.auto_daily_mofish_ids:
            self.auto_daily_mofish_ids.remove(umo_id)
        else:
            self.auto_daily_mofish_ids.append(umo_id)
            opened = True

        self.data["auto_daily_mofish_ids"] = self.auto_daily_mofish_ids
        with open(self.config_data_file, "w") as f:
            json.dump(self.data, f)

        self._start_cron_if_not()

        if opened:
            return CommandResult().message(f"已对 {umo_id} 开启每日摸鱼")
        return CommandResult().message(f"已对 {umo_id} 关闭每日摸鱼")

    # 发送多条转发消息
    async def _send_forward_msg(self, event: AstrMessageEvent, message_arr: list[str], source: str):
        if event.get_platform_name() == "aiocqhttp":
            # qq
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot  # 得到 client
            messages = []
            for message_str in message_arr:
                message = {
                    "type": "node",
                    "data": {
                        "user_id": 905617992,
                        "nickname": "Soulter",
                        "content": [{
                            "type": "text",
                            "data": {
                                "text": message_str
                            },
                        }]
                    }
                }
                messages.append(message)
            payloads = {
                "group_id": event.get_group_id(),
                "user_id": event.get_sender_id(),
                "messages": messages,
                "source": source
            }
            # 调用 协议端  API
            ret = await client.api.call_action('send_forward_msg', **payloads)
            self.logger.info(f"send_forward_msg: {ret}")