#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import sys
from datetime import datetime

# ==================== 配置区域 ====================
PUSH_TITLE = "🔔 心流APIKey提醒"
BASE_DAY = 1
TARGET_DAY = 7
IFLOW_URL = "https://platform.iflow.cn/profile?tab=apiKey"
IFLOW_ACCOUNT = "17706008679"
# ==================== 核心功能函数 ====================
def send_feishu_push(webhook_url, title, content):
    # 改用飞书【纯文本消息】格式，最稳定，不会报错
    data = {
        "msg_type": "text",
        "content": {
            "text": f"{title}\n{content}"
        }
    }
    try:
        response = requests.post(
            webhook_url,
            json=data,
            timeout=10
        )
        result = response.json()
        if result.get("code") == 0 or result.get("StatusCode") == 0:
            return True
        else:
            print(f"❌ 飞书返回错误：{result}")
            return False
    except Exception as e:
        print(f"❌ 飞书请求失败：{str(e)}")
        return False

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def build_push_content():
    remaining_days = TARGET_DAY - BASE_DAY
    content = f"""
(第{BASE_DAY}天)
━━━━━━━━━━━━━━━━━━
⏰ 时间：{get_current_time()}
📝 今天是第{BASE_DAY}天，距离第7天提醒还有{remaining_days}天
🔗 地址：{IFLOW_URL}
💡 账号：{IFLOW_ACCOUNT}
━━━━━━━━━━━━━━━━━━"""
    return content

def main():
    print("=" * 50)
    print("🚀 心流APIKey提醒推送程序启动")
    print("=" * 50)

    print("\n📋 第一步：获取飞书Webhook配置...")
    feishu_webhook = os.environ.get("FEISHU_WEBHOOK")
    if not feishu_webhook or len(feishu_webhook) < 20:
        print("❌ 错误：FEISHU_WEBHOOK 未设置或无效")
        sys.exit(1)
    print(f"✅ 飞书Webhook已配置")

    print("\n📝 第二步：构建提醒内容...")
    push_content = build_push_content()
    print(f"✅ 内容构建完成")

    print("\n📱 第三步：发送飞书提醒...")
    push_success = send_feishu_push(feishu_webhook, PUSH_TITLE, push_content)
    if push_success:
        print("✅ 推送成功！")
    else:
        print("❌ 推送失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
