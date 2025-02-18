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
        if len(args) < 2:
            return CommandResult().message(help_msg)
        if args[1] == "today":
            return self.today_info_desc(event, context)
        if args[1] == "nga":
            return await self.send_nga_hot(event, context)
        if args[1] == "help":
            return CommandResult().message(help_msg)
        return CommandResult().message("指令错误喵~")

    def today_info_desc(self, event: AstrMessageEvent, context: Context):
        return CommandResult().message('\n'.join(self.holiday_process.getTodayDesc()))

    async def send_nga_hot(self, event: AstrMessageEvent, context: Context):
        self.logger.info("send_nga_hot")
        hot_arr = await self.ngq_qfc.get_hot()
        self.logger.info(hot_arr)
        content = []
        for hot in hot_arr:
            content.append(Plain(hot))
        yield event.chain_result(content)

    async def send_v2ex_hot(self, event: AstrMessageEvent, context: Context):
        self.logger.info("send_v2ex_hot")
        hot_arr = await self.v2ex.get_hot()
        self.logger.info(hot_arr)
        content = []
        for hot in hot_arr:
            content.append(Plain(hot))
        yield event.chain_result(content)
