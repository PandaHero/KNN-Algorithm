import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError

base_url = "http://weixin.sogou.com/weixin?"
headers = {
    "Cookie": "SUV=009B27273CF71B815A6150B95A13E112; IPLOC=CN1100; SUID=811BF73C1F13940A000000005A6E8279; ABTEST=0|1517191809|v1; SNUID=75E804CFF3F190134D2F1ABFF4758438; weixinIndexVisited=1; sct=1; JSESSIONID=aaaU2qWfxZgnL-XSSwCew",
    "Host": "weixin.sogou.com",
    "Referer": "http://weixin.sogou.com/weixin?query=%E9%A3%8E%E6%99%AF&type=2&page=4&ie=utf8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
proxy_pool_url = "http://127.0.0.1:5010/get/"
# 设置初始代理为空
proxy = None
max_count = 10


# 获取代理
def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


# 获取网页源代码
def get_html(url, count=1):
    print("Trying Count", count)
    # 设置代理为全局变量
    global proxy
    if count >= max_count:
        print("tried too many times")

    try:
        # 判断是否存在代理
        if proxy:
            proxies = {
                "http": "http://" + proxy
            }
            # 若存在代理，则使用代理
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 302:
            # 获取代理池中的代理
            proxy = get_proxy()
            # 非空判断
            if proxy:
                print("user proxy:" + proxy)
                return get_html(url)
            else:
                print("get proxy failed")
                return None
    except ConnectionError:
        print("error occured ", ConnectionError)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


# 获取网页链接
def get_index(keyword, page):
    data = {
        "query": keyword,
        "type": 2,
        "page": page
    }
    params = urlencode(data)
    url = base_url + params
    html = get_html(url)
    return html


def main():
    for page in range(10):
        html = get_index("风景", page)


if __name__ == '__main__':
    main()
