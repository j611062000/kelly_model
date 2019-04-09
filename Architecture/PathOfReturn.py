import json

"""
{
    "metaData":{},
    "data":{
        "date1": data1,
        "date2": data2,
        .
        .
        .
        "dateN": dataN,

    },
    
}
"""

class PathOfReturn():
    
    fractionRange = None
    numberOfPlays = None
    odds = None

    def __init__(self, pathOfReturn = None):
        
        self.mdd = None
        self.pathOfReturn = pathOfReturn
    
    @classmethod
    def extractOnePathOfReturnFromFile(cls, filename, withDate = False, dataLabel = "data"):
        if filename:
            with open(filename, "r") as fileOfData:
                deserializedData = json.load(fileOfData)
            
            # all values are under "data" as a list
            if not withDate:
                pathOfReturn = deserializedData[dataLabel]

            # one key, one value    
            else:
                pathOfReturn = list()
                for eachDateLabel in deserializedData[dataLabel]:
                    pathOfReturn.append(deserializedData[dataLabel][eachDateLabel])
        
        return cls(pathOfReturn)


class AggregatedPathOfReturn():


    def __init__(self,filename):
        self.alphaRange = None
        self.arrayForPathOfReturn = list()
        self.pathOfReturns = self.extractPathOfReturnsFromFile(filename)
    
    def extractPathOfReturnsFromFile(self, filename, dataLabel = "data"):
        if filename:
            with open(filename, "r") as fileOfData:
                deserializedData = json.load(fileOfData)
            
            # all lists are under "data"
            pathOfReturns = list()
            for eachLabelOfList in deserializedData[dataLabel]:
                pathOfReturns.append(deserializedData[dataLabel][eachLabelOfList])
        

            

if __name__ == "__main__":
    testPathOfReturns = AggregatedPathOfReturn("testDataForPathOfReturns.json")
    print(testPathOfReturns.pathOfReturns)