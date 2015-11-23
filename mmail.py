# -*- coding: UTF-8 -*-
#!/usr/bin/env Python

import os
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

mailto_list = ["mailto@stmp.com"]
# mail_host = "smtp.163.com"  # 设置服务器
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "noreply"  # 用户名
mail_pass = "**********"  # 口令
mail_postfix = "vlintech.com"  # 发件箱的后缀


def send_mail(subject, filename=None):
    to_list = mailto_list
    me = mail_user + "@" + mail_postfix
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    if filename != None and os.path.exists(filename):
        f = open(filename, 'r')
        fx = MIMEApplication(f.read())
        f.close()
        fx.add_header(
            'Content-Disposition', 'attachment', filename=os.path.basename(filename))
        msg.attach(fx)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(me, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def send_mail_with_files(subject, files=None):
    to_list = mailto_list
    me = mail_user + "@" + mail_postfix
    content = ''

    if files != None:
        temp_file_list = []

        for file in files:
            if (os.path.exists(file.strip())):
                temp_file_list.append(file)
                pass
            else:
                content = content + file + " doesn't exist."
                pass
            pass

    else:
        content = content + 'no attachment.'
        pass

    print(content)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)


    for file in temp_file_list:
        file = file.strip()
        f = open(file, 'r')
        fx = MIMEApplication(f.read())
        f.close()
        fx.add_header(
            'Content-Disposition', 'attachment', filename=os.path.basename(file))
        msg.attach(fx)
        pass
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(me, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


pass


if __name__ == "__main__":
    if send_mail_with_files("test2", ["/Users/liguangming/Desktop/3.txt", "/Users/liguangming/Desktop/2.txt"]):
        print "发送成功！"
    else:
        print "发送失败！"
