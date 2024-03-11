import cv2

if __name__ == "__main__":
    cap = cv2.VideoCapture(
        "rtsp://admin:hik123456@192.168.1.201:554/h264")
    winname = "test"
    # 创建一个窗口来显示视频流
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    while True:
        # 读取视频帧
        ret, frame = cap.read()

        if not ret:
            break
        # 实时显示视频帧
        cv2.imshow(winname, frame)
        # 按下esc键退出预览
        # if cv2.waitKey(1) == 27:
        #     break

        # 点击窗口X按钮退出预览
        cv2.waitKey(1)
        if cv2.getWindowProperty(winname, cv2.WND_PROP_VISIBLE) < 1:
            break
    # 释放视频流和关闭窗口
    cap.release()
    cv2.destroyAllWindows()
