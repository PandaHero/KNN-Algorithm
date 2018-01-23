import requests
from bs4 import BeautifulSoup

req = requests.get("https://item.jd.com/1304924.html")
soup = BeautifulSoup(req.text, "lxml")
sku_name = soup.find("div", {"class": "sku-name"})
# 删除空格
print(sku_name.get_text().strip())
img = sku_name.find("img")
if img:
    print(img["alt"])
dd = soup.find("div", {"class": "dd"})
variety = dd.find_all("div", {"class": "item  "})
print(variety)
