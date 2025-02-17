import logging
from .holiday import Holiday
from astrbot.api.all import Context, AstrMessageEvent, CommandResult, html_renderer

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

    async def html_render(self, tmpl: str, data: dict, return_url=True) -> str:
        '''渲染 HTML'''
        return await html_renderer.render_custom_template(tmpl, data, return_url=return_url)

    async def today_info_desc(self, event: AstrMessageEvent):
        url = await self.html_render(HTML, {"items": self.holiday_process.getTodayDesc()})
        yield event.image_result(url)
