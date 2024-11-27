# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import time
import schedule
import threading

# 签到函数
def sign_in(user_id, password):
    headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    url = "https://m.sgzy.com.cn:2000/app/AppAuth.ashx"
    signUrl = "https://m.sgzy.com.cn:2000/app/AppBusiness.ashx"

    res = requests.post(url, data={"action": "login", "UserID": user_id, "Password": password}, headers=headers)
    token = json.loads(res.text)["Token"]
    data = {"token": token, "action": "sign"}
    time.sleep(1)
    sign = requests.post(signUrl, data=data, headers=headers).text
    return json.loads(sign)["Msg"]

# 定时任务
def job():
    # 用户信息
    user_info = [
        {"user_id": "BED4FC501850E5ACFB1477C855540316F686365DA6E4F061", "password": "6CBB7E8C5DB81A02C54AE10F0EA876E5"},
        {"user_id": "26F10DB2C9C7B3F81620EA24559B1E48B42842C745B58C59", "password": "6CBB7E8C5DB81A02C54AE10F0EA876E5"}
    ]
    
    for user in user_info:
        result = sign_in(user["user_id"], user["password"])  # 直接使用密码
        print(f"{user['user_id']} 签到结果: {result}")

# 启动定时任务
def run_schedule():
    schedule.every().day.at("06:30").do(job)
    schedule.every().day.at("12:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# 主程序
if __name__ == '__main__':
    st.title("签到系统")

    # 启动定时任务线程
    threading.Thread(target=run_schedule, daemon=True).start()

    if st.button("手动签到"):
        job()  # 直接调用job方法进行手动签到

    st.write("执行完毕，自动退出！")
