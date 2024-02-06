import asyncio
import aiohttp
import smtplib
import queue
from email.mime.text import MIMEText


async def send_email(subject, body, to_address, from_address, password):
    # 设置邮件内容
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    # 连接SMTP服务器并登录
    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_address, password)

    # 发送邮件
    try:
        await server.sendmail(from_address, to_address, msg.as_string())
        print(f"邮件发送成功至：{to_address}")
    except Exception as e:
        print(f"邮件发送失败至：{to_address}")
        print(f"错误信息：{str(e)}")

    # 关闭连接
    server.quit()


async def email_worker(email_queue):
    while True:
        to_address, subject, body = await email_queue.get()

        # 使用异步发送邮件
        await send_email(subject, body, to_address, from_address, password)

        email_queue.task_done()

if __name__ == "__main__":
    # 发送人邮箱和密码
    from_address = "your_email@qq.com"
    password = "your_password"

    # 创建异步邮件队列
    email_queue = asyncio.Queue()

    # 创建协程来处理发送邮件
    asyncio.create_task(email_worker(email_queue))

    # 邮件内容
    subject = "测试邮件"
    body = "这是一封测试邮件，请忽略！"

    # 添加要发送的邮件到队列
    to_address = "receiver1_email@qq.com"
    email_queue.put_nowait((to_address, subject, body))

    to_address = "receiver2_email@qq.com"
    email_queue.put_nowait((to_address, subject, body))

    # 运行事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(email_queue.join())
    loop.close()
