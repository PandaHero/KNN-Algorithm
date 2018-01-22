#coding:utf8
#author:xiejiahong 149172415@qq.com
from base_param import baseParam
import json

class userParam(baseParam):


    def __init__(self):
        baseParam.__init__(self)


    def getJson(self):
        return json.dumps(self.params)

