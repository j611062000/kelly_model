from bs4 import BeautifulSoup
import requests, json

url = "http://jow.win168.com.tw/z/zm/zmd/zmdb.djhtm"
r = requests.get(url)

soup = BeautifulSoup(r.content)

dic = {
    "date":"2019/6/27",
    "description":"top 100 stock by market share"
}
ticker = list()
ticker_info = list()

for data in soup.findAll('td',{"class":"t3n1"}):
    if data.text == "\xa0":
        ticker_info.append("")
    else:
        ticker_info.append(data.text)

t = range(0,600,6)
it = iter(t)
for count, data in enumerate(soup.findAll('td',{"class":"t3t1"})):
    if data.text != "\n":
        c = next(it)
        dic[str(count+1)] = {
            "ticker":str(data.text[:4]),
            "market_share":ticker_info[c],
            "percentage_of_market":ticker_info[c+1],
            "accum_percentage":ticker_info[c+2]
        }


with open("./top_100_list.json", "w") as file:
    json.dump(dic,file,indent=4)
    


