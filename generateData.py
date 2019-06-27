import json

from batchProcess import *
from configuration import *
from datetime import datetime
from loadDataFromJson import loadJson
from numpy.random import normal, randint


# rtn.json --> simulated.rtn.json
def dumpUniformDistribution(numberOfSampling, sourceFileName, numberOfExperiments,  targetFileName = False, dataFromMemory = False):

    deserializedData  = loadJson(sourceFileName)
    pathForUnderlying = ["metadata","underlying"]
    pathForTimeRange  = ['metadata','timeRange']
    underlying = findValueInDictByKeyName(pathForUnderlying, deserializedData)
    dataRange  = findValueInDictByKeyName(pathForTimeRange, deserializedData)
    print(dataRange)

    dataToBeSerialized = createHeaderOfTemplateForJson(flag = 2, returnStyle = 1, underlying = underlying, dataRange=dataRange,lengthOfEachExperiment = numberOfSampling, numberOfExperiments = numberOfExperiments)

    if not dataFromMemory:
        with open(sourceFileName, "r") as fileOfData:
            deserializedData = json.load(fileOfData)["data"][-numberOfSampling:]
    
    elif dataFromMemory:
        deserializedData = dataFromMemory

    for eachExperiment in range(numberOfExperiments):
        listOfChosenIndex = randint(0,numberOfSampling-1,size = numberOfSampling)
        pathOfReturn = list()
        
        for index in listOfChosenIndex:
                pathOfReturn.append(deserializedData[index])

        dataToBeSerialized["data"].append(pathOfReturn)
    
    with open(targetFileName,"w") as targetFile:
        json.dump(dataToBeSerialized, targetFile, indent = 4)

def dumpNormalDistribution(mean, std, num_of_exp,file_name, time):
    data = dict()
    with open(file_name+".json","w") as file:
        for exp in range(num_of_exp):
            data[str(exp+1)] = [x for x in normal(mean, std, time)]
        
        dic = {
            "metaData":
                {
                    "mean":mean, 
                    "std":std, 
                    "num_of_exp":num_of_exp, 
                    "model":"normal",
                    "Time":str(datetime.today())
                },
            "data": data
            }
        json.dump(dic, file, indent = 4)

        
if __name__ == "__main__":
    # mean = 0
    # std = 0.1

    # num_of_exp = 100
    # time = 30
    # file_name = "./data/normal_dist_"+str(num_of_exp)+"exps"
    # dumpNormalDistribution(mean, std, num_of_exp, file_name, time)
    tickers = ["1301", "1303", "1326", "2317", "2330", "2412", "2454", "2882", "3008", "6505"]

    for ticker in tickers:
        dumpUniformDistribution(
            numberOfSampling = 250, 
            sourceFileName = "./data/"+ticker+"/rtn.json",
            numberOfExperiments = 10000,
            targetFileName="./data/"+ticker+"/simulated_rtn.json")