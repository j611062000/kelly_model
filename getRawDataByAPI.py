import requests, os, json, time

api_key = "8BHO3DV69A6T0OPC"

with open("./data/top_100_list.json", "r") as file:
    data = json.load(file)
    for count, key in enumerate(data):
        try:
            if count<500:
                time.sleep(15)
                ticker =data[key]["ticker"]+".tw"
                url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&apikey="+api_key+"&outputsize=full"

                with open("./data/top_100_list/"+str(count-1)+"_"+data[key]["ticker"]+"/rawData.json","w") as file:
                    toBeDump = json.loads(requests.get(url).text)
                    json.dump(toBeDump,file, indent=4)
        except:
            pass