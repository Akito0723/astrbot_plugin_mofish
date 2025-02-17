import logging
from .holiday import Holiday
from astrbot.api.all import Context, AstrMessageEvent, CommandResult


class Main:
    def __init__(self, context: Context) -> None:
        self.NAMESPACE = "astrbot_plugin_mofish"
        self.context = context
        self.logger = logging.getLogger("astrbot")
        self.context.register_commands(self.NAMESPACE, "mofish", "每日摸鱼", 1, self.mofish)
        self.holiday_process = Holiday()

    async def mofish(self, event: AstrMessageEvent, context: Context):
        args = event.message_str.split(" ")
        help_msg = '\n'.join(['每日摸鱼 指令描述',
                              '/mofish today 今日信息'
                              '/mofish auto 启动/关闭每日 9 点发送摸鱼信息(锐意开发中)'])
        if len(args) < 2:
            return CommandResult().message(help_msg).use_t2i(False)
        if args[1] == "today":
            self.today_info_desc(event)
        elif args[1] == "auto":
            self.auto_send_mofish_info(event)

        elif args[1] == "help":
            return CommandResult().message(help_msg).use_t2i(False)
        else:
            return CommandResult().message(help_msg).use_t2i(False)

    async def today_info_desc(self, event: AstrMessageEvent):
        yield event.plain_result('\n'.join(self.holiday_process.getTodayDesc()))

    async def auto_send_mofish_info(self, event: AstrMessageEvent):
        yield event.plain_result('锐意开发中')
