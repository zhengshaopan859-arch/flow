#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心流APIKey 倒计时提醒推送脚本
用于 GitHub Actions 定时推送心流APIKey提醒至飞书
作者：自定义
功能:
    1. 固定心流APIKey相关提醒信息
    2. 计算倒计时（距离第7天提醒的剩余天数）
    3. 通过飞书机器人推送格式化提醒通知
"""
import os
import requests
import sys
from datetime import datetime

# ==================== 配置区域 ====================
# 推送标题
PUSH_TITLE = "🔔 心流APIKey提醒"
# 心流APIKey基础配置（可根据需要修改）
BASE_DAY = 1  # 当前是第1天
TARGET_DAY = 7  # 目标提醒第7天
IFLOW_URL = "https://platform.iflow.cn/profile?tab=apiKey"
IFLOW_ACCOUNT = "17706008679"
# ==================== 核心功能函数 ====================
def send_feishu_push(webhook_url, title, content):
    """
    通过飞书机器人发送推送（富文本卡片格式）
    参数:
        webhook_url: 飞书机器人 Webhook 地址
        title: 推送标题
        content: 推送内容（支持飞书markdown）
    返回:
        bool: 推送是否成功
    """
    # 飞书富文本卡片消息格式
    data = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "red"  # 红色模板突出提醒
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": content}
                }
            ]
        }
    }
    try:
        response = requests.post(
            webhook_url,
            json=data,
            timeout=10
        )
        result = response.json()
        # 兼容飞书不同机器人的返回码
        if result.get("code") == 0 or result.get("StatusCode") == 0:
            return True
        else:
            print(f"❌ 飞书推送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 飞书请求失败：{str(e)}")
        return False

def get_current_time():
    """获取当前北京时间（格式化）"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def build_push_content():
    """构建飞书推送的提醒内容"""
    remaining_days = TARGET_DAY - BASE_DAY  # 计算剩余天数
    content = f"""**(第{BASE_DAY}天)**
━━━━━━━━━━━━━━━━━━
⏰ 提醒时间：{get_current_time()}
📝 今日状态：今天是第{BASE_DAY}天，距离第{TARGET_DAY}天提醒还有**{remaining_days}天**
🔗 心流APIKey地址：[{IFLOW_URL}]({IFLOW_URL})
💡 绑定账号：{IFLOW_ACCOUNT}
━━━━━━━━━━━━━━━━━━
⚠️  请及时关注APIKey状态，避免过期影响使用！"""
    return content

def main():
    """主函数：程序入口"""
    print("=" * 50)
    print("🚀 心流APIKey提醒推送程序启动")
    print("=" * 50)

    # 从环境变量获取飞书Webhook（避免硬编码，适配GitHub Actions）
    print("\n📋 第一步：获取飞书Webhook配置...")
    feishu_webhook = os.environ.get("FEISHU_WEBHOOK")
    if not feishu_webhook:
        print("❌ 错误：未设置 FEISHU_WEBHOOK 环境变量")
        sys.exit(1)
    print(f"✅ 飞书Webhook已获取 (长度：{len(feishu_webhook)})")

    # 构建推送内容
    print("\n📝 第二步：构建提醒内容...")
    push_content = build_push_content()
    print(f"✅ 推送内容构建完成：\n{push_content}")

    # 发送飞书推送
    print("\n📱 第三步：发送飞书提醒推送...")
    push_success = send_feishu_push(feishu_webhook, PUSH_TITLE, push_content)
    if push_success:
        print("✅ 飞书提醒推送发送成功!")
    else:
        print("❌ 飞书提醒推送发送失败")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("✅ 程序执行完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()