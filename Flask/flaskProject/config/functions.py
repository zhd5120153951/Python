import cv2
import numpy as np
import base64
import requests
import time


def check_api_status(monitored_api_url):
    """检查api服务的状态"""
    api_static = {'start_time': None, 'status': 'offline'}   # 被监控服务的状态信息
    try:
        response = requests.get(monitored_api_url, timeout=2)
        if response.status_code == 200:
            if response.json().get('status') == 'healthy':
                api_static['start_time'] = time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime())
                api_static['status'] = 'online'
        else:
            api_static['status'] = 'offline'
    except:
        api_static['status'] = 'offline'
    return api_static


# 二次帧差判断
def is_same_data(a, b):
   # 第一帧不做判断
    if a == None:
        return False
    gray_a = rgb2gray(a)
    gray_b = rgb2gray(b)
    # 计算帧差
    frame_diff = cv2.absdiff(gray_a, gray_b)
    threshold = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)[1]

    # 进行形态学处理，去除噪声
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    threshold = cv2.erode(threshold, kernel)

    threshold = cv2.dilate(threshold, kernel)
    contours, _ = cv2.findContours(
        threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # 相似--无运动目标
        if cv2.contourArea(contour) < 1000:
            return True
        # 不相似--有运动目标
        else:
            return False


def rgb2gray(rgb):
    res = rgb['image']
    input_image = base64.b64decode(res)
    # print(input_image)
    imBytes = np.frombuffer(input_image, np.uint8)
    # print(imBytes)
    iImage = cv2.imdecode(imBytes, cv2.IMREAD_COLOR)
    # 转换为灰度图像
    gray = cv2.cvtColor(iImage, cv2.COLOR_BGR2GRAY)
    return gray


if __name__ == '__main__':
    pass
