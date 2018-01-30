import re
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 获取浏览器驱动
browser = webdriver.Chrome()
browser_wait = WebDriverWait(browser, 10)
# 京东商品列表表头
headers = {"Accept-Encoding": "gzip, deflate, sdch, br",
           "Accept-Language": "zh-CN,zh;q=0.8",
           "Connection": "keep-alive",
           "Cookie": "ipLoc-djd=1-72-2799-0; qrsc=3; user-key=fabc9ed1-34b6-4c47-905b-8a591c1584ff; cn=0; TrackID=1Cf0d8zDlNMi-Nh8fJzaxQHyuj6yY95ZNW997HP7tApYzeedW_TcPakelmURjH5SMG1fy9iSppcwzMedQOq1slM23N69mAYd2QiDZwZgH4Wg; pinId=zcvgUdwKIVIc3Mjva66NhLV9-x-f3wj7; pin=jd_638309812df29; unick=jd_188117vlqn; _tp=C6E1mKU%2FUrE9D%2Bsr77FDJPWRQmq6iENw%2Bqd0qhQpdpY%3D; _pst=jd_638309812df29; ceshi3.com=103; mt_xid=V2_52007VwMWUl5dUFMaSxBfBGIDEFZbUVpZGE0ZbAAzBhAGCFABRkhLTA4ZYgoWBUEIAAoZVREIUGNQEAJYCFRYHnkaXQVhHxJRQVlVSx9MEl8CbAMQYl9oUmofShpcBGEDEVdtWFdcGA%3D%3D; unpl=V2_ZzNtbRBTExUmWhFSKE0IVWIAFFVKB0oSc1tBV30dCwFkA0ZcclRCFXMURldnGFsUZwYZX0NcRxxFCEdkex5fDGQzFllDVkEcdgF2ZHgZbAVXAxZdQVJBHHAKT1d6HFwHYwUbVUFQRxVFOEFkexBYAWUDEG2WwujN%2fp8UFTnA7KCxqbxtRVJEE3wBQ1BLGGwEV1V8XUNWQhR9CURdfVRcAWcAF19LUkEcdglDVHkdWgxvABVZQmdCJXY%3d; __jdv=122270672|c.duomai.com|t_16282_55003828|tuiguang|c5a1bcf7beea42799a867b6275f521e0|1512541856677; thor=A257E4655512B33DC660E4CA52B913D703513485981E874E98F24A135E236C9D2E05DAD37089CFD0A8AD49B30AADA9000B6ECE5078C8BEF6AEDE0FB3498CC20A471BDA6A981307F835C719913EA1C62636B82C6B46A72FBAC7213AD77E72BE2F70B2705720AB37695921897FD2D0BDD06FC1CE08ECF381BE7F67B847D2A0D373E760E0E041DF62164EBF05510FA67F88F338945CA6200DE4E1E17042AE2400B9; __jda=122270672.15124384382041357892651.1512438438.1512539786.1512541857.10; __jdb=122270672.11.15124384382041357892651|10.1512541857; __jdc=122270672; xtest=3379.cf6b6759; rkv=V0200; __jdu=15124384382041357892651; 3AB9D23F7A4B3C9B=6PKO32CAWD4YZDHT5H5EBATJ4DT4RFKEQ7EFFJUQYW54U5N6ERCIHDRIVQV3WBCHYY5VFR6XJNEKH7WCVXHBD7RZAM",
           "Host": "search.jd.com",
           "Referer": "https://search.jd.com/Search?keyword=%E7%BA%A2%E9%85%92&enc=utf-8&suggest=1.his.0.0&wq=&pvid=76c46eeb71b0417e93d45d6900c4796f",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "X-Requested-With": "XMLHttpRequest"}


# 浏览器加载主页面并返回包含关键字商品的总页数
def search():
    browser.get("https://www.jd.com")
    editText = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#key")))
    button = browser_wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button > i")))
    editText.send_keys("红酒")
    button.click()
    total_page_num = browser_wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1) > b"))).text
    return total_page_num


