'''
@FileName   :pool.py
@Description:进程池任务形式开辟，然后每个进程开辟两个子线程，一个拉流解码，一个取图显示
@Date       :2024/06/17 16:41:14
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import cv2
import multiprocessing
import threading
from queue import Queue


def rtsp_reader(rtsp_url, queue):
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if not queue.full():
            queue.put(frame)
        else:
            queue.get()
    cap.release()


def frame_display(queue):
    while True:
        if not queue.empty():
            frame = queue.get()
            cv2.imshow('RTSP Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()


def process_task(rtsp_url):
    queue = Queue(maxsize=10)
    reader_thread = threading.Thread(
        target=rtsp_reader, args=(rtsp_url, queue))
    display_thread = threading.Thread(target=frame_display, args=(queue,))

    reader_thread.start()
    display_thread.start()

    reader_thread.join()
    display_thread.join()


def main():
    # Replace with actual RTSP URLs
    rtsp_urls = [
        'rtsp://admin:jiankong123@192.168.23.17:554/cam/realmonitor?channel=1&subtype=0',
        'rtsp://admin:jiankong123@192.168.23.19:554/cam/realmonitor?channel=1&subtype=0']
    pool_size = 8
    processes = []

    with multiprocessing.Pool(pool_size) as pool:
        for i in range(pool_size):
            print(i)
            # Assign RTSP URLs round-robin
            rtsp_url = rtsp_urls[i % len(rtsp_urls)]
            process = pool.apply_async(process_task, (rtsp_url,))
            processes.append(process)

        for process in processes:
            process.get()


if __name__ == '__main__':
    main()
