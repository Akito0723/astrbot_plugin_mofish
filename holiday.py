import aiohttp
import logging
import json
import os
import asyncio
import random
from datetime import datetime, timedelta

Hitokoto = ["认认真真地上班，根本不叫赚钱，这是劳动换取报酬。只有偷懒，在上班的时候浑水摸鱼，那才是从你老板那赚到了钱。",
            "“时间是一直过的很快，还是只有在摸鱼的时候是？”",
            "工作是用来赚钱的，摸鱼是用来续命的。人生苦短，难得清闲，摸鱼才是职场的顶级哲学。",
            "古人云：‘为天地立心，为生民立命。’我却说：‘为工资摸鱼，为自由争命。’",
            "摸鱼的意义不在于摸鱼本身，而在于一种心理上的反抗，是对资本剥削的无声抗议。",
            "人在职场，摸鱼第一。老板是虚无的，工作是浮云的，只有摸鱼才是实实在在的快乐。",
            "摸鱼一时爽，一直摸鱼一直爽。生活不止有工作，还有坐在办公桌前偷偷刷手机的那份悠然。",
            "你可以不爱你的工作，但一定要爱摸鱼的时光。因为那是你生命里最真实、最自由的时刻。",
            "摸鱼是一种技术活，偷得浮生半日闲，不是混日子，而是平衡身心健康的智慧。",
            "摸鱼的终极目标：在看似忙碌的状态中实现灵魂的深度休息，同时还能稳稳拿到工资。",
            "有人摸鱼是怕被老板骂，有人摸鱼是怕被扣工资，而我是为了找回工作中失去的灵魂。",
            "摸鱼是一门艺术，而我，就是这门艺术的大师。",
            "摸鱼是一种抵抗996的温柔方式，悄悄地摸，认真地活。",
            "摸鱼的意义在于，工作能给你薪水，摸鱼能给你快乐。",
            "在工作中，摸鱼让我短暂自由；在生活中，摸鱼让我保持理智。",
            "摸鱼时光虽短，但胜过无数乏味的会议和无尽的表格。",
            "摸鱼，是疲惫生活里的光；偷闲，是无趣工作的糖。",
            "摸鱼时，我的眼睛看着屏幕，但我的心早已飞向自由。",
            "摸鱼不只是一种行为，更是一种哲学：‘工作未必要全力以赴，生活一定要认真摸鱼。’",
            "摸鱼，是对工作的调味剂；偷闲，是对生活的润滑剂。",
            "老板以为我在工作，其实我在摸鱼。摸鱼是艺术，欺骗是技术。",
            "摸鱼的每一分钟，都是我对生活的小小抗争。",
            "摸鱼的最高境界：所有人都觉得你很忙，只有你知道自己在偷闲。",
            "摸鱼的精髓在于，用最忙碌的姿态做最放松的事情。",
            "摸鱼时间是有限的，但摸鱼的乐趣是无穷的。",
            "如果工作能像摸鱼一样快乐，那这个世界一定会更加美好。",
            "别人的午休是睡觉，我的午休是摸鱼。快感加倍，精神满分。",
            "摸鱼这件事，不需要计划，但一定需要勇气。",
            "用摸鱼平衡工作的无聊，才是对生活最大的尊重。",
            "没有摸鱼的工作是枯燥的，没有自由的生活是乏味的。",
            "摸鱼，是职场哲学的一部分；懂摸鱼的人，才是职场高手。",
            "摸鱼是每个打工人的特权，轻松一刻，才有继续工作的力气。"
            ]
