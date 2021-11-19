from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from utils import get_data


def sendMail(message, subject, to_addres, from_show, to_show, cc_show=''):
    '''
    :param message: str 邮件内容
    :param subject: str 主题
    :param from_show: str 发件人显示
    :param to_show: str 收件人显示
    :param cc_show: str 抄送人显示
    :param to_addres: str 实际收件人
    :return:
    '''

    data = get_data()
    mail = data.get('MAIL')
    user = mail.get('user')
    password = mail.get('password')
    if len(to_addres) == 0:
        to_addres = data.get('mailToAddres')
    if len(from_show) == 0:
        from_show = 'lustime'
    if len(to_show) == 0:
        to_show = 'lbb'
    msg = MIMEText(message, 'plain', _charset="utf-8")
    msg["Subject"] = subject
    msg["from"] = from_show
    msg["to"] = to_show
    msg["Cc"] = cc_show
    with SMTP_SSL(host="smtp.exmail.qq.com", port=465) as smtp:
        smtp.login(user=user, password=password)
        smtp.sendmail(from_addr=user, to_addrs=to_addres.split(','), msg=msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    message = 'Python 测试邮件...'
    Subject = '主题测试'
    # 显示发送人
    sender_show = 'ailulu'
    # 显示收件人
    recipient_show = 'lbb'
    # 实际发给的收件人
    to_addrs = 'lumin_sn@126.com'
    sendMail(message, Subject, to_addrs, sender_show, recipient_show)
