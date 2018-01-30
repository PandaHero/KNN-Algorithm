import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re
import threading

# 获取浏览器驱动(禁止加载图片和javascript)
options = webdriver.ChromeOptions()
pref = {'profile.default_content_setting_values': {'images': 2, 'javascript': 2}}
options.add_experimental_option('prefs', pref)
browser = webdriver.Chrome(chrome_options=options)
browser_wait = WebDriverWait(browser, 10)
# 天猫商品列表表头
headers = {
    "cookie": "cna=5kffEqqIyS0CATz3G4EbJmmu; hng=CN%7Czh-CN%7CCNY%7C156; t=9b35ae456d1875923fa20b8aca3cf7b4; _tb_token_=43b3ec664044; cookie2=197619e2a335e6cffa3dc26262d2e4e0; sm4=110100; enc=24pHlTGtd5%2B9knRPQ%2FMbmjxcLZH7Vcq597xnwBKyb%2BSNdvFwdtkdDVGW9V14pPR%2B%2FiHhlltyQr77fHrlu4drHA%3D%3D; _med=dw:1366&dh:768&pw:1366&ph:768&ist:0; _m_h5_tk=430fa4d4029a5af842d694d696035a71_1517203571677; _m_h5_tk_enc=03d66a4a3ed285208819120db7471b18; tk_trace=1; pnm_cku822=098%23E1hvOQvUvbpvUpCkvvvvvjiPPLSUQjimRFLZ1j3mPmPp1jEhRscWgjlbP2LWsji2PsyCvvpvvvvvmphvLC2WTvvjPJ2v1n97RAYVyO2vqbVQWl4v1nLIRfU6pwet9E7rejvrYneYiLUpwHAxfwLhdigDNr3l%2BE7rejwuYnkQD40OJoL6AbmxdXkivpvUvvmv%2BvCjVOKEvpvVmvvC9jxvKphv8vvvvvCvpvvvvvmm86CvmUZvvUUdphvWvvvv9krvpv3Fvvmm86CvmVWCvpvVvvpvvhCv2QhvCPMMvvm5vpvhvvmv99%3D%3D; res=scroll%3A1349*5543-client%3A1349*609-offset%3A1349*5543-screen%3A1366*768; Hm_lvt_9d483e9e48ba1faa0dfceaf6333de846=1515566978,1515567233,1517201122,1517201738; Hm_lpvt_9d483e9e48ba1faa0dfceaf6333de846=1517201869; cq=ccp%3D1; isg=BHV1IDOSQ1rJ_afi-KlkdpVFhPEv8ikEEeEep_eaCOw7zpXAv0I51IOkHJB4jkG8",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
max_count = 10
proxy_pool_url = "http://127.0.0.1:5010/get/"
# 设置初始代理为空
proxy = None
# 开始时间
start_time = time.time()


# 浏览器加载主页面并返回包含关键字商品的总页数
def search():
    browser.get("https://www.tmall.com/")
    editText = browser_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mq")))
    button = browser_wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#mallSearch > form > fieldset > div > button")))
    editText.send_keys("红酒")
    button.click()
    total_page_num = browser_wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#J_Filter > p > b.ui-page-s-len"))).text
    total_page_num = int(total_page_num.split("/")[1])
    return total_page_num


# 翻页，并返回商品列表页信息
def next_page(page_num):
    try:
        edit_text = browser_wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-skip > form > input.ui-page-skipTo")))
        button = browser_wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-skip > form > button")))
        edit_text.clear()
        edit_text.send_keys(page_num)
        button.click()
        # 判断当前页面是否是加载页面
        browser_wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#content > div > div.ui-page > div > b.ui-page-num > b.ui-page-cur"), str(page_num)))
    except TimeoutError:
        next_page(page_num)


# 解析列表页
def get_product_list_info():
    '''
    :return: 返回商品的链接用于解析商品详情信息
    '''
    product_info_list = []
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    product_lists = soup.find("div", {"id": "J_ItemList"})
    product_items = product_lists.find_all("div", {"class": "product"})
    for item in product_items:
        productPrice = item.find("p", {"class": "productPrice"})
        product_info = {}
        if productPrice:
            # 商品价格
            productPrice = productPrice.get_text().replace("¥", "").strip()
            # 商品名称
            productTitle = item.find("p", {"class": "productTitle"}).a["title"].strip()
            # 商品链接
            productUrl = "https:" + item.find("p", {"class": "productTitle"}).a["href"].strip()
            # 商品spu,sku
            spu = re.search("\d+", productUrl.split("&")[0]).group()
            sku = re.search("\d+", productUrl.split("&")[1]).group()
            # 店铺名称
            productShop = item.find("div", {"class": "productShop"}).get_text().strip()
            # 店铺ID
            shopID = re.search("\d+", productUrl.split("&")[2]).group()
            # 月成交量和评价数
            productStatus = item.find("p", {"class": "productStatus"}).get_text().strip()
            # 月成交量
            month_buy = productStatus.split("笔")[0].replace("月成交", "").strip()
            # 评价数
            productComments = productStatus.split("笔")[1].replace("评价", "").strip()
            product_info = {
                "productTitle": productTitle,
                "productUrl": productUrl,
                "productPrice": productPrice,
                "month_buy": month_buy,
                "product_comments": productComments,
                "productShop": productShop,
                "spu": spu,
                "sku": sku,
                "shopID": shopID
            }
        if product_info:
            product_info_list.append(product_info)
    return product_info_list


# 获取代理
def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_detail_product_info(productUrl):
    response = requests.get(productUrl, allow_redirects=False, headers=headers)
    if response.status_code == 200:
        print(response.status_code)
    elif response.status_code == 302:
        print(response.status_code)


def main():
    total_page_num = search()
    for page in range(1, total_page_num + 1):
        next_page(page)
        product_info_list = get_product_list_info()
        threads = []
        for product_info in product_info_list:
            thread = threading.Thread(target=get_detail_product_info, args=(product_info["productUrl"],))
            threads.append(thread)
        yield threads



if __name__ == '__main__':
    threads = main()
    for t in threads:
        for i in t:
            i.start()
        for j in t:
            j.join()
    end_time = time.time()
    print(end_time - start_time)
