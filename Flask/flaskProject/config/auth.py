import hashlib
import time
import uuid
import hmac
import base64

# 这个是由软件服务器生成
appKey = "lRAPKJRh"
appSecret = "50f4a5b5ad4ea835fbd3f3ddc76d6efead032df8"


def generate_auth_params():
    timestamp = str(int(time.time() * 1000))
    print("timestamp:", timestamp)
    nonce = str(uuid.uuid4())
    print("nonce:", nonce)
    return timestamp, nonce


def generate_signature(timestamp, nonce, body_form):
    # 拼接签名字符串
    # query_string = '&'.join([f'{k}={v}' for k, v in query_form.items()])
    body_string = '&'.join([f'{k}={v}' for k, v in body_form.items()])
    print("body_string:", body_string)
    # sign_string = f'/camera/list?ts={timestamp}&nonce={nonce}'
    sign_string = f'/camera_algorithm/get_by_node_code?ts={timestamp}&nonce={nonce}'
    # sign_string = f'/analysis?={timestamp}&nonce={nonce}'
    print("sign_string:", sign_string)
    # 计算签名
    signature = hmac.new(appSecret.encode('utf-8'),
                         sign_string.encode('utf-8'), hashlib.sha256).digest()
    signature_base64 = base64.b64encode(signature).decode('utf-8')
    return signature_base64
