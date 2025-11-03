import os
import json
import datetime
import asyncio
import aiohttp
from astrbot.api import Plugin

class DailyReminder(Plugin):
    def __init__(self, bot):
        super().__init__(bot)
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")
        self.tasks = []
        self.sent_today = set()  # 记录今天已发送的任务，避免重复
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.tasks = json.load(f).get("tasks", [])
        else:
            self.logger.error("配置文件不存在: " + self.config_path)

    async def on_startup(self):
        self.bot.loop.create_task(self.reminder_loop())

    async def reminder_loop(self):
        while True:
            now_time = datetime.datetime.now().strftime("%H:%M")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # 重置每日发送记录
            if not hasattr(self, 'last_date') or self.last_date != current_date:
                self.sent_today.clear()
                self.last_date = current_date
            
            for idx, task in enumerate(self.tasks):
                task_id = f"{current_date}_{idx}_{task['time']}"
                if task["time"] == now_time and task_id not in self.sent_today:
                    self.sent_today.add(task_id)
                    
                    # 判断是否使用API获取内容
                    if task.get("use_api", False):
                        message = await self.fetch_api_data(task)
                    else:
                        message = task["message"]
                    
                    if message:
                        await self.send_to_friend(task["qq"], message)
            
            await asyncio.sleep(60)

    async def fetch_api_data(self, task):
        """从API获取数据并格式化"""
        try:
            api_url = task.get("api_url")
            api_headers = task.get("api_headers", {})
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=api_headers, timeout=30) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.format_statistics(data)
                    else:
                        self.logger.error(f"API请求失败，状态码: {response.status}")
                        return None
        except asyncio.TimeoutError:
            self.logger.error("API请求超时")
            return None
        except Exception as e:
            self.logger.error(f"获取API数据失败: {e}")
            return None

    def format_statistics(self, data):
        """格式化统计数据"""
        try:
            message = f"""📊 【每日统计报告】

🔑 密钥统计
• 总应用数: {data['totalApps']}
• 总密钥数: {data['totalKeys']}
• 已用密钥: {data['usedKeys']}
• 未用密钥: {data['unusedKeys']}
• 过期密钥: {data['expiredKeys']}
• 活跃密钥: {data['activeKeys']}

📈 今日数据
• 今日使用: {data['todayUsedKeys']} 个密钥
• 今日生成: {data['todayGeneratedKeys']} 个密钥
• 今日成功: {data['todaySuccessCount']} 次
• 今日金额: ¥{data['todayAmount']:.2f}

📊 昨日对比
• 昨日使用: {data['yesterdayUsedKeys']} 个密钥
• 昨日生成: {data['yesterdayGeneratedKeys']} 个密钥
• 昨日成功: {data['yesterdaySuccessCount']} 次
• 昨日金额: ¥{data['yesterdayAmount']:.2f}

📉 变化趋势
• 使用变化: {data['usedKeysChange']:.2f}%
• 生成变化: {data['generatedKeysChange']:.2f}%
• 成功变化: {data['successCountChange']:.2f}%
• 金额变化: {data['amountChange']:.2f}%

👥 其他信息
• 在线用户: {data['onlineUsers']} 人
• 总成功次数: {data['totalSuccessCount']}
• 总金额: ¥{data['totalAmount']:.2f}
• 总验证次数: {data['totalVerifications']}
"""
            return message
        except Exception as e:
            self.logger.error(f"格式化数据失败: {e}")
            return None

    async def send_to_friend(self, qq, message):
        try:
            await self.bot.call_api(
                "send_private_msg",
                user_id=qq,
                message=message
            )
            self.logger.info(f"已向 {qq} 发送提醒")
        except Exception as e:
            self.logger.error(f"发送给 {qq} 失败: {e}")
