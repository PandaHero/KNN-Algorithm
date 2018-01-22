#coding:utf8
#author:xiejiahong 149172415@qq.com

from base_param import baseParam



class requestParam(baseParam):
    #系统级参数
    #API接口名称
    KEY_METHOD = "Method"

    #应用票据
    KEY_ACCESS_TOKEN = "AccessToken"

    #时间戳，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8
    KEY_TS = "Timestamp"

    #返回值格式。默认为xml格式，可选值：xml，json
    KEY_FORMAT = "Format"

    #API输入参数签名结果
    KEY_SIGN = "Sign"

    KEY_PARAMETER = "Parameter"

    VALUE_FORMAT_JSON = "json"
    VALUE_FORMAT_XML = "xml"

    def __init__(self):
        baseParam.__init__(self)
        #default format value is xml
        self.set_param(self.KEY_FORMAT, self.VALUE_FORMAT_XML)

    def validate(self):
        self.params

