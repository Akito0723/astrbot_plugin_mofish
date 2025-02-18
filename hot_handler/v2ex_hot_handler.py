import aiohttp
import logging
import datetime

class V2exHotHandler:

    def __init__(self):
        super().__init__()
        self.hot_url = 'https://www.v2ex.com/api/topics/hot.json'
        self.logger = logging.getLogger("astrbot")

    async def get_hot(self) -> list[str]:
        hot_arr = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.hot_url, timeout=5) as resp:
                    if resp.status != 200:
                        self.logger.error(f"v2ex api请求失败, url:{self.hot_url}")
                        hot_arr = ["v2ex api请求失败"]
                        return hot_arr
                    try:
                        resp_json = await resp.json()
                        for item in resp_json:
                            if item.get('node').get('name') != 'life':
                                continue
                            title = item.get('title')
                            url = item.get('url')
                            created_day = datetime.datetime.fromtimestamp(item.get('created')).strftime("%Y-%m-%d")
                            content = item.get('content')
                            if len(content) > 10:
                                content = content[:10] + '...'
                            hot_arr.append(f"标题: {title}\n发帖时间: {created_day}\n内容: {content}\n链接: {url}")
                        return hot_arr
                    except Exception as e:
                        self.logger.error(f"v2ex api解析失败,原因:{repr(e)}")
                        hot_arr = ["v2ex api解析失败"]
                        return hot_arr
        except Exception as e:
            self.logger.error(f"v2ex api连接失败,原因:{repr(e)}")
            hot_arr = ["v2ex api解析失败"]
            return hot_arr
