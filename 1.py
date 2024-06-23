from flask import Flask, request, jsonify
import requests
import json
import hashlib
import random
import sqlite3

app = Flask(__name__)

@app.route("/send_stock_order", methods=["POST"])
def send_stock_order():
    # 获取请求参数
    phone = request.json.get("phone")
    password = request.json.get("password")
    productCode = request.json.get("productCode")

    data = login_with_sha3_224(phone, password)

    if data:
        # 后续可以使用data进行其他操作
        token = data
        order_type = 20
        biz_type = "21"
        stock_order_details = [
            {
                "seq": 1,
                "productCode": productCode,
                "qty": random.randint(100, 5000),
                "stockOrderDetailCustomFieldsValue": []
            }
        ]

        result = send_stock_order_api(token, order_type, biz_type, stock_order_details)
        if result is not None:
            return jsonify(result)
        else:
            return jsonify({"message": "接口调用失败"}), 500
    else:
        return jsonify({"message": "登录失败"}), 400

def login_with_sha3_224(phone, password):
    url = "https://liteweb.blacklake.cn/api/user/v1/users/_login"
    headers = {
        "X-CLIENT": "lite-web",
        "Content-Type": "application/json"
    }

    sha3_224 = hashlib.sha3_224()
    sha3_224.update(password.encode('utf-8'))
    hashed_password = sha3_224.hexdigest()

    data = {
        "phone": phone,
        "password": hashed_password
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()

    if response.status_code == 200:
        if result["message"] == "成功":
            return result["data"]
        else:
            print("登录失败")
            print(result["message"])
    else:
        print("接口调用失败")
        print(response.text)

def send_stock_order_api(token, order_type, biz_type, stock_order_details):
    url = "https://liteweb.blacklake.cn/api/dytin/external/stock/order/add"
    headers = {
        "X-AUTH": token,
        "Content-Type": "application/json"
    }

    data = {
        "orderType": order_type,
        "bizType": biz_type,
        "stockOrderDetails": stock_order_details
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print("接口调用失败")
        print(response.text)
        return None

if __name__ == "__main__":
    app.run()
