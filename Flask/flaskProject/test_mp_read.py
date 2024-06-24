import multiprocessing as mp
import cv2
import time

# 定义一个函数，用于处理每一路RTSP流的消费端


def consumer(rtsp_stream, queue):
    while True:
        if queue.qsize() == 0:
            time.sleep(1/30)
            continue
        # 从队列中获取帧
        frame = queue.get()

        # 在这里可以进行图像处理，例如显示图像
        cv2.imshow(rtsp_stream, frame)
        # 按'q'退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

# 定义一个函数，用于处理每一路RTSP流的产生端


def producer(rtsp_stream, queue):
    cap = cv2.VideoCapture(rtsp_stream, cv2.CAP_FFMPEG)
    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            # 如果读取失败，则结束这一路的生产
            break
        # 将帧放入队列中
        queue.put(frame)
        if queue.qsize() > 2:
            queue.get()
        # 控制生产速度，例如每秒一张图
        time.sleep(1/30)
    cap.release()

# 主函数，用于启动进程


def main(rtsp_streams):
    # 创建64个队列
    queues = [mp.Queue(2) for _ in range(len(rtsp_streams))]

    # 启动19个生产进程
    producer_processes = []
    # rtsp_streams是一个包含19个RTSP流的列表
    for i, rtsp_stream in enumerate(rtsp_streams):
        p = mp.Process(
            target=producer, args=(rtsp_stream, queues[i]))
        p.start()
        producer_processes.append(p)

    # 启动19个消费进程
    consumer_processes = []
    for i, rtsp_stream in enumerate(rtsp_streams):
        cp = mp.Process(
            target=consumer, args=(rtsp_stream, queues[i]))
        cp.start()
        consumer_processes.append(cp)

    # 等待所有生产进程结束
    for p in producer_processes:
        p.join()
    # 等待消费进程结束
    for p in consumer_processes:
        p.join()


if __name__ == '__main__':
    rtsp_streams = [
        'rtsp://admin:jiankong123@192.168.23.17:554/cam/realmonitor?channel=1&subtype=0',
        'rtsp://admin:jiankong123@192.168.23.19:554/cam/realmonitor?channel=1&subtype=0'

    ]
    main(rtsp_streams)

# 'rtsp://admin:jiankong123@192.168.23.20:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.22:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.23:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.24:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.25:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.26:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.27:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.31:554/cam/realmonitor?channel=1&subtype=0',
# 'rtsp://admin:jiankong123@192.168.23.10:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.11:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.12:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.13:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.14:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.15:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.16:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.17:554/Streaming/Channels/101',
# 'rtsp://admin:jiankong123@192.168.23.18:554/Streaming/Channels/101'
