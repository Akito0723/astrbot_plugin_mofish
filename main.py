import logging
from .holiday import Holiday
from astrbot.api.all import Context, AstrMessageEvent, CommandResult

class Main:
    def __init__(self, context: Context) -> None:
        self.NAMESPACE = "astrbot_plugin_mofish"
        self.context = context
        self.logger = logging.getLogger("astrbot")
        self.context.register_commands(self.NAMESPACE, "mofish", "今日摸鱼", 1, self.today_info_desc)
        self.holiday_process = Holiday()



    async def today_info_desc(self, event: AstrMessageEvent):
        yield event.plain_result('\n'.join(self.holiday_process.getTodayDesc()))
        # yield event.image_result(url)
