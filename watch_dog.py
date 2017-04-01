# -*- coding: utf-8 -*-
import time
import json

import arrow

from helper_ping import Ping
from helper_device import Device
from my_yaml import MyYAML
from my_logger import *


debug_logging(u'logs/error.log')
logger = logging.getLogger('root')


class WatchDog(object):
    def __init__(self):
        ini = MyYAML()
        self.my_ini = ini.get_ini()
        self.p = Ping(**dict(self.my_ini['ping']))
        self.p.base_path = ''
        self.dev = Device(**dict(self.my_ini['device']))

        self.loop = 3

    def __del__(self):
        pass

    def mul_ping(self, dev_list):
        """多进程ping"""
        dev_true_list = []
        dev_false_list = []
        rel = []
        for i in dev_list:
            r = self.p.get_ping(i['ip'])
            rel.append(r['connect'])
        for i, j in zip(dev_list, rel):
            if j is True:
                dev_true_list.append(
                    {'id': i['id'], 'ip': i['ip'], 'status': True})
                continue
            if j is False and i['status'] is False:
                dev_true_list.append(
                    {'id': i['id'], 'ip': i['ip'], 'status': False})
                continue
            dev_false_list.append(
                {'id': i['id'], 'ip': i['ip'], 'status': False})

        return dev_true_list, dev_false_list


    def set_device_status(self, dev_list):
        """更新设备状态"""
        if len(dev_list) > 0:
            self.dev.set_device(dev_list)
            for i in dev_list:
                print '{0} {1} {2}'.format(
                    str(arrow.now()), i['ip'], i['status'])
                #logger.info('{0} {1}'.format(i['ip'], i['status']))


    def device_status_check(self, type):
        """"设备状态检测"""
        dev_true_list = []
        dev_false_list = self.dev.get_device_check(num=8, type=type)['items']
        print dev_false_list
        if len(dev_false_list) == 0:
            return
        for i in range(self.loop):
            dev_true_list, dev_false_list = self.mul_ping(dev_false_list)
            self.set_device_status(dev_true_list)
            if len(dev_false_list) == 0:
                break
        self.set_device_status(dev_false_list)
        
    def run(self):
        while 1:
            try:
                self.device_status_check(1)
                time.sleep(1)
            except Exception as e:
                print e
                logger.error(e)
                time.sleep(10)
            finally:
                time.sleep(1)

if __name__ == "__main__":
    wd = WatchDog()
    #wd.get_ip_list()
    wd.device_status_check(1)
