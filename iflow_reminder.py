#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import sys
from datetime import datetime

# ==================== 配置区域 ====================
PUSH_TITLE = "🔔 心流APIKey提醒"
BASE_DAY = 1  # 可自行修改当前天数
TARGET_DAY = 7  # 可自行修改目标提醒天数
IFLOW_URL = "https://platform.iflow.cn/profile?tab=apiKey"
IFLOW_ACCOUNT = "17706008679"
# ==================== 核心功能函数 ====================
def send_feishu_push(webhook_url, title, content):
    # 纯文本格式，飞书机器人100%兼容，无参数报错
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
    # 格式化北京时间，只保留时分，更简洁
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def build_push_content():
    remaining_days = TARGET_DAY - BASE_DAY
    # 精简提醒内容，适配飞书纯文本展示
    content = f"""
(第{BASE_DAY}天)
━━━━━━━━━━━━━━━━━━
⏰ 提醒时间：{get_current_time()}
📝 今日状态：今天是第{BASE_DAY}天，距离第{TARGET_DAY}天提醒还有{remaining_days}天
🔗 APIKey地址：{IFLOW_URL}
💡 绑定账号：{IFLOW_ACCOUNT}
━━━━━━━━━━━━━━━━━━
⚠️  及时关注APIKey状态，避免过期影响使用！"""
    return content

def main():
    print("=" * 50)
    print("🚀 心流APIKey提醒推送程序启动")
    print("=" * 50)

    print("\n📋 第一步：获取飞书Webhook配置...")
    feishu_webhook = os.environ.get("FEISHU_WEBHOOK")
    # 校验Webhook有效性，避免短地址错误
    if not feishu_webhook or len(feishu_webhook) < 50:
        print("❌ 错误：FEISHU_WEBHOOK 未设置或地址无效")
        sys.exit(1)
    print(f"✅ 飞书Webhook已成功获取")

    print("\n📝 第二步：构建提醒内容...")
    push_content = build_push_content()
    print(f"✅ 提醒内容构建完成：\n{push_content}")

    print("\n📱 第三步：发送飞书提醒推送...")
    push_success = send_feishu_push(feishu_webhook, PUSH_TITLE, push_content)
    if push_success:
        print("✅ 飞书提醒推送成功！")
    else:
        print("❌ 飞书提醒推送失败")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("✅ 程序执行完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
