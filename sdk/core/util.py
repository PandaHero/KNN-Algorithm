#coding:utf8
#author:xiejiahong 149172415@qq.com
import datetime

def date2str(d):
    return datetime.datetime.strftime(d, "%Y-%m-%d %H:%M:%S")

def now():
    return date2str(datetime.datetime.utcnow() + datetime.timedelta(hours=8))