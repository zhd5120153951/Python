

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

#加载模型
def load_detector(model_path,device = 'cpu'):

    model = attempt_load(model_path, device)
    model.eval()
    return model





def calculate_intersection_ratio(polygon_a_vertices, polygon_b_vertices):
    # 创建多边形A和B的shapely对象
    polygon_a = Polygon(polygon_a_vertices)
    polygon_b = Polygon(polygon_b_vertices)

    # 计算交集多边形C
    #intersection_polygon = intersection(polygon_a, polygon_b)
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

#推理然后判断是否和墙有交集
def fanyue_pic(imgs,  model, wallPoints,thresh_person, inter_ratio,device='cpu'):

    # 前向传播
    #while 1:

    pred = model(imgs)[0] # 前向传播，只获取预测结果（因为我们只预测一张图片）

    # 非极大值抑制（NMS）
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.5)  # 你可以调整 conf_thres 和 iou_thres

    # condition = pred[:, -1] == 0
    # # 使用布尔索引来选择满足条件的行
    # pred = pred[condition]
    # 解析预测结果
    for det in pred[0]:  # det 是一个列表，每个元素是一个字典，表示一个检测到的物体
        per = det.cpu().numpy()
        x1,y1,x2,y2,score,cls = per
        x1, y1, x2, y2 = int(x1),int(y1),int(x2),int(y2)
        if score > thresh_person and cls == 0:
            #polygon_a_vertices = wallPoints
            polygon_person = [(x1,y1),(x1,y2),(x2,y2),(x2,y1)]
            ratio = calculate_intersection_ratio(wallPoints, polygon_person)
            print(per)
            print(ratio)
            cv2.rectangle(img_org, (x1,y1), (x2,y2), (255, 0, 0), 3)
            for i in range(len(wallPoints)-1):
                cv2.line(img_org,wallPoints[i],wallPoints[i+1], (255, 255, 0), 5)
            cv2.line(img_org, wallPoints[0], wallPoints[- 1], (255, 255, 0), 5)

    # cv2.imshow('fuck',img_org)
    # cv2.waitKey(0)
            # 这里可以根据你的需要添加更多逻辑，比如绘制边界框等
            # 368 180     460 536








if __name__ == '__main__':
    img = cv2.imread('friday.png')
    img = cv2.resize(img, (640, 640), interpolation=cv2.INTER_LINEAR)
    wallPoints = [(300, 100), (300, 400), (400, 400),(500,380) ,(400, 100)]
    print(wallPoints[0])
    polygon_a_vertices = '[(0, 0), (1, 0), (1, 1), (0, 1)]'
    polygon_a_vertices.strip()
    print(polygon_a_vertices)
    polygon_b_vertices = '[(0.5, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5)]'

    thresh_person = 0.25
    inter_ratio = 0.05

    model = load_detector('yolov5s.pt', device='cuda:0')

    img_org = img
    img = torch.from_numpy(img).to('cuda:0')
    img = img.float()  # uint8 to fp16/32
    img /= 255

    img = img.unsqueeze(0).permute(0,3,1,2)  # 添加批次维度，因为我们只预测一张图片
    imgs = img.repeat(64,1, 1, 1)
    # rtsp = ''
    # cap = cv2.VideoCapture(rtsp)
    while True:
        t1 = time.time()

        inputimg = imgs

        # ret, frame = cap.read()
        # img = cv2.resize(imgs, (640, 640), interpolation=cv2.INTER_LINEAR)
        # img = torch.from_numpy(img).to('cuda:0')
        # img = img.float()  # uint8 to fp16/32
        # img /= 255

        fanyue_pic(inputimg, model, wallPoints, thresh_person, inter_ratio,device='cuda:0')
        t2 = time.time()
        print(t2 - t1)
        #time.sleep(3)