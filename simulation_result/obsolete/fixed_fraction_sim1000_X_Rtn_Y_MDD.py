import json
from batchProcess import processBatchPriceAndDumpToJson
from batchProcess import processBatchMDDAndDumpToJson
from batchProcess import processBatchFinalRtnAndDumpToJson

from bokeh.plotting import figure, output_file, show
from numpy.random import choice
from loadDataFromJson import loadAllDataFromJson

# 固定一個下注比率& 模擬1000次， 橫軸是Rtn,縱軸是MDD
# 1. generate sim which # is 1000
# 2. cal every MDD and return for each sim

# time = 30
# prob = [0.5, 0.5]
# return_vector = [3, 0]
# time_period = time
# number = 10000
# init_wealth = 1
# fixed_fraction = 0.2

def generate_flip_outcome(time, prob, return_vector):
    # retrun: a list of outcome which length is defined by time
    return [int(choice(return_vector, p=prob)) for x in range(time)]


def generate_json(number_of_data,filename,time, prob, return_vector):
    temp = dict()
    for i in range(number_of_data):
        temp[str(i)] = generate_flip_outcome(time, prob, return_vector)
    with open(filename,"w") as file:
        json.dump(temp, file, indent = 4)


# def load_json(filename):
#     with open(filename, "r") as read_file:
#         data = json.load(read_file)
#     return data


# def MDD(prices, maxDrawdown=0):
#     """
#     data: a list stores the wealth(i), i=1~n
#     definition of MDD: (price-high)/high
#     """

#     high = prices[0]
#     for price in prices:
#         if price == 0:
#             # you lose all wealth when second round (=prices[0])
#             return -1

#         elif high > price:
#             maxDrawdown = min(maxDrawdown, (price - high) / high)
#             # print(high, price)
#         else:
#             high = price

#     return maxDrawdown


# def processBatchMDD(number):
#     tmp = dict()
#     i = 0
#     datas = load_json("./data/"+str(number)+"_experiment_price.json")
#     for data in datas:
#         tmp[str(i)] = MDD(datas[data])
#         i+= 1
#     with open("./data/"+str(number)+"_experiment_MDD.json","w") as file:
#         json.dump(tmp, file, indent = 4)


# def cal_final_return(fixed_fraction, init_wealth,flip_outcome, time_period, retrunStyle):
    
#     final_return = init_wealth
#     calResultOfReturn = None

#     for outcome in flip_outcome[0:time_period]:
        
#         if retrunStyle == 0:
#             calResultOfReturn = outcome
        
#         elif retrunStyle == 1:
#             calResultOfReturn = (1+outcome)

#         final_return = (1-fixed_fraction) * final_return + (fixed_fraction*(calResultOfReturn)*final_return)
#     return final_return


# def cal_price(outcomes, init_wealth, fixed_fraction, retrunStyle):
    
#     tmp = [1]

#     for outcome in outcomes:
    
#         if retrunStyle == 0:
#             calResultOfReturn = outcome
        
#         elif retrunStyle == 1:
#             calResultOfReturn = (1+outcome)
    
#         last_return = tmp[-1]
#         tmp.append((1-fixed_fraction) * last_return + (fixed_fraction*calResultOfReturn*last_return))
    
#     return tmp


# def processBatchPrice(init_wealth, fixed_fraction,number, retrunStyle, datas):
#     tmp = dict()
#     i = 0

#     for data in datas:
#         tmp[str(i)] = cal_price(datas[data], init_wealth, fixed_fraction, retrunStyle)
#         i+= 1

#     with open("./data/"+str(number)+"_experiment_price.json","w") as file:
#         json.dump(tmp, file, indent = 4)


# def processBatchFinalRtn(number):
#     tmp = dict()
#     i = 0
#     datas = load_json("./data/"+str(number)+"_experiment_price.json")
#     for data in datas:
#         prices = datas[data]
#         tmp[str(i)] = (prices[-1] - prices[0])/prices[0]
#         i+= 1

#     with open("./data/"+str(number)+"_experiment_finalRtn.json","w") as file:
#         json.dump(tmp, file, indent = 4)


def main():
    
    fileNameWithoutDotJson = "./data/0050/0050_simulated_return"
    fileName = fileNameWithoutDotJson+".json"
    fraction = 0.624
    
    dataLabel = "data"
    flagLabel = "flag"
    returnStyleLabel = "returnStyle"
    
    # numberOfLimitedTestData = 4

    argsForLoadDataFromJson = [dataLabel, flagLabel, returnStyleLabel, fileName]
    experiments ,timePeriod, numberOfExperiment, returnStyle, flag= loadAllDataFromJson(*argsForLoadDataFromJson)

    # datas = load_json("./data/"+str(number)+"_experiment.json")

    processBatchPriceAndDumpToJson(fraction, returnStyle, experiments, flag, fileNameWithoutDotJson)
    processBatchMDDAndDumpToJson(fileNameWithoutDotJson)
    processBatchFinalRtnAndDumpToJson(fileNameWithoutDotJson)
    

    # processBatchPrice(initWealth = 1 , fixed_fraction, file_num, retrunStyle, datas)
    # processBatchFinalRtn(file_num)
    # generate_json(number,"./data/"+str(file_num)+"_experiment.json",time, prob, return_vector)
    
if __name__ == '__main__':
    main()