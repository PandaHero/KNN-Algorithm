#coding:utf8
#author:xiejiahong 149172415@qq.com

class baseParam(object):
    def __init__(self):
        self.params = {}

    def set_param(self, param_key, param_value):
        self.params[param_key] = param_value