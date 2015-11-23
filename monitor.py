# -*- coding: UTF-8 -*-

# 作用
# ----
# 监控服务器服务进程，如果进程挂了，则发出邮件通知运维团队。

import os
import sys
import time
import json
import mmail

process_list = json.loads(
    '[{"name":"vlink", "log":"/var/log/vlink/access.log"},\
    {"name":"teleport", "log":"/var/log/teleport/teleport.log"},\
    {"name":"surveillance", "log":"/var/log/surveillance/access.log, /var/log/surveillance/surveillance.log"},\
    {"name":"apn-publish", "log":"/var/log/apn/access.log"}]')

host = open('/etc/hostname').read().strip('\n')

while True:
    t = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    print('[time]' + t)
    sys.stdout.flush()

    output = os.popen('ps aux')
    outStr = output.read()
    output.close()

    for process in process_list:
        process_name = process["name"]
        x = outStr.find(process_name)

        if x > 0:
            print("[info]process " + process_name + " is alive.")
            sys.stdout.flush()
        else:
            subject = "IDC process " + process_name + " was dead."
            print("[error]process " + process_name + " was dead.")
            sys.stdout.flush()

            logs = process["log"].split(',')
            mmail.send_mail_with_files(subject + ' ' + host, logs)

            os.system('service ' + process_name + ' restart')
            print("[debug]process " + process_name + " was restarted.")
            sys.stdout.flush()

    time.sleep(10)
