def createHeader(flag, returnStyle, underlying):
    header =  {
        "metadata":{
            "flag":flag,
            "lengthOfEachExperiment":None,
            "numberOfExperiments":None,
            "returnStyle":returnStyle,
            "underlying":underlying
        },
        "data":[]
    }

    return header
