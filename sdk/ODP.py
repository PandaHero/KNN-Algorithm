#coding:utf8
#author:xiejiahong 149172415@qq.com

from core import odplib
from core import sign


def call(url, user_parameters, secret, token, method,http_method="get", format="json"):
    flag, msg, reqs = sign.getRequestParameters(user_parameters, secret, token, method, format=format)
    if http_method == "post":
        return odplib.post(url, reqs.params)
    else:
        return odplib.get(url, reqs.params)
