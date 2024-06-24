import cv2

import torch
import time

from models.experimental import attempt_load
from utils.general import non_max_suppression

from shapely.geometry import Polygon

import numpy as np

#加载模型
def load_detector(model_path,device = 'cpu'):

    model = attempt_load(model_path, device)
    model.eval()
    return model







#推理然后判断是否和墙有交集
def chaoxian_pic(imgs,  model, multipolyPoints,thresh_person,thresh_num, inter_ratio,device='cpu'):

    # 前向传播
    #while 1:

    pred = model(imgs)[0] # 前向传播，只获取预测结果（因为我们只预测一张图片）

    # 非极大值抑制（NMS）
    pred = non_max_suppression(pred, conf_thres=thresh_person, iou_thres=0.5)  # 你可以调整 conf_thres 和 iou_thres

    # condition = pred[:, -1] == 0
    # # 使用布尔索引来选择满足条件的行
    # pred = pred[condition]
    #解析预测结果

    for i in range(len(pred)):
        picpred = pred[i]
        condition = picpred[:, -1] == 0
        # 使用布尔索引来选择满足条件的行
        picpred = picpred[condition]
        #polyPoints = multipolyPoints[i]
        for det in picpred:  # det 是一个列表，每个元素是一个字典，表示一个检测到的物体
            if len(det.cpu().numpy()) >= thresh_num:
                print("chao xian")

    # cv2.imshow('fuck',img_org)
    # cv2.waitKey(0)
            # 这里可以根据你的需要添加更多逻辑，比如绘制边界框等
            # 368 180     460 536



def set_mask(img,polyPoints1):

    img1 = img
    #img1 = cv2.imread('friday.png')

    height, width, _ = img1.shape

    # 创建一个与图片大小相同的掩码，初始化为全零（黑色）
    mask = np.zeros((height, width), dtype=np.uint8)

    # 在掩码上绘制多边形区域，设置为白色（即255）
    cv2.fillPoly(mask, polyPoints1, (255, 255, 255))

    # 如果图片是RGBA格式的，并且你想保持透明度，则需要在RGBA掩码上进行操作
    # 否则，直接使用下面的按位与操作将非多边形区域置零

    # 使用掩码将图片中非多边形区域置零
    # 如果图片是BGR格式的
    result = cv2.bitwise_and(img1, img1, mask=mask)


    return result


if __name__ == '__main__':
    img_org = cv2.imread('friday.png')
    img = cv2.resize(img_org, (640, 640), interpolation=cv2.INTER_LINEAR)
    polyPoints1 = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 100)]
    polyPoints2 = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 60)]
    polyPoints3 = [(300, 100), (300, 400), (400, 400), (500, 380), (400, 60)]
    # polyPoints = [polyPoints1,polyPoints2]
    polyPoints1 = np.array([polyPoints1], dtype=np.int32)
    polyPoints2 = np.array([polyPoints2], dtype=np.int32)
    polyPoints3 = np.array([polyPoints3], dtype=np.int32)
    multipolyPoints = [polyPoints1, polyPoints2,polyPoints2]
    thresh_person = 0.25
    inter_ratio = 0.05

    model = load_detector('yolov5s.pt', device='cuda:0')

    img1 = set_mask(img, polyPoints1)
    # cv2.imshow('fuck1', img1)
    # cv2.waitKey(0)
    img1 = torch.from_numpy(img1).to('cuda:0')
    img1 = img1.float()  # uint8 to fp16/32
    img1 /= 255
    img1 = img1.unsqueeze(0).permute(0,3,1,2)  # 添加批次维度，因为我们只预测一张图片


    img2 = set_mask(img, polyPoints2)
    # cv2.imshow('fuck2', img2)
    # cv2.waitKey(0)
    img2 = torch.from_numpy(img2).to('cuda:0')
    img2 = img2.float()  # uint8 to fp16/32
    img2 /= 255
    img2 = img2.unsqueeze(0).permute(0, 3, 1, 2)  # 添加批次维度，因为我们只预测一张图片


    img3 = set_mask(img, polyPoints3)
    # cv2.imshow('fuck2', img2)
    # cv2.waitKey(0)
    img3 = torch.from_numpy(img3).to('cuda:0')
    img3 = img3.float()  # uint8 to fp16/32
    img3 /= 255
    img3 = img3.unsqueeze(0).permute(0, 3, 1, 2)  # 添加批次维度，因为我们只预测一张图片


    imgs = torch.cat((img1, img2,img3), dim=0)

    thresh_num =1

    while 1:
        t1 = time.time()

        inputimg = imgs

        chaoxian_pic(inputimg, model, multipolyPoints, thresh_person, thresh_num,inter_ratio,device='cuda:0')
        t2 = time.time()
        print(t2 - t1)
        time.sleep(3)