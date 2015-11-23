# -*- coding: UTF-8 -*-

import os
import sys
import time
import mmail
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("/var/www/nginx-default/operation/ServiceMonitor/conf.ini")

process_list = cf.items("monitor")

host = open('/etc/hostname').read().strip('\n')

while True:
    t = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
    print('[time]' + t)
    sys.stdout.flush()

    output = os.popen('ps aux')
    outStr = output.read()
    output.close()

    for process in process_list:
        process_name = process[0]
        x = outStr.find(process_name)

        if x > 0:
            print("[info]process " + process_name + " is alive.")
            sys.stdout.flush()
        else:
            subject = "IDC process " + process_name + " was dead."
            print("[error]process " + process_name + " was dead.")
            sys.stdout.flush()

            logs = process[1].split(',')
            mmail.send_mail_with_files(subject + ' ' + host, logs)

            os.system('service ' + process_name + ' restart')
            print("[debug]process " + process_name + " was restarted.")
            sys.stdout.flush()

    time.sleep(10)
