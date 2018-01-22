# coding:utf8
# author:xiejiahong 149172415@qq.com

from sdk.parms.request_param import requestParam
from sdk.parms.user_param import userParam
# from core import util
import hashlib


# 拼接字符串
def getSignString(app_secret, sign_parameters):
    key_order = [requestParam.KEY_ACCESS_TOKEN, \
                 requestParam.KEY_FORMAT, \
                 requestParam.KEY_METHOD, \
                 requestParam.KEY_PARAMETER, \
                 requestParam.KEY_TS]
    datas = []
    for k in key_order:
        datas.append(k)
        datas.append(sign_parameters.params[k])
    return app_secret + "".join(datas) + app_secret


# 前面并设置所有请求参数
def getRequestParameters(user_parameters, app_secret, access_token, method, format="xml"):
    req_map = requestParam()
    req_map.set_param(requestParam.KEY_FORMAT, format)
    req_map.set_param(requestParam.KEY_METHOD, method)
    req_map.set_param(requestParam.KEY_ACCESS_TOKEN, access_token)
    req_map.set_param(requestParam.KEY_TS, util.now())
    req_map.set_param(requestParam.KEY_PARAMETER, user_parameters.getJson())

    signString = getSignString(app_secret, req_map)

    m = hashlib.md5()
    m.update(signString)
    md5_str = m.hexdigest().upper()
    req_map.set_param(requestParam.KEY_SIGN, md5_str)

    return True, "success", req_map
