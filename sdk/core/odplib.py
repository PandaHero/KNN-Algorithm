#coding:utf8
#author:xiejiahong 149172415@qq.com

import urllib
import urllib.request
import requests
from urllib.parse import urlencode

def get(url, data):
    # print url + "?" + urllib.urlencode(data)
    return urllib.request.urlopen(url + "?" + urlencode(data)).read()

def post(url, data):
    req = requests.get(url)
    data = urlencode(data)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()