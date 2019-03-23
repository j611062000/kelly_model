# 固定一個下注比率& 模擬1000次， 橫軸是Rtn,縱軸是MDD
from bokeh.plotting import figure, output_file, show
from numpy.random import choice
import json

# 1. generate sim which # is 1000
# 2. cal every MDD and return for each sim
time = 30
prob = [0.5, 0.5]
return_vector = [3, 0]
time_period = time
number = 10000
init_wealth = 1
fixed_fraction = 0.2

def generate_flip_outcome(time, prob, return_vector):
    # retrun: a list of outcome which length is defined by time
    return [int(choice(return_vector, p=prob)) for x in range(time)]

def MDD(prices, maxDrawdown=0):
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
            # print(high, price)
        else:
            high = price

    return maxDrawdown

def  (number_of_data,filename,time, prob, return_vector):
    temp = dict()
    for i in range(number_of_data):
        temp[str(i)] = generate_flip_outcome(time, prob, return_vector)
    with open(filename,"w") as file:
        json.dump(temp, file, indent = 4)

def cal_final_return(fixed_fraction, init_wealth,flip_outcome, time_period):
    final_return = init_wealth

    for outcome in flip_outcome[0:time_period]:
        final_return = (1-fixed_fraction) * final_return + (fixed_fraction*outcome*final_return)
    return final_return

def load_json(filename):
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    return data

def cal_price(outcomes, init_wealth, fixed_fraction):
    tmp = [1]
    for outcome in outcomes[0:time_period]:
        last_return = tmp[-1]
        tmp.append((1-fixed_fraction) * last_return + (fixed_fraction*outcome*last_return))
    return tmp

def MDD_(number):
    tmp = dict()
    i = 0
    datas = load_json("./data/"+str(number)+"_experiment_price.json")
    for data in datas:
        tmp[str(i)] = MDD(datas[data])
        i+= 1
    with open("./data/"+str(number)+"_experiment_MDD.json","w") as file:
        json.dump(tmp, file, indent = 4)

def price(init_wealth, fixed_fraction,number):
    tmp = dict()
    i = 0
    datas = load_json("./data/"+str(number)+"_experiment.json")
    for data in datas:
        tmp[str(i)] = cal_price(datas[data], init_wealth, fixed_fraction)
        i+= 1

    with open("./data/"+str(number)+"_experiment_price.json","w") as file:
        json.dump(tmp, file, indent = 4)

def finalRtn(number):
    tmp = dict()
    i = 0
    datas = load_json("./data/"+str(number)+"_experiment_price.json")
    for data in datas:
        prices = datas[data]
        tmp[str(i)] = (prices[-1] - prices[0])/prices[0]
        i+= 1

    with open("./data/"+str(number)+"_experiment_finalRtn.json","w") as file:
        json.dump(tmp, file, indent = 4)


def main():
    file_num = "10000_T"+str(time)
    
     (number,"./data/"+str(file_num)+"_experiment.json",time, prob, return_vector)

    price(init_wealth , fixed_fraction, file_num)
    MDD_(file_num)
    finalRtn(file_num)

if __name__ == '__main__':
    main()