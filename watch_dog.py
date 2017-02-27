# -*- coding: utf-8 -*-
import time
import json

import arrow
import requests

from sqlitedb import KakouDB
from helper_ping import Ping
from helper_sms import SMS
from ini_conf import MyIni
from my_logger import *


debug_logging(u'logs/error.log')
logger = logging.getLogger('root')


class WatchDog(object):
    def __init__(self):
	# 时间标记
        self.time_flag = arrow.now().replace(hours=-1)

        self.my_ini = MyIni()
        
        self.sms = SMS(**self.my_ini.get_sms())
        self.p = Ping(**self.my_ini.get_ping())
	self.sq = KakouDB()
	
	# 设备状态字典 {'127.0.0.1': '2017-02-03 12:00:00'}
        self.device_status_dict = {}
        # 短信发送记录，形如{('441302001', 'IN'): <Arrow [2016-03-02T20:08:58.190000+08:00]>}
        self.mobiles_list = []
	self.send_time_step = 12

    def __del__(self):
        pass

    def get_device_ip_dict(self):
        """IP地址列表"""
	device_dict = {}
        device_list = self.sq.get_device()
	for i in device_list:
	    device_dict[i[1]] = {'ip': i[1], 'type': i[2], 'application': i[3], 'ps': i[4]}
	return device_dict

    def sms_send_info(self, sms_send_list):
        """发送短信通知"""
	if sms_send_list == []:
	    return
        t = arrow.now()
        content = u'[设备状态报警]\n'
        for i in sms_send_list:
            content += u'[{0}={1}]\n'.format(
                i['ip'], i['type'])
        content += u'连接超时'

        self.sms.sms_send(content, self.mobiles_list)


    def device_status_check(self):
	""""设备状态检测"""
	device_dict = self.get_device_ip_dict()
	device_miss_dict = {}
	for i in device_dict.keys():
	    r = self.p.get_ping(i)
	    if r['connect'] is False:
	    	device_miss_dict[i] = device_dict[i]

	if len(device_miss_dict.keys()) > 0:
	    for i in device_miss_dict.keys():
		if self.is_device_status(i) is True:
		    del device_miss_dict[i]

	sms_send_list = []
	if len(device_miss_dict.keys()) > 0:
	    for i in device_miss_dict.keys():
		t = self.device_status_dict.get(i, None)
		if t is None:
		    self.device_status_dict[i] = arrow.now()
		    sms_send_list.append(device_miss_dict[i])
		    continue
		if t.replace(hours=self.send_time_step) < arrow.now():
		    self.device_status_dict[i] = arrow.now()
		    sms_send_list.append(device_miss_dict[i])
	if len(sms_send_list) > 0:
	    self.sms_send_info(sms_send_list)

    def is_device_status(self, ip, loop=3):
	"""设备状态重新检测"""
	for i in range(loop):
	    r = self.p.get_ping(ip)
	    if r['connect'] is True:
		return True
	return False

        
    def run(self):
	print 'start run'
        while 1:
            try:
                # 当前时间
                t = arrow.now()
                # 每30秒检查一遍
                if t > self.time_flag.replace(seconds=30):
                    self.device_status_check()
                    self.time_flag = t
            except Exception as e:
                logger.exception(e)
                time.sleep(10)
            finally:
                time.sleep(1)

if __name__ == "__main__":
    wd = WatchDog()
    #wd.get_ip_list()
    wd.device_status_check()