# 传入页码，并返回商品列表
def next_page(page_num):
    lists = []
    print("正在翻第" + str(page_num) + "页")
    # 判断items(每一个宝贝)是否加载成功
    # browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ml-wrap .gl-warp .gl-item")))
    # 获取页面右上角点击按钮
    button = browser_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_topPage > a.fp-next")))
    button.click()
    # 休息2秒获取下一个页面
    time.sleep(2)
    # 获取网页源代码
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    goodsList = soup.find("div", {"id": "J_goodsList"})
    # print(type(goodsList))
    items = goodsList.find_all("li")
    show_item = ""
    for item in items:
        # print(type(item))
        data_sku = item["data-sku"]
        show_item = show_item + str(data_sku) + ","
    show_items = show_item[:-2]
    # 剩下的30个商品item的url获取网页源码并解析
    url = "https://search.jd.com/s_new.php?keyword=%E7%BA%A2%E9%85%92&enc=utf-8&" + "page=" + str(
        int(2 * page_num)) + "&scrolling=y&show_items=" + str(show_items)
    req = requests.get(url, headers=headers)
    obj_soup = BeautifulSoup(req.text, "lxml")
    list_1 = obj_soup.find_all("li", {"class": "gl-item"})
    lists = goodsList.find_all("li", {"class": "gl-item"})
    # 把剩下的30个商品items添加到lists列表中
    lists.extend(list_1)
    goods_info = []
    for goods in lists:
        # goods_details = goods.find("div", {"class": "p-name p-name-type-2"})
        goods_price = goods.find("div", {"class": "p-price"})
        goods_url = goods.find("div", {"class": "p-img"})
        goods_commit = goods.find("div", {"class": "p-commit"})
        # details = goods_details.a["title"]
        url = goods_url.a["href"]
        if "https" in url:
            url = url
        else:
            url = "http:" + url
        price = goods_price.get_text().replace("\n", "").replace("￥", "").replace(" ", "")
        commit = goods_commit.get_text().replace("\n", "").replace("条评价", "")
        if "万" in commit:
            commits = float(re.search("\d", commit).group()) * 10000
            # product = {"good_title": details, "good_url": url, "good_price": price, "good_commit": commits}
        else:
            commits = commit
        product = {"good_url": url, "good_price": price, "good_commit": commits}
        goods_info.append(product)
        # print(details, url, price, commits)
    return goods_info


# 解析每个商品url的信息，并返回商品详情页的数据：品牌、原产国、原料、产区等等
def get_details_info(url):
    product_details_dic = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    req = requests.get(url, headers=headers)
    print(url)
    if req.status_code == 200:
        # req.encoding = "utf-8"
        soup = BeautifulSoup(req.text, "lxml")
        # 获取商品的详细信息
        good_parameter = soup.find("div", {"class": "p-parameter"})
        # parameter_brand = good_parameter.find("ul", {"id": "parameter-brand"}, {"class": "p-parameter-list"})
        # brand = parameter_brand.find("li")["title"]
        if good_parameter:
            p_parameter_list = good_parameter.find("ul", {"class": "parameter2"})
            print(p_parameter_list)
            li_parameter_list = p_parameter_list.find_all("li")
            # 把商品介绍的详情信息添加到product_details_info
            for li_parameter in li_parameter_list:
                li_split = str(li_parameter.get_text()).split("：")
                product_details_dic[li_split[0]] = li_split[-1]
            # 把商品的规格与包装信息添加到product_details_info
            ptable = soup.find("div", {"class": "Ptable"})
            if ptable:
                ptable_dl = ptable.find("dl")
                ptable_dt = ptable_dl.find_all("dt")
                ptable_dd = ptable_dl.find_all("dd")
                for i in range(len(ptable_dt)):
                    product_details_dic[ptable_dt[i].get_text()] = ptable_dd[i].get_text()
    return product_details_dic


# def write_to_csv(goods):
#     with open(r"C:\Users\67505\Desktop\jd_wine.csv", "w+", newline="") as file:
#         writer = csv.writer(file)
#         writer.writerow(
#             ["goods_name", "goods_weight", "goods_price", "goods_commits", "goods_location", "acidity", "odor_type",
#              "is_import",
#              "taste", "color",
#              "character", "capacity", "sweetness", "classify", "packaging", "type", "grape_variety", "brand",
#              "origin_country", "raw_material", "producing_area", "year", "alcohol", "expiration_date", "fit_people",
#              "storage"])


def main():
    page_num = int(search())
    for num in range(1, page_num + 1):
        print(next_page(num))


if __name__ == '__main__':
    main()
