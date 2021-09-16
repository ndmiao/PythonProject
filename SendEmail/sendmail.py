# coding: utf-8
# Author：南岛鹋
# Blog: www.ndmiao.cn
# Date ：2021/5/30 13:29
# Tool ：PyCharm

from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import argparse

# 第三方SMTP服务
host_server = 'smtp.126.com'
# sender_qq为发件人的邮箱
sender_qq = '******@126.com'
# pwd为126邮箱的授权码
pwd = '*******'
# 发件人的邮箱
sender_qq_mail = '*****@126.com'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--receivers", default="", help="mail receivers")
    parser.add_argument("-s", "--subject", default="GitLab ci/cd", help="mail subject")
    parser.add_argument("-c", "--content", default="", help="mail body content")
    args = parser.parse_args()
    return args

def send_mail():
    try:
        # ssl登录
        smtp = SMTP_SSL(host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(0)
        smtp.ehlo(host_server)
        smtp.login(sender_qq, pwd)

        args = parse_args()
        # print(args)
        receivers = args.receivers.split(',')  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        to = list(set(receivers))
        print(to)

        mail_subject = args.subject
        mail_content = args.content
        msg = MIMEText(mail_content, 'html', 'utf-8')
        msg["Subject"] = Header(mail_subject, 'utf-8')
        msg["From"] = sender_qq_mail
        for i in to:
            msg['To'] = i
        smtp.sendmail(sender_qq_mail, to, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    if send_mail():
        print("发送成功")
    else:
        print("发送失败")