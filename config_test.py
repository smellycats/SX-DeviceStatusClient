#-*- encoding: utf-8 -*-
from ini_conf import MyIni
from my_yaml import MyYAML


class ConfigTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        
    def test_sms(self):
        print self.my_ini.get_sms()
    def test_ping(self):
        print self.my_ini.get_ping()

class TestYAML(object):
    def __init__(self):
        self.my_ini = MyYAML()
        
    def get_ini(self):
        print self.my_ini.get_ini()

    def set_ini(self):
        data = self.my_ini.get_ini()
        data['ping']['test'] = u'马刺'
        print self.my_ini.set_ini(data) 



if __name__ == "__main__":
    #ct = ConfigTest()
    #ct.test_sms()
    #ct.test_ping()
    ty = TestYAML()
    print ty.get_ini()
    #ty.set_ini()
