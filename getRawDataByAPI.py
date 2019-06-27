import requests, os, json

api_key = "8BHO3DV69A6T0OPC"

with open("./data/top_100_list.json", "r") as file:
    data = json.load(file)
    for count, key in enumerate(data):
        try:
            ticker =data[key]["ticker"]
            url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&apikey="+api_key+"&outputsize=full"

            with open("./data/top_100_list/"+str(count-1)+"_"+data[key]["ticker"]+".json","w") as file:
                toBeDump = json.loads(requests.get(url).text)
                json.dump(toBeDump,file, indent=4)
        except:
            pass