import aiohttp
import logging
import re
from lxml import etree
from bs4 import BeautifulSoup

class NGAQFXHotHandler:

    def __init__(self):
        super().__init__()
        self.hot_url = 'https://momoyu.cc/api/hot/rss?code=OTg='
        self.logger = logging.getLogger("astrbot")

    async def get_hot(self) -> list[str]:
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
                            # 使用正则表达式移除 "1." 这样的前缀
                            title = re.sub(r'^\d+\.\s*', '', title)
                            url = url.replace("nga.178.com", "bbs.nga.cn", 1)
                            hot_arr.append(f"标题: {title}\n链接: {url}")
                    return hot_arr
                except Exception as e:
                    self.logger.error(f"momoyu rss解析失败,原因:{repr(e)}")
                    hot_arr = ["momoyu rss解析失败"]
                    return hot_arr

