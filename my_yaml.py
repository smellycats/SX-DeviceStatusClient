#-*- encoding: utf-8 -*-
#from __future__ import print_function

import ruamel.yaml


class MyYAML(object):
    def __init__(self, path = 'my.yaml'):
        self.path = path
        self.f = open(path, 'r')

    def __del__(self):
        self.f.close()

    def get_ini(self):
        return ruamel.yaml.load(stream=self.f,
                                Loader=ruamel.yaml.RoundTripLoader)

    def set_ini(self, data):
        f = open(self.path, 'w')
        ruamel.yaml.dump(data, stream=f, Dumper=ruamel.yaml.RoundTripDumper,
                         default_flow_style=False, allow_unicode=True)
        f.close()
