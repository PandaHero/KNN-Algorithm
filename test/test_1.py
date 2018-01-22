import csv
from urllib.parse import *
import requests
import json

# print(unquote("%5B%5D"))
headers = {
    "cookie": "ASP.NET_SessionSvc=MTAuOC4xODkuNTZ8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTUxMjA5MzU2NjE2OA; ASP.NET_SessionId=mxntav0qkfgqddqd5fnwcrrs; Favorite_Products=Pkg_0=2256299|1; StartCity_Pkg=PkgStartCity=1; _abtest_userid=25f8b7b2-96f1-44a8-b16d-d4707dc61b96; appFloatCnt=2; manualclose=1; StartCity_Pkg=PkgStartCity=1; DetailPageProductStarCity=pkg2256299_starcity1; Hm_lvt_9d483e9e48ba1faa0dfceaf6333de846=1516339654; Hm_lpvt_9d483e9e48ba1faa0dfceaf6333de846=1516340904; _RF1=60.247.27.129; _RSG=FG4zkMy6OOBH576vil1Et8; _RDG=28d958ae105a312e2a1db2e64c20ffbf76; _RGUID=b6181bc5-aef4-440f-8dce-06fb39187151; _ga=GA1.2.774395027.1516339658; _gid=GA1.2.1242263362.1516339658; _gat=1; MKT_Pagesource=PC; _bfi=p1%3D103047%26p2%3D103047%26v1%3D14%26v2%3D12; EnableUsaBooking=false; SaleCity_Pkg=PkgSaleCity=1; Hm_lvt_859112bb3c1c4be58e7e0e59a966879f=1516339654; Hm_lpvt_859112bb3c1c4be58e7e0e59a966879f=1516340926; _bfa=1.1516339654023.4c1789.1.1516339654023.1516339654023.1.15; _bfs=1.15",
    "referer": "https://vacations.ctrip.com/grouptravel/p2256299s1.html?kwd=%E4%B8%8A%E6%B5%B7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}


def parse_detail_page_province(url):
    province = {}
    req = requests.get(url, headers=headers)
    con_json = json.loads(req.content)
    for item in con_json["departureCity"]:
        province[item["name"]] = item["cityId"]
    return province


def get_detail_province_url(province):
    for name, city_id in province.items():
        info = {"ProductID": "2256299",
                "StartCity": city_id,
                "SalesCity": "1",
                "MinPrice": "2762",
                "EffectDate": "2014 - 12-31",
                "ExpireDate": "2018-05-05"}

        url = "https://vacations.ctrip.com/bookingnext/CalendarV2/CalendarInfo?" + urlencode(info)
        yield url


def get_detail_province_day_info(url):
    province_day_info = {}
    req = requests.get(url, headers=headers)
    req_json = json.loads(req.content)
    availableDate = req_json["calendar"]["bigCalendar"]["availableDate"]
    city_name = req_json["departureCity"][0]["name"]
    province_day_info["city_name"] = city_name
    for item in availableDate:
        date = item["Date"]
        price = item["MinPrice"]
        province_day_info[date] = price
    return province_day_info


if __name__ == '__main__':
    province = parse_detail_page_province(
        "https://vacations.ctrip.com/bookingnext/CalendarV2/CalendarInfo?ProductID=2256299&StartCity=1&SalesCity=1&MinPrice=2762&EffectDate=2014-12-31&ExpireDate=2018-05-05")
    # print(province)
    with open(r"C:\Users\chen\Desktop\新建 Microsoft Excel 工作表.csv", "a+", newline="", errors="ignore") as file:
        writer = csv.writer(file)
        writer.writerow(["city", "data", "price"])
        for url in get_detail_province_url(province):
            province_day_info = get_detail_province_day_info(url)
            for k in province_day_info.keys():
                if k != "city-name":
                    writer.writerow([province_day_info["city_name"], k, province_day_info[k]])
                print(province_day_info["city_name"] + "写入成功")
