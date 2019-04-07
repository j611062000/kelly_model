import json

def f_wealth_test(datas, f):
    simulation_of_f = list()
    final_wealth = 1
    for data in datas[1:]:
        final_wealth = (1-f)*final_wealth + (f)*final_wealth*(1+data)
        simulation_of_f.append(final_wealth)
        initial_price = data
    return final_wealth, simulation_of_f

def MDD_test(prices, maxDrawdown=0):
    """
    data: a list stores the wealth(i), i=1~n
    definition of MDD: (price-high)/high
    """
    high = prices[0]
    for price in prices:
        if price == 0:
            # you lose all wealth when second round (=prices[0])
            return -1

        elif high > price:
            maxDrawdown = min(maxDrawdown, (price - high) / high)

        else:
            high = price

    return maxDrawdown


with open("./data/0050/0050_Return_Path.json", "r") as file:
    data = json.load(file)["Return Path"]

with open("./data/0050/0050_f_With_MDD.json","w") as file:
    tmp = dict()
    for f in range(1,101):
        tmp[str(f)] = MDD_test(f_wealth_test(data,f/100)[1])
    json.dump(tmp,file,indent=4)
