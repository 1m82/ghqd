# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import time
from cryptography.fernet import Fernet
import schedule
import threading

# 生成密钥并加密密码
def generate_key():
    return Fernet.generate_key()

def encrypt_password(password, key):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode()).decode()

# 签到函数
def sign_in(user_id, encrypted_password):
    headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    url = "https://m.sgzy.com.cn:2000/app/AppAuth.ashx"
    signUrl = "https://m.sgzy.com.cn:2000/app/AppBusiness.ashx"

    res = requests.post(url, data={"action": "login", "UserID": user_id, "Password": encrypted_password}, headers=headers)
    token = json.loads(res.text)["Token"]
    data = {"token": token, "action": "sign"}
    time.sleep(1)
    sign = requests.post(signUrl, data=data, headers=headers).text
    return json.loads(sign)["Msg"]

# 定时任务
def job():
    key = generate_key()  # 生成密钥
    # 用户信息
    user_info = [
        {"user_id": "BED4FC501850E5ACFB1477C855540316F686365DA6E4F061", "password": "6CBB7E8C5DB81A02C54AE10F0EA876E5"},
        {"user_id": "26F10DB2C9C7B3F81620EA24559B1E48B42842C745B58C59", "password": "6CBB7E8C5DB81A02C54AE10F0EA876E5"}
    ]
    
    for user in user_info:
        encrypted_password = encrypt_password(user["password"], key)
        result = sign_in(user["user_id"], encrypted_password)
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
        key = generate_key()  # 生成密钥
        user_info = [
            {"user_id": st.text_input("输入 chl 用户ID"), "password": st.text_input("输入 chl 密码", type="password")},
            {"user_id": st.text_input("输入 lmy 用户ID"), "password": st.text_input("输入 lmy 密码", type="password")}
        ]
        
        for user in user_info:
            if user["user_id"] and user["password"]:  # 检查用户ID和密码是否输入
                encrypted_password = encrypt_password(user["password"], key)
                result = sign_in(user["user_id"], encrypted_password)
                st.write(f"{user['user_id']} 签到结果: {result}")
            else:
                st.write("请确保输入用户ID和密码。")  # 提示用户输入信息

    st.write("执行完毕，自动退出！")
