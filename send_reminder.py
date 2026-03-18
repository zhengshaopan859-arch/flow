#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心流APIKey提醒脚本
用于GitHub Actions定时发送飞书提醒
"""

import requests
from datetime import datetime

# 飞书Webhook地址
WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/72f8caa6-69ea-4ad0-93af-d5695976223c"


def send_reminder():
    """发送提醒消息"""
    # 从2026-03-16开始计算，第7天提醒
    start_date = datetime(2026, 3, 16)
    today = datetime.now()
    days_passed = (today - start_date).days + 1  # 今天算第1天
    
    days_left = 7 - days_passed
    
    if days_passed == 7:
        message = f"""🔔 **心流APIKey提醒 (第7天)**

⏰ 时间：{today.strftime('%Y-%m-%d %H:%M:%S')}

📝 请记得去重置心流APIKey！
🔗 地址：https://platform.iflow.cn/profile?tab=apiKey

💡 账号：17706008679"""
    else:
        message = f"""🔔 **心流APIKey提醒 (第{days_passed}天)**

⏰ 时间：{today.strftime('%Y-%m-%d %H:%M:%S')}

📝 今天是第{days_passed}天，距离第7天提醒还有{days_left}天
🔗 地址：https://platform.iflow.cn/profile?tab=apiKey

💡 账号：17706008679"""

    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }

    response = requests.post(WEBHOOK, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200


if __name__ == "__main__":
    send_reminder()
