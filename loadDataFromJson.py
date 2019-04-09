import json

def loadAllDataFromJson(dataLabel, flagLabel, returnStyleLabel, filename):
    
    with open(filename, "r") as file:
            
            deserializedData = json.load(file)
            data             = deserializedData[dataLabel]
            flag             = deserializedData[flagLabel]
            returnStyle      = deserializedData[returnStyleLabel]
            
            # multiple lists under the "data" label, each list has a key
            # "data": {"key1":[],..., keyN:[]}
            if flag == 0:
                experiments = [data[eachLabel] for eachLabel in data]
            
            # single list under the "data" label
            # "data": [e1,..., eN]
            elif flag == 1:
                experiments = [data[dataLabel]]
            
            # multiple lists under the "data" label, each list has no key
            # "data": [[],...[]]
            elif flag == 2:
                experiments = [eachList for eachList in data]
                
            time_period = len(experiments[0])
            number_of_experiment = len(data)
    
    return (experiments, time_period, number_of_experiment, returnStyle, flag)