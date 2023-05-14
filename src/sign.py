import requests
from datetime import date
import yaml
from send_alert_mail import send_alert_email


def auto_sign(url="https://glados.network/api/user/checkin", cookie=None, proxies=None):
    """自动签到函数

    :param url:
    :param cookie:
    :param proxies:
    :return:
    """
    if cookie is None:
        assert Exception("Not cookie! Please add.")

    if proxies is None:
        proxies = proxies
    headers = {
        'authority': 'glados.network',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
    }
    # 添加post的表单数据 仅有token
    data = {
        'token': 'glados.network'
    }
    # 发送POST请求
    response = requests.post(
        url,
        proxies=proxies,
        headers=headers,
        data=data
    )
    return response


if __name__ == '__main__':
    # 解析配置文件
    with open("../config.yaml", encoding="UTF-8") as f:
        CONFIG = yaml.safe_load(f)

    response = auto_sign(url=CONFIG["URL"], cookie=CONFIG["COOKIE"], proxies=CONFIG["PROXIES"])
    # 查看状态码（200为正确）和响应内容
    print(f'状态码：{response.status_code}')
    print(response.text)

    # 假如状态码为200 说明已经签到成功
    if response.status_code == 200:
        today = date.today()
        today_str = today.strftime("%Y.%m.%d")
        print(f'[{today_str}] 已签到成功！')
    else:
        # 假如状态码不是200，则邮件报警，内容就是response.text
        if CONFIG["ENABLE_ALERT_MAIL"]:
            send_alert_email(CONFIG["SENDER_EMAIL"], CONFIG["RECEIVER_EMAIL"], subject=CONFIG["SUBJECT"],
                             message=f"签到失败，[状态码]：{response.status_code}，[响应]: {response.text}，请查看网站检查：{CONFIG['URL']}", smtp_server=CONFIG["SMTP_SERVER"],
                             smtp_port=CONFIG["SMTP_PORT"],
                             username=CONFIG["USERNAME"], password=CONFIG["PASSWORD"])
