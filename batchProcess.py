import json

from datetime import datetime, date
from loadDataFromJson import loadJson, loadAllDataFromJson

# flag : the data format of the value under the label, "data"

INDENT = 4
SUFFIX_OF_PRICED_DATA = "_price.json"
SUFFIX_OF_MDD_DATA = "_MDD.json"
SUFFIX_OF_FINAL_RTN = "_FinalRtn.json"

def dumpDictToFile(dictData, filePath):
    with open(filePath, "w") as file:
        json.dump(dictData, file, indent=4)

def convetStringToDate(stringDate):
    return datetime.strptime(stringDate, '%Y-%m-%d')

def createHeaderOfTemplateForJson(flag, returnStyle, underlying, dataRange,lengthOfEachExperiment = None, numberOfExperiments = None):
    headerOfTemplateForJson = {
        "metadata": {
            "flag":flag,
            "underlying": underlying,
            "lengthOfEachExperiment": lengthOfEachExperiment,
            "numberOfExperiments": numberOfExperiments,
            "returnStyle":returnStyle,
            "timeRange":str(dataRange[0])+"-"+str(dataRange[1]) if not (type(dataRange) == str) else dataRange
        },
        "data": list()
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

def findValueInDictByKeyName(keyNames, dictData):
    if len(keyNames) > 0:
        return findValueInDictByKeyName(keyNames[1:], dictData[keyNames[0]])
    else:
        return dictData

def batchProcessRtnToNormalizedPrice(fileName):
    data = loadJson(fileName)
    priceData = [1]
    dataLabel = "data"

    for rtn in data[dataLabel]:
        priceData.append(priceData[-1]*(1+rtn))
    print(priceData)
        



def processBatchPriceToRtn(filePath, dumpFileName, dataRange):
    '''
    Input : 
        The raw data from Alpha Vintage
        dataRange = [lowerBound, UpperBound]
    Output:  
        "metadata": {
            "flag":0,
            "underlying": xxxx,
            "lengthOfEachExperiment": None,
            "numberOfExperiments": None,
            "returnStyle":1,
            "time":str(datetime.today())
        },
        "data": [
            0,
            1.2,
            .
            .
            .
            1.3
        ]
        the first element in "data" satnds for the earliest data
    '''

    deserializedData = loadJson(filePath)
    pathForUnderlying = ["Meta Data","2. Symbol"]
    underlying = findValueInDictByKeyName(pathForUnderlying, deserializedData)
    
    header = createHeaderOfTemplateForJson(0,1, dataRange,underlying)
    pathForPrice = ["Time Series (Daily)"]
    priceData = findValueInDictByKeyName(pathForPrice, deserializedData)

    initPrice = 0
    for dailyPriceData in priceData:
        beforeUpperBound = convetStringToDate(dailyPriceData) <= dataRange[1]
        afterLowerBound  = convetStringToDate(dailyPriceData) >= dataRange[0]
        
        if beforeUpperBound and afterLowerBound:
            currentPrice = float(priceData[dailyPriceData]['4. close'])
            rtn = (initPrice - currentPrice)/currentPrice
            header["data"].insert(0,rtn)
            initPrice = currentPrice
    header["data"].pop(-1)

    dumpDictToFile(header, dumpFileName)        
    



if __name__ == "__main__":

    tickers = ["1301", "1303", "1326", "2317", "2330", "2412", "2454", "2882", "3008", "6505"]

    # for ticker in tickers:    
    #     fileDir  = "./data/"+ticker+"/"
    #     filePath = "./data/"+ticker+"/rawData.json"
    #     dumpFileName = fileDir + "rtn.json"
    #     dataRange = [datetime(2018,1,15), datetime(2019,1,22)]
    #     processBatchPriceToRtn(filePath,dumpFileName,dataRange)

    
  
    # experiments ,timePeriod, numberOfExperiment, returnStyle, flag= loadAllDataFromJson(fileName)
    # experiments = [experiments[0][-251:]]
    
    # tmp = dict()
    # for i in range(0,100):
    #     # fraction = i/100
    #     fileNameWithoutDotJson = "./data/0050/backTesting/fraction_" + str(i) + "0050_Return_Path_MDD"
    #     fileName = fileNameWithoutDotJson+".json"
    #     with open(fileName, "r") as file:
    #         tmp[str(i)] = json.load(file)["0"]
    
    # with open("./data/0050/backTesting/0050_yearly_fraction_MDD.json", "w") as file:
    #     json.dump(tmp,file,indent=4)

    # processBatchPriceAndDumpToJson(fraction, returnStyle, experiments, flag, fileNameWithoutDotJson)
    # processBatchMDDAndDumpToJson(fileNameWithoutDotJson)
    # processBatchFinalRtnAndDumpToJson(fileNameWithoutDotJson)