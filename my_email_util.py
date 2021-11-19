from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from utils import get_data
import requests


def one() -> str:
    """
    获取一条一言。
    :return:
    """
    try:
        url = "https://v1.hitokoto.cn/"
        res = requests.get(url).json()
        return res["hitokoto"] + "    ----" + res["from"]
    except requests.exceptions.ConnectionError:
        return ""


def sendMail(message, subject, to_addres=None, from_show='lustime', to_show='lbb', cc_show=None):
    """
    :param message: str 邮件内容
    :param subject: str 主题
    :param from_show: str 发件人显示
    :param to_show: str 收件人显示
    :param cc_show: str 抄送人显示
    :param to_addres: str 实际收件人
    :return:
    """

    data = get_data()
    mail = data.get('MAIL')
    user = mail.get('user')
    password = mail.get('password')
    if to_addres is None:
        to_addres = mail.get('toAddres')
    hitokoto = data.get('HITOKOTO')
    text = one() if hitokoto else ''
    message += '\n\n' + text
    msg = MIMEText(message, 'plain', _charset="utf-8")
    msg["Subject"] = subject
    msg["from"] = from_show
    msg["to"] = to_show
    msg["Cc"] = cc_show
    with SMTP_SSL(host="smtp.qq.com", port=465) as smtp:
        smtp.login(user=user, password=password)
        smtp.sendmail(from_addr=user, to_addrs=to_addres.split(','), msg=msg.as_string())
        smtp.quit()
    print('邮件通知完成')


if __name__ == '__main__':
    message = 'Python 测试邮件...'
    Subject = '主题测试'
    sendMail(message, Subject, to_show='ailulu')
