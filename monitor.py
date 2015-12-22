# -*- coding: UTF-8 -*-

import os
import sys
import time
import mmail
import ConfigParser


host = open('/etc/hostname').read().strip('\n')
# host = 'liguangming\'s macbook pro'
config = '/var/www/nginx-default/operation/ServiceMonitor/conf.ini'


def CheckDiskCapacity(filesystem_list):
    for filesystem in filesystem_list:
        cmd = "df -h | grep " + filesystem + " | awk '{print $5}'"
        output = os.popen(cmd)
        outStr = output.read()
        if outStr == '':
            print('[ERROR]THE FILESYSTEM [' + filesystem + '] IS NOT EXIST!')
            mmail.send_mail_with_files('THE FILESYSTEM [' + filesystem + '] IS NOT EXIST! CHECK IT AS SOON AS YOU CAN! From: ' + host)
            return
        percentage = int(outStr.replace('%','').replace('\r', '').replace('\n', ''))
        output.close()
        if percentage >= 90:
            print('[ERROR]THE FILESYSTEM [' + filesystem + '] IS FULL!')
            mmail.send_mail_with_files('THE FILESYSTEM [' + filesystem + '] IS FULL! CHECK IT AS SOON AS YOU CAN! From: ' + host)
            pass
        elif percentage >= 80 and percentage < 90:
            print('[WARNING]The filesystem [' + filesystem + '] will be full!')
            mmail.send_mail_with_files('The filesystem [' + filesystem + '] will be full. Please delete some file. ' + host)
            pass
        else:
            # it's ok
            print('[INFO]Check disk capacity, all right. Percentage is: ' + str(percentage) + '%.')
            sys.stdout.flush()
            pass
        pass
    pass

def CheckService(process_list):
    output = os.popen("ps aux")
    outStr = output.read()
    output.close()

    for process in process_list:
        process_name = process[0]
        x = outStr.find(process_name)

        if x > 0:
            print("[INFO]process " + process_name + " is alive.")
            sys.stdout.flush()
        else:
            subject = "IDC process " + process_name + " was dead."
            print("[ERROR]process " + process_name + " was dead.")
            sys.stdout.flush()

            logs = process[1].replace(' ', '').split(',')
            mmail.send_mail_with_files(subject + ' ' + host, logs)

            os.system('service ' + process_name + ' restart')
            print("[ERROR]process " + process_name + " was restarted.")
            sys.stdout.flush()
            pass
        pass
    pass

if __name__ == "__main__": 
    cf = ConfigParser.ConfigParser()
    cf.read(config)

    time_sleep = int(cf.get('loop', 'time'))
    process_list = cf.items("monitor")
    filesystem_list = cf.get('disk','filesystem').split(',')

    while True:
        # print time
        t = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        print('[Time]' + t)
        sys.stdout.flush()

        # check service
        CheckService(process_list)

        # check the capacity of hard disk
        CheckDiskCapacity(filesystem_list)

        time.sleep(time_sleep)
