import json

from datetime import datetime
from loadDataFromJson import loadJson, loadAllDataFromJson

# flag : the data format of the value under the label, "data"

INDENT = 4
SUFFIX_OF_PRICED_DATA = "_price.json"
SUFFIX_OF_MDD_DATA = "_MDD.json"
SUFFIX_OF_FINAL_RTN = "_FinalRtn.json"

def createHeaderOfTemplateForJson(flag, returnStyle):
    headerOfTemplateForJson = {
        "metadata": {
            "flag":flag,
            "underlying": None,
            "lengthOfEachExperiment": None,
            "numberOfExperiments": None,
            "returnStyle":returnStyle,
            "time":str(datetime.today())
        },
        "data": None
    }

    return headerOfTemplateForJson

def injectFractionToExperiment(aVectorOfReturn, fraction, retrunStyle, initWealth = 1):
    
    tmp = [initWealth]

    for eachReturn in aVectorOfReturn:
    
        if retrunStyle == 0:
            calResultOfReturn = eachReturn
        
        elif retrunStyle == 1:
            calResultOfReturn = (1+eachReturn)
    
        last_return = tmp[-1]
        tmp.append((1-fraction) * last_return + (fraction*calResultOfReturn*last_return))
    
    return tmp[1:]


def processBatchPriceAndDumpToJson(fraction, retrunStyle, experiments, flag, fileNameWithoutDotJson):
    
    pricedDatas = dict()

    for count, experiment in enumerate(experiments):
    
        if flag == 1:
            # vectorOfReturn = experiment
            aVectorOfReturn = experiments[experiment]

        elif flag == 0 or flag == 2:
            aVectorOfReturn = experiment
    
        pricedDatas[str(count)] = injectFractionToExperiment(aVectorOfReturn, fraction, retrunStyle)

    with open(fileNameWithoutDotJson + SUFFIX_OF_PRICED_DATA,"w") as file:
        json.dump(pricedDatas, file, indent = INDENT)


def MDD(prices, maxDrawdown=0):

    high = prices[0]

    for price in prices:
        
        if price == 0:
            return -1

        elif high > price:
            maxDrawdown = min(maxDrawdown, (price - high) / high)
        
        else:
            high = price

    return maxDrawdown


def processBatchMDDAndDumpToJson(fileNameWithoutDotJson):
    
    tmp = dict()

    pricedDatas = loadJson(fileNameWithoutDotJson + SUFFIX_OF_PRICED_DATA)
    
    for count, key in enumerate(pricedDatas):
        tmp[str(count)] = MDD(pricedDatas[key])
    
    with open(fileNameWithoutDotJson + SUFFIX_OF_MDD_DATA,"w") as file:
        json.dump(tmp, file, indent = INDENT)


def processBatchFinalRtnAndDumpToJson(fileNameWithoutDotJson):
    
    tmp = dict()
    datas = loadJson(fileNameWithoutDotJson + SUFFIX_OF_PRICED_DATA)
    
    for count, data in enumerate(datas):
        prices = datas[data]
      
        tmp[str(count)] = prices[-1] - prices[0]

    with open(fileNameWithoutDotJson + SUFFIX_OF_FINAL_RTN,"w") as file:
        json.dump(tmp, file, indent = INDENT)


if __name__ == "__main__":
    fileNameWithoutDotJson = "./data/0050/backTesting/0050_Return_Path"
    fileName = fileNameWithoutDotJson+".json"
    fraction = 0.624

    experiments ,timePeriod, numberOfExperiment, returnStyle, flag= loadAllDataFromJson(fileName)

    # datas = load_json("./data/"+str(number)+"_experiment.json")

    processBatchPriceAndDumpToJson(fraction, returnStyle, experiments, flag, fileNameWithoutDotJson)
    processBatchMDDAndDumpToJson(fileNameWithoutDotJson)
    processBatchFinalRtnAndDumpToJson(fileNameWithoutDotJson)