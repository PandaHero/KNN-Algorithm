# # # import requests
# # #
# # # proxy = {"http": "http://218.64.220.2:1080"}
# # # req = requests.get("https://www.google.com.hk/", proxies=proxy)
# # # print(req.text)
# # name=input("请输入你的姓名")
# # print(name)
# from urllib.parse import urlencode
#
# url = "https://maps.googleapis.com/maps/api/streetview?"
# for i in range(-90, 135, 45):
#     for j in range(0, 360, 45):
#         params = {"size": "600x300",
#                   "location": "39.9071439,116.3971384",
#                   "heading": str(j),
#                   "pitch": str(i)}
#         data = url + urlencode(params)
#         print(data)
s=set([1,1,2,2])
print(s)
