import json

from datetime import datetime
from numpy.random import normal, randint


    
def dumpUniformDistribution(numberOfSampling, fileName, numberOfExperiments):

    dataToBeSerialized = {
        "metadata":{
            "underlying":"0050.tw",
            "numberOfExperiments":numberOfExperiments,
            "lengthOfEachExperiment":numberOfSampling
        },
        "data":[]
    }


    with open(fileName, "r") as fileOfData:
        deserializedData = json.load(fileOfData)["data"][-numberOfSampling:]

    for eachExperiment in range(numberOfExperiments):
        
        listOfChosenIndex = randint(0,numberOfSampling,size = numberOfSampling)
        
        pathOfReturn = list()
        for index in listOfChosenIndex:
            pathOfReturn.append(deserializedData[index])
        dataToBeSerialized["data"].append(pathOfReturn)
    
    with open("0050_simulated_return.json","w") as targetFile:
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

def dumpMDD
        
if __name__ == "__main__":
    # mean = 0
    # std = 0.1

    # num_of_exp = 100
    # time = 30
    # file_name = "./data/normal_dist_"+str(num_of_exp)+"exps"
    # dumpNormalDistribution(mean, std, num_of_exp, file_name, time)
    
    dumpUniformDistribution(250, "./data/0050/0050_Return_Path.json",10000)