import json
import os

LABEL_OF_DATA = "data"
LABEL_OF_FLAG = "flag"
LABEL_OF_METADATA = "metadata"
LABEL_OF_RETURN_STYLE = "returnStyle"

def getAllFilesName(path, exceptionOfFiles = list()):

    fileNames = list()

    for filename in os.listdir(path):
        if filename not in exceptionOfFiles:
            fileNames.append(filename)

    return fileNames


def loadJson(filename):
   
    with open(filename, "r") as toBeSerialized:
        serializedData = json.load(toBeSerialized)
   
    return serializedData


def loadAllDataFromJson(filename, targetDir = ""):
    with open(targetDir+filename, "r") as file:
            
            deserializedData = json.load(file)
            data             = deserializedData[LABEL_OF_DATA]
            flag             = deserializedData[LABEL_OF_METADATA][LABEL_OF_FLAG]
            returnStyle      = deserializedData[LABEL_OF_METADATA][LABEL_OF_RETURN_STYLE]
            
            # single list under the "data" label
            # "data": [e1,..., eN]
            if flag == 0:
                experiments = [data]
            
            # multiple lists under the "data" label, each list has a key
            # "data": {"key1":[],..., keyN:[]}
            elif flag == 1:
                experiments = [data[eachLabel] for eachLabel in data]
            
            # multiple lists under the "data" label, each list has no key
            # "data": [[],...[]]
            elif flag == 2:
                experiments = [eachList for eachList in data]
                
            time_period = len(experiments[0])
            number_of_experiment = len(data)
    
    return (experiments, time_period, number_of_experiment, returnStyle, flag)

if __name__ == "__main__":
    print(getAllFilesName("./data/0050/MovingWindow/SimulationOfEachWindow/", ["0050_Return_Path.json"]))