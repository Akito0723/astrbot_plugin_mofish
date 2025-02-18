import logging
from .holiday import Holiday
from .hot_handler.v2ex_hot_handler import V2exHotHandler
from .hot_handler.nga_qfx_hot_handler import NGAQFXHotHandler
from astrbot.api.all import Context, AstrMessageEvent, CommandResult
from astrbot.api.message_components import Node, Plain


class Main:
    def __init__(self, context: Context) -> None:
        self.NAMESPACE = "astrbot_plugin_mofish"
        self.context = context
        self.logger = logging.getLogger("astrbot")
        self.context.register_commands(self.NAMESPACE, "mofish", "每日摸鱼", 1, self.mofish)
        self.holiday_process = Holiday()
        self.v2ex = V2exHotHandler()
        self.ngq_qfc = NGAQFXHotHandler()

    async def mofish(self, event: AstrMessageEvent, context: Context):
        args = event.message_str.split(" ")
        help_msg = '\n\n'.join(['每日摸鱼 指令描述',
                                '/mofish today 今日信息',
                                '/mofish hot_nga NGA晴风村',
                                '/mofish hot_v2ex v2ex',
                                # '/mofish 喜加一 EPIC 喜加一'
                                # '/mofish hot_all 所有鱼塘热榜'
                                # '/mofish auto 启动/关闭每日 9 点发送摸鱼信息(锐意开发中)'
                                ])
        self.logger.info(args)
        if len(args) < 2:
            yield event.plain_result("指令错误喵~")
            return
        if args[1] == "today":
            self.today_info_desc(event)
            return
        if args[1] == "hot_nga":
            self.send_nga_hot(event)
            return
        if args[1] == "hot_v2ex":
            self.send_v2ex_hot(event)
            return
        if args[1] == "help":
            CommandResult().message(help_msg).use_t2i(False)
            return
        yield event.plain_result("指令错误喵~")

    def today_info_desc(self, event: AstrMessageEvent):
        yield event.plain_result('\n'.join(self.holiday_process.getTodayDesc()))

    async def send_nga_hot(self, event: AstrMessageEvent):
        hot_arr = self.ngq_qfc.get_hot()
        content = []
        for hot in hot_arr:
            content.append(Plain(hot))
        node = Node(
            uin=907999195,
            name="诶嘿bot",
            content=content
        )
        yield event.chain_result([node])

    async def send_v2ex_hot(self, event: AstrMessageEvent):
        hot_arr = self.v2ex.get_hot()
        content = []
        for hot in hot_arr:
            content.append(Plain(hot))
        node = Node(
            uin=907999195,
            name="诶嘿bot",
            content=content
        )
        yield event.chain_result([node])
