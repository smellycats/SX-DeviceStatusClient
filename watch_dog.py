# -*- coding: utf-8 -*-
import time
import json
import multiprocessing as mul

import arrow

from helper_ping import *
from helper_device import Device
from my_yaml import MyYAML
from my_logger import *


debug_logging(u'logs/error.log')
logger = logging.getLogger('root')


class WatchDog(object):
    def __init__(self):
        ini = MyYAML()
        self.my_ini = ini.get_ini()
        self.dev = Device(**dict(self.my_ini['device']))
        # 进程池
        self.pool = mul.Pool(8)
        # 循环检测次数
        self.loop = self.my_ini['loop']

    def __del__(self):
        pass

    def mul_ping(self, dev_list):
        """多进程ping"""
        dev_true_list = []
        dev_false_list = []
        rel = self.pool.map(ping, [i['ip'] for i in dev_list])
        for i, j in zip(dev_list, rel):
            i['res'] = j
            if j is True:
                dev_true_list.append(i)
                continue
            if j is False and i['status'] is False:
                dev_true_list.append(i)
                continue
            dev_false_list.append(i)

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
        dev_info_list = self.dev.get_device_check(num=8, type=type)['items']
        if len(dev_info_list) == 0:
            return
        for i in range(self.loop):
            dev_true_list, dev_false_list = self.mul_ping(dev_info_list)
            self.set_device_status(
                [{'id': i['id'], 'ip': i['ip'],
                  'status': i['res']} for i in dev_true_list])
            if len(dev_false_list) == 0:
                break
            dev_info_list = dev_false_list
        self.set_device_status(
            [{'id': i['id'], 'ip': i['ip'],
              'status': i['res']} for i in dev_false_list])

    def run(self):
        while 1:
            try:
                self.device_status_check(1)
                time.sleep(1)
            except Exception as e:
                logger.error(e)
                time.sleep(15)


if __name__ == "__main__":
    wd = WatchDog()
    #wd.get_ip_list()
    t = time.time()
    wd.device_status_check(1)
    t2 = time.time()
    print t2 - t