class Holiday:
    def __init__(self):
        now = datetime.now()
        self.logger = logging.getLogger("astrbot")
        self._holiday_data = {}
        self._load_holiday(now)

    def get_holiday_data(self, now):
        if self._holiday_data.get(now.year) is None:
            self._load_holiday(now)
        return self._holiday_data.get(now.year)

    def _load_holiday(self, now):
        holiday_data_file = f"data/astrbot_plugin_mofish_holiday_{now.year}.json"
        if not os.path.exists(holiday_data_file):
            asyncio.run(self._init_holiday_data(now, holiday_data_file))
        with open(holiday_data_file, "r") as f:
            self._holiday_data = {now.year: json.load(f)}

    async def _init_holiday_data(self, now, holiday_data_file):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://timor.tech/api/holiday/year/{now.year}?type=Y&week=Y") as response:
                with open(holiday_data_file, "w") as f:
                    response_json = await response.json()
                    code = response_json.get('code')
                    if code != 0:
                        self.logger.error(f"获取: {now.year} 假期数据失败, response: {response.json()}")
                        json.dump({}, f)
                    else:
                        json.dump(response_json.get("holiday"), f)
                        self.logger.debug(f"获取: {now.year} 假期数据成功")

    '''获取今日信息'''
    def getTodayDesc(self) -> list:
        desc_arr = []
        now = datetime.now()
        # 星期几的处理
        weekday = "周" + ["一", "二", "三", "四", "五", "六", "日"][now.weekday()]
        # 找到对应的时间段描述
        hour = now.hour
        hour_desc_map = {
            range(0, 6): "的凌晨",
            range(6, 9): "的早上",
            range(9, 12): "的上午",
            range(12, 14): "的中午",
            range(14, 17): "的下午",
            range(17, 19): "的傍晚",
            range(19, 23): "的晚上",
            range(23, 24): "的晚上"
        }
        hour_desc = next(desc for time_range, desc in hour_desc_map.items() if hour in time_range)
        desc_arr.append(f'📣 摸鱼提醒：今天是{now.month}月{now.day}日，{weekday}的{hour_desc}')

        # 随机摸鱼一言
        random_hitokoto = random.choice(Hitokoto)
        desc_arr.append(random_hitokoto)

        holiday_data = self.get_holiday_data(now)
        today_info = holiday_data.get(now.strftime('%m-%d'))

        # now = datetime.strptime('2025-01-26', '%Y-%m-%d')
        if today_info is None:
            # 今天不是休息日
            next_weekend_day_info, next_holiday_day_info = self._get_next_weekend_and_holiday(holiday_data, now)
            next_weekend_day_diff = (datetime.strptime(next_weekend_day_info['date'], '%Y-%m-%d') - now).days + 1
            next_holiday_day_diff = (datetime.strptime(next_holiday_day_info['date'], '%Y-%m-%d') - now).days + 1
            if next_holiday_day_diff < next_weekend_day_diff:
                # 先过节假日
                desc_arr.append(f"距离{next_holiday_day_info['name']}还有{next_holiday_day_diff}天")
            else:
                desc_arr.append(f"距离周末还有{next_weekend_day_diff}天")
                desc_arr.append(f"距离{next_holiday_day_info['name']}还有{next_holiday_day_diff}天")
        elif today_info['holiday']:
            # 今天补班 QAQ
            next_weekend_day_info, next_holiday_day_info = self._get_next_weekend_and_holiday(holiday_data, now)
            next_weekend_day_diff = (datetime.strptime(next_weekend_day_info['date'], '%Y-%m-%d') - now).days + 1
            next_holiday_day_diff = (datetime.strptime(next_holiday_day_info['date'], '%Y-%m-%d') - now).days + 1
            if next_holiday_day_diff < next_weekend_day_diff:
                # 先过节假日
                desc_arr.append(f"距离{next_holiday_day_info['name']}还有{next_holiday_day_diff}天")
            else:
                desc_arr.append(f"距离周末还有{next_weekend_day_diff}天")
                desc_arr.append(f"距离{next_holiday_day_info['name']}还有{next_holiday_day_diff}天")
        else:
            # 今天休息!
            if today_info['name'] == '周六' or today_info['name'] == '周日':
                desc_arr.append("周末愉快~")
            else:
                desc_arr.append("有啥事节后再说~")
        return desc_arr

    def _get_next_weekend_and_holiday(self, holiday_data, now):
        next_weekend_day_info = None
        next_holiday_day_info = None
        i = 1
        while True:
            next_day = now + timedelta(days=i)
            next_day_info = holiday_data.get(next_day.strftime('%m-%d'))
            if (next_day_info is not None and next_day_info['holiday'] and next_weekend_day_info is None
                    and (next_day_info['name'] == '周六' or next_day_info['name'] == '周日')):
                # 找到了下一个周末
                next_weekend_day_info = next_day_info
            if (next_day_info is not None and next_day_info['holiday'] and next_holiday_day_info is None
                    and next_day_info['name'] != '周六' and next_day_info['name'] != '周日'):
                # 找到了下一个节假日
                next_holiday_day_info = next_day_info
            if next_weekend_day_info is not None and next_holiday_day_info is not None:
                # 下一个周末和下一个节假日都找到了以后
                break
            if i >= 365:
                # 防止 while True
                break
            i = i + 1
        return next_weekend_day_info, next_holiday_day_info