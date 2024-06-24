

import argparse
import os
import platform
import sys
from pathlib import Path
import cv2

import torch
import time

from models.experimental import attempt_load
from utils.general import non_max_suppression

from shapely.geometry import Polygon
import numpy as np

# 加载模型


def load_detector(model_path, device='cpu'):

    model = attempt_load(model_path, device)
    model.eval()
    return model


def calculate_intersection_ratio(polygon_a_vertices, polygon_b_vertices):
    # 创建多边形A和B的shapely对象
    polygon_a = Polygon(polygon_a_vertices)
    polygon_b = Polygon(polygon_b_vertices)

    # 计算交集多边形C
    # intersection_polygon = intersection(polygon_a, polygon_b)
    intersection_polygon = polygon_a.intersection(polygon_b)
    # 检查是否有交集
    if intersection_polygon.is_empty:
        return 0.00  # 没有交集，返回0

    # 计算多边形B的面积和交集C的面积
    area_b = polygon_b.area
    area_intersection = intersection_polygon.area

    # 计算交集占多边形B的比例
    ratio = area_intersection / area_b

    # 保留两位小数
    return round(ratio, 2)

# 推理然后判断是否和墙有交集


def fanyue_pic(img_org_last, img_org, imgs,  model, wallPoints, thresh_person, inter_ratio, device='cpu'):

    # 前向传播
    # while 1:
    img_org_last_copy = np.copy(img_org_last)
    img_org_copy = np.copy(img_org)

    pred = model(imgs)[0]  # 前向传播，只获取预测结果（因为我们只预测一张图片）

    # 非极大值抑制（NMS）
    # 你可以调整 conf_thres 和 iou_thres
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.5)

    # condition = pred[:, -1] == 0
    # # 使用布尔索引来选择满足条件的行
    # pred = pred[condition]
    # 解析预测结果
    for det in pred[0]:  # det 是一个列表，每个元素是一个字典，表示一个检测到的物体
        per = det.cpu().numpy()
        x1, y1, x2, y2, score, cls = per
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if score > thresh_person and cls == 0:
            check_2pic_difference(img_org_last_copy, img_org_copy, wallPoints)
            # polygon_a_vertices = wallPoints
            # polygon_person = [(x1,y1),(x1,y2),(x2,y2),(x2,y1)]
            # ratio = calculate_intersection_ratio(wallPoints, polygon_person)
            # print(per) 17 95 261 259
            # print(ratio)
            cv2.rectangle(img_org_copy, (x1, y1), (x2, y2), (255, 0, 0), 3)
            # for k in range(len(wallPoints[0])-1):
            #     # print('wallPoints ',k)
            #     cv2.line(img_org,wallPoints[0][k],wallPoints[0][k+1], (255, 255, 0), 5)
            # cv2.line(img_org, wallPoints[0][0],wallPoints[0][-1], (255, 255, 0), 5)

    cv2.imshow('fuck', img_org_copy)
    cv2.waitKey(20)
    # 这里可以根据你的需要添加更多逻辑，比如绘制边界框等
    # 368 180     460 536


def check_2pic_difference(img_org_last, img_org, wallPoints):

    # img1 = set_mask(img_org_last,wallPoints)
    # img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    #
    # img2 = set_mask(img_org, wallPoints)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # # cv2.imshow('img1',img1)
    # # cv2.waitKey(20)
    #
    # diff = cv2.absdiff(img1, img2)

    diff = cv2.absdiff(img_org_last, img_org)
    diff1 = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff2 = set_mask(diff1, wallPoints)
    # cv2.imshow('diff2', diff2)
    # cv2.waitKey(20)
    # 步骤5: 二值化
    _, thresh = cv2.threshold(diff2, 20, 255, cv2.THRESH_BINARY)  # 阈值可能需要调整

    # 步骤6: 查找轮廓
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for k in range(len(wallPoints[0])-1):
        # print('wallPoints ',k)
        cv2.line(thresh, wallPoints[0][k],
                 wallPoints[0][k+1], (255, 255, 0), 5)
    cv2.line(thresh, wallPoints[0][0], wallPoints[0][-1], (255, 255, 0), 5)
    cv2.imshow('paowu quyu', thresh)
    cv2.waitKey(20)

    for contour in contours:
        # 计算轮廓的面积
        area = cv2.contourArea(contour)

        # 假设我们想要过滤掉面积小于1000的轮廓
        if area > 20:
            print(area)
            print("paowu")
            return
        else:
            # print('no paowu')
            pass


def set_mask(img, polyPoints1):

    img1 = img
    # img1 = cv2.imread('friday.png')

    height, width = img1.shape[0], img1.shape[1]

    # 创建一个与图片大小相同的掩码，初始化为全零（黑色）
    mask = np.zeros((height, width), dtype=np.uint8)

    # 在掩码上绘制多边形区域，设置为白色（即255）
    cv2.fillPoly(mask, polyPoints1, (255, 255, 255))
    # cv2.imshow('Filled Polygon', mask)
    # cv2.waitKey(0)
    # 如果图片是RGBA格式的，并且你想保持透明度，则需要在RGBA掩码上进行操作
    # 否则，直接使用下面的按位与操作将非多边形区域置零

    # 使用掩码将图片中非多边形区域置零
    # 如果图片是BGR格式的
    result = cv2.bitwise_and(img1, img1, mask=mask)

    return result


def test():
    img = np.zeros((500, 500, 3), dtype=np.uint8)

    # 定义一个三角形的顶点
    pts = np.array([[100, 200], [200, 200], [150, 300]], np.int32)
    pts = pts.reshape((-1, 1, 2))  # 转换为 fillPoly 所需的格式

    # 使用绿色填充三角形
    cv2.fillPoly(img, [pts], (0, 255, 0))

    # 显示图像
    cv2.imshow('Filled Polygon', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    # test()
    # img = cv2.imread('friday.png')
    # img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_LINEAR)
    # 人的检测区域
    personPoints = [(10, 10), (10, 600), (600, 600), (600, 10)]
    # 墙的区域
    wallPoints = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 60)]
    wallPoints = np.array([wallPoints], dtype=np.int32)
    personPoints = np.array([personPoints], dtype=np.int32)

    thresh_person = 0.25
    inter_ratio = 0.05

    model = load_detector('yolov5s.pt', device='cuda:0')

    # img = img.unsqueeze(0).permute(0,3,1,2)  # 添加批次维度，因为我们只预测一张图片
    # imgs = img.repeat(4, 1, 1, 1)

    rtsp = 'rtsp://admin:jiankong123@192.168.23.23:554/cam/realmonitor?channel=1&subtype=0'
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 640), interpolation=cv2.INTER_LINEAR)
    img_org = frame
    img_org_last = frame
    while 1:
        t1 = time.time()

        # inputimg = imgs
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 640), interpolation=cv2.INTER_LINEAR)
        img_org = frame
        # cv2.imshow('fuckxx', frame)
        # cv2.waitKey(0)
        img = set_mask(frame, personPoints)
        img = torch.from_numpy(img).to('cuda:0')
        img = img.float()  # uint8 to fp16/32
        img = img.unsqueeze(0).permute(0, 3, 1, 2)
        img /= 255
        inputimg = img
        fanyue_pic(img_org_last, img_org, inputimg, model, wallPoints,
                   thresh_person, inter_ratio, device='cuda:0')
        t2 = time.time()
        # print(t2 - t1)
        time.sleep(1)
        img_org_last = frame
