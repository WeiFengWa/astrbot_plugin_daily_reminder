# AstrBot 每日提醒插件

一个用于 AstrBot 的定时提醒插件，支持定时向指定QQ好友发送消息，可以发送静态文本或从API获取动态数据。

## ✨ 功能特性

- 🕐 支持多个定时任务
- 📨 自动向指定QQ好友发送提醒消息
- 🌐 支持从API获取动态数据
- 📊 内置统计数据格式化
- 🔄 自动避免重复发送
- ⚙️ 灵活的配置系统

## 📦 安装

1. 将插件文件放置到 AstrBot 插件目录
2. 确保已安装 `aiohttp` 依赖：

```bash
pip install aiohttp
```

## ⚙️ 配置说明

编辑 `config.json` 文件：

```json
{
  "tasks": [
    {
      "time": "09:00",
      "qq": "123456789",
      "message": "早上好！",
      "use_api": false
    },
    {
      "time": "14:00",
      "qq": "987654321",
      "message": "每日统计数据",
      "use_api": true,
      "api_url": "https://api.example.com/stats",
      "api_headers": {
        "authorization": "Bearer YOUR_TOKEN",
        "accept": "application/json"
      }
    }
  ]
}
```

### 配置项说明

- `time`: 发送时间，格式为 "HH:MM"（24小时制）
- `qq`: 接收消息的QQ号
- `message`: 消息内容描述（use_api为false时为实际发送内容）
- `use_api`: 是否从API获取数据（可选，默认false）
- `api_url`: API地址（use_api为true时必填）
- `api_headers`: API请求头（可选）

## 📊 API数据格式

插件内置了统计数据格式化功能，期望API返回如下格式的JSON数据：

```json
{
  "totalApps": 48,
  "totalKeys": 4729,
  "usedKeys": 4621,
  "unusedKeys": 73,
  "todaySuccessCount": 18,
  "todayAmount": 910.33,
  ...
}
```

## 🎨 自定义格式化

如需自定义API数据格式化，可修改 `daily_reminder.py` 中的 `format_statistics` 方法。

## 📝 使用示例

### 1. 简单文本提醒

```json
{
  "time": "09:00",
  "qq": "123456789",
  "message": "早上好，记得喝水！"
}
```

### 2. API动态数据

```json
{
  "time": "09:00",
  "qq": "123456789",
  "use_api": true,
  "api_url": "https://api.example.com/daily-stats",
  "api_headers": {
    "authorization": "Bearer YOUR_TOKEN"
  }
}
```

## ⚠️ 注意事项

1. 时间检查间隔为60秒，请确保任务时间精确到分钟
2. API请求超时时间为30秒
3. 同一任务每天只会发送一次，避免重复
4. 请妥善保管API认证信息，不要泄露token

## 🔧 技术栈

- Python 3.7+
- aiohttp - 异步HTTP客户端
- AstrBot API

## 📄 许可证

MIT License

## 👤 作者

小懒

## 🔗 链接

- [项目仓库](https://github.com/xiaolan0216/astrbot_plugin_daily_reminder)
- [AstrBot文档](https://astrbot.app)

## 🐛 问题反馈

如有问题或建议，请在GitHub提交Issue。
