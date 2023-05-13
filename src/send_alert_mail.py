import smtplib
from email.mime.text import MIMEText


def create_message(sender_email, receiver_email, subject, message):
    """构造邮件对象

    :param sender_email:
    :param receiver_email:
    :param subject:
    :param message:
    :return:
    """
    # 构建 MIMEText 对象
    msg = MIMEText(message, 'plain')

    # 设置邮件头部信息
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    return msg


def send_email(sender_email, receiver_email, msg, smtp_server, smtp_port, username, password):
    """发送邮件

    :param sender_email:
    :param receiver_email:
    :param msg:
    :param smtp_server:
    :param smtp_port:
    :param username:
    :param password:
    :return:
    """
    try:
        # 创建 SMTP 连接
        server = smtplib.SMTP(smtp_server, smtp_port)

        # 开启 TLS 加密
        server.starttls()

        # 登录 SMTP 服务器
        server.login(username, password)

        # 发送邮件
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败:', str(e))
    finally:
        # 关闭 SMTP 连接
        server.quit()


def send_alert_email(sender_email, receiver_email, subject, message, smtp_server='smtp.qq.com', smtp_port=587,
                     username=None, password=None):
    """入口函数

    :return:
    """
    # 创建邮件
    msg = create_message(sender_email, receiver_email, subject, message)

    # 发送邮件
    send_email(sender_email, receiver_email, msg, smtp_server, smtp_port, username, password)


# 调用函数发送警报邮件
if __name__ == '__main__':
    send_alert_email()
