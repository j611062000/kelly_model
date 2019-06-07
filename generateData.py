import json

from configuration import *
from datetime import datetime
from numpy.random import normal, randint



def dumpUniformDistribution(numberOfSampling, sourceFileName, numberOfExperiments, dataFromMemory = False, targetFileName = False):

    dataToBeSerialized = createHeader(flag = 2, returnStyle = 1, underlying = "0050.tw")

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
    
    if not targetFileName:
        with open("0050_simulated_return.json","w") as targetFile:
            json.dump(dataToBeSerialized, targetFile, indent = 4)
   
    elif targetFileName:
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
    dumpUniformDistribution(
        numberOfSampling = 250, 
        sourceFileName = "./data/0050/0050_Return_Path.json",
        numberOfExperiments = 10000)