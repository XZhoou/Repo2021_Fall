import smtplib
from email.mime.text import MIMEText
from email.header import Header
from functools import wraps

sender = '2836072921@qq.com'  # 发送邮件的以预防
receiver = 'buaasqh@163.com'  # 接收邮件的一方
password = 'mfzmucycdhqhdeia'  # QQ邮箱的授权码
smtp_server = 'smtp.qq.com'


def send_email_func():
    msg = MIMEText('您的程序已执行完毕，请及时查看结果！\n\n这是系统自动发出邮件，请不要回复。', 'plain', 'utf-8')
    msg['From'] = u'孙小舟 <2836072921@qq.com>'
    msg['To'] = u'<buaasqh@163.com>'
    msg['Subject'] = u'您的程序已经执行完毕'
    server = smtplib.SMTP_SSL(smtp_server)
    server.set_debuglevel(1)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()


class SendEmailClass:
    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                send_email_func()
                #每次程序运行结束之后向我的邮箱发送一封提醒邮件
            except Exception as e:
                print(e)
        return wrapper
