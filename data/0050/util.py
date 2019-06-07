import json


def HPR():
    """
    Reference: Prof. Wu's blog
    """
    geoMean = dict()
    with open("0050_Return_Path.json", "r") as file:
        returns = json.load(file)["Return Path"]

    max_loss = min(returns)
    f = [x/100 for x in range(1,101)]
    for fraction in f:
        hpr = 1
        for count, daily_return in enumerate(returns):
            hpr *= 1+fraction*(-(daily_return)/max_loss)
        geoMean[str(fraction)] = (hpr**(1/(1+count)))
    with open("0050_HPR_and_f.json", "w") as file:
        json.dump(geoMean,file,indent=4)

def extractReturnPath(file):
    return_tmp = list()
    with open(file, "r") as rawData:
        rawData = json.load(rawData)
        for data in rawData:
            print(data)
            return_tmp.append(rawData[data]["Daily Return"])
    with open("0050_Return_Path", "w") as file:
        json.dump({"Return Path":return_tmp}, file, indent=4)
    

def rawDataToJson():
    tmp_data = None

    with open("0050_refinement.json", "r") as data:
        data_from_json = json.load(data)
        tmp = list()
        last_price = 100
        for daily_data in data_from_json:
            today_price = data_from_json[daily_data]["price"]
            data_from_json[daily_data]["Daily Return"] = (today_price - last_price) / last_price
            last_price = today_price
        tmp_data = data_from_json

    with open("0050_refinement_01.json", "w") as file:
        json.dump(tmp_data, file, indent=4)

def main():
    # extractReturnPath("./0050_refinement.json")
    HPR()

main()