import logging
from .holiday import Holiday
from astrbot.api.all import *

HTML = '''
<div style="padding: 20px;
    margin-bottom: 20px;
    color: #8a6d3b;
    background-color: #fcf8e3;
    border: 1px solid #faebcc;
    border-radius: 20px;
    line-height: 1.4em;
    font-size: 14px;
    transition: border-color .3s, background-color .3s;">
    <span>
        {% for item in items %}
        {{ item }}<br/>
        {% endfor %}
    </span>
</div>
'''
class Main:
    def __init__(self, context: Context) -> None:
        self.NAMESPACE = "astrbot_plugin_mofish"
        self.context = context
        self.logger = logging.getLogger("astrbot")
        self.context.register_commands(self.NAMESPACE, "mofish", "今日摸鱼", 1, self.today_info_desc)
        self.holiday_process = Holiday()


    async def today_info_desc(self, event: AstrMessageEvent):
        url = await self.html_render(TMPL, {"items": self.holiday_process.getTodayDesc()})
        yield event.image_result(url)
