import aiohttp
import logging
import datetime
from lxml import etree
from bs4 import BeautifulSoup
# NGA晴风村
class NGAQFXHotHandler:

    def __init__(self):
        super().__init__()
        self.hot_url = 'https://momoyu.cc/api/hot/rss?code=OTg='
        self.logger = logging.getLogger("astrbot")

    async def get_hot(self):
        hot_arr = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self.hot_url) as resp:
                if resp.status != 200:
                    self.logger.error(f"momoyu rss请求失败, url:{self.hot_url}")
                    hot_arr = ["momoyu rss请求失败"]
                    return hot_arr
                try:
                    text = await resp.read()
                    root = etree.fromstring(text)
                    items = root.xpath("//item")
                    for item in items:
                        description = item.xpath("description")[0].text
                        soup = BeautifulSoup(description, 'html.parser')
                        for a_tag in soup.find_all('a'):
                            url = a_tag.get('href')
                            title = a_tag.text
                            hot_arr.append(f"标题: {title}")
                            hot_arr.append(f"链接: {url}")
                            hot_arr.append("\n")
                except Exception as e:
                    self.logger.error(f"momoyu rss解析失败,原因:{e}")
                    hot_arr = ["momoyu rss解析失败"]
                    return hot_arr

