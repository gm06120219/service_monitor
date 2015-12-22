# -*- coding: UTF-8 -*-
#!/usr/bin/env Python

import os
import smtplib
import ConfigParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

config = '/var/www/nginx-default/operation/ServiceMonitor/conf.ini'

cf = ConfigParser.ConfigParser()
cf.read(config)

mail_to = cf.get("mail", "mail_to").split(",")
mail_host = cf.get("mail", "mail_host")
mail_user = cf.get("mail", "mail_user")
mail_pass = cf.get("mail", "mail_pass")
mail_postfix = cf.get("mail", "mail_postfix")


def send_mail(subject, filename=None):
    to_list = mail_to
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
    to_list = mail_to
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
        content = content + ' no attachment.'
        pass

    print(content)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ";".join(to_list)


    if files != None:
        for file in temp_file_list:
            file = file.strip()
            f = open(file, 'r')
            fx = MIMEApplication(f.read())
            f.close()
            fx.add_header(
                'Content-Disposition', 'attachment', filename=os.path.basename(file))
            msg.attach(fx)
            pass
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
        print "send mail success."
    else:
        print "send mail failure"
