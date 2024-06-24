import requests
import json
from flask import Flask, request, jsonify
from config.auth import generate_signature, generate_auth_params, appKey
from config.functions import check_api_status
app = Flask(__name__)

# app秘钥
app.secret_key = "greatech_flask"
# 被监控服务url
monitored_api_url = "http://127.0.0.1:5001/infer"


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    """测试心跳功能的服务接口"""
    api_static = check_api_status(monitored_api_url)
    if api_static['status'] == 'online':
        return jsonify({
            'status': 'online',
            'start_time': api_static['start_time'],
            'message': 'this api service is online'
        })
    else:
        return jsonify({
            'status': 'offline',
            'start_time': api_static['start_time'],
            'message': 'this api service is offline'
        })


@app.route('/param_info', methods=['GET', 'POST'])
def param_info():
    if request.method == 'GET':
        timestamp, nonce = generate_auth_params()
        signature = generate_signature(timestamp, nonce, dict())
        headers = {
            'X-Ge-Key': appKey,
            'X-Ge-Signature': signature,
            'X-Ge-Timestamp': timestamp,
            'X-Ge-Nonce': nonce,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        ret = requests.get("http://192.168.20.5:8001/ms-video-ai-analysis/camera_algorithm/get_by_node_code",
                           data=json.dumps({"nodeCode": "1"}), headers=headers)
        if ret.status_code == 200:  # 请求web成功
            data = ret.json()
            print("请求到的参数：", data)
            return jsonify(data)
        else:
            print("请求前端json参数接口失败.")
            return jsonify({'code': ret.status_code, 'msg': ret.text})

    else:
        print("POST请求啊")
        data = request.get_json()
        print(type(data))
        print(data)
        # accessplatform = data["accessPlatform"]
        # cameraname = data["cameraName"]
        # id = data["id"]
        # manufacturer = data["manufacturer"]
        # online = data["online"]
        # url_path = "http://192.168.20.5:8001/device-manger/camera/list"
        url_path = "http://192.168.20.5:8001/ms-video-ai-analysis/camera_algorithm/get_by_node_code"
        # url_path = "http://192.168.20.5:9219/analysis"
        # 鉴权参数--每次调用后端接口都要生成
        # query_form = {}
        body_form = {
            # "accessPlatform": accessplatform,
            # "cameraName": cameraname,
            # "id": id,
            # "manufacturer": manufacturer,
            # "online": online
            "nodeCode": data['nodeCode']
        }
        print(type(body_form))
        print(body_form)
        timestamp, nonce = generate_auth_params()
        signature = generate_signature(timestamp, nonce, body_form)
        headers = {
            'X-Ge-Key': appKey,
            'X-Ge-Signature': signature,
            'X-Ge-Timestamp': timestamp,
            'X-Ge-Nonce': nonce,
            'Content-Type': 'application/json'
        }
        # ret = requests.post(url_path, data=json.dumps(data), headers=headers)
        ret = requests.get(url_path, data=json.dumps(data), headers=headers)

        if ret.status_code == 200:
            data = ret.json()
            print(data)
            return jsonify(data)
        else:
            return jsonify({'code': ret.status_code, 'msg': ret.text})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
