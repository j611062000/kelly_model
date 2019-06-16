import os
import json

from batchProcess import injectFractionToExperiment
from collections import defaultdict
from generateData import dumpUniformDistribution
from loadDataFromJson import loadAllDataFromJson, getAllFilesName
from plot import generateDotGraphWithSubYAxis, generateVanilaDotGraph
from simulation_X_f_Y_beta import batchCalProbBelowAlphaOfEachF


class Configuration():
    ALPHA = 0.03
    BETA = 0.8
    F_RANGE = [x / 100 for x in range(1, 101, 1)]
    LEN_HISTORY_WINDOW = 30
    LEN_FUTURE_WINDOW = 10
    NUMBER_OF_EXPERIMENTS_PER_WINDOW = 10000
    FILE_NAME = "0050_Return_Path.json"
    LABEL_OF_FRACTION = "fraction"
    READ_DATA_FROM_FILE = True
    TARGET_DIR = "./data/0050/MovingWindow/SimulationOfEachWindow/"
    DESIRED_TITLE = "Strategy v.s. 0050.tw"
    XLabel = "Time"
    YLabel = "Normalized Return"
    COLORS = ["red", "blue"]
    
    startSimulation = False
    probOfMddBelowAlphaOfEachF = defaultdict(lambda:0)
    expectedWealthOfEachF = defaultdict(lambda:0)


def plotStrategyAndUnderlying(Xs, Ys, legenOfData, ifWithLine = True):
    generateVanilaDotGraph(
        Configuration.DESIRED_TITLE,
        Configuration.XLabel, 
        Configuration.YLabel, 
        Xs, 
        Ys, 
        legenOfData, 
        ifWithLine,
        Configuration.COLORS)


def calFractionGivenAlphaBeta(experiments):
    argsOfBatchCalProbBelowAlphaOfEachF = [
        experiments,
        Configuration.F_RANGE, 
        Configuration.NUMBER_OF_EXPERIMENTS_PER_WINDOW,
        Configuration.LEN_HISTORY_WINDOW,
        Configuration.ALPHA,
        Configuration.BETA, 
        defaultdict(lambda:0), 
        defaultdict(lambda:0)]
    probBelowAlphaOfEachF, expWealthOfEachF = batchCalProbBelowAlphaOfEachF(*argsOfBatchCalProbBelowAlphaOfEachF)
    
    fraction = 0
    for f in Configuration.F_RANGE:
        if probBelowAlphaOfEachF[f] >= Configuration.BETA:
            fraction = f
    
    return fraction, probBelowAlphaOfEachF[fraction], expWealthOfEachF[fraction]


# def calRtnForEachWindow(fraction, returnPathOfFutureWindow, TARGET_DIR, FILE_NAME):
#     pass


def calRtnForWindows(TIME_SERIES, LEN_HISTORY_WINDOW, LEN_FUTURE_WINDOW, ALPHA, BETA, startSimulation, TARGET_DIR, NUMBER_OF_EXPERIMENTS_PER_WINDOW, FILE_NAME):
    # Input: list(), Output: list()

    exceptionOfFile = FILE_NAME
    fileNames = getAllFilesName(TARGET_DIR, exceptionOfFile)
    wealthPath = list()
    initWealth = 1


    if not Configuration.READ_DATA_FROM_FILE:
        if startSimulation:
            for startDay in range(0,len(TIME_SERIES)-LEN_HISTORY_WINDOW,LEN_FUTURE_WINDOW): 
                returnPathOfHistoryWindow = TIME_SERIES[startDay:startDay+LEN_HISTORY_WINDOW]
                dumpUniformDistribution(LEN_HISTORY_WINDOW, "None", NUMBER_OF_EXPERIMENTS_PER_WINDOW, returnPathOfHistoryWindow, TARGET_DIR+str(startDay)+".json")

        tmp = {"fraction":list(), "prob":list(), "E[Wealth]":list()}
        for count, fileName in enumerate(fileNames):
            experiments = loadAllDataFromJson(fileName,TARGET_DIR)[0]
            tmp["fraction"].append(calFractionGivenAlphaBeta(experiments)[0])
            tmp["prob"].append(calFractionGivenAlphaBeta(experiments)[1])
            tmp["E[Wealth]"].append(calFractionGivenAlphaBeta(experiments)[2])
            print("Progress: {} %".format(100*(count+1)/len(fileNames)))
    
    elif Configuration.READ_DATA_FROM_FILE:
        TIME_SERIES = loadAllDataFromJson(TARGET_DIR+FILE_NAME)[0][0][-250:]
        with open(TARGET_DIR+"result.json", "r") as file:
            fractionCandidates = json.load(file)[Configuration.LABEL_OF_FRACTION]

    for startDay, fraction in zip(range(0, len(TIME_SERIES), LEN_FUTURE_WINDOW), fractionCandidates):
        wealthPathOfThisWindow = injectFractionToExperiment(TIME_SERIES[startDay:startDay+LEN_FUTURE_WINDOW],fraction, 1, initWealth)
        wealthPath.extend(wealthPathOfThisWindow)
        initWealth = wealthPath[-1]
    wealthPath.insert(0,1)
    return wealthPath


def main():
    
    ALPHA = Configuration.ALPHA
    BETA = Configuration.BETA
    LEN_HISTORY_WINDOW = Configuration.LEN_HISTORY_WINDOW
    LEN_FUTURE_WINDOW = Configuration.LEN_FUTURE_WINDOW
    NUMBER_OF_EXPERIMENTS_PER_WINDOW = Configuration.NUMBER_OF_EXPERIMENTS_PER_WINDOW
    startSimulation = False

    FILE_NAME = Configuration.FILE_NAME
    TARGET_DIR = Configuration.TARGET_DIR
    
    TIME_SERIES = loadAllDataFromJson(TARGET_DIR+FILE_NAME)[0][0][-280:]
    argsOfCalRtnForWindows = [
        TIME_SERIES, 
        LEN_HISTORY_WINDOW, 
        LEN_FUTURE_WINDOW,
        ALPHA, 
        BETA, 
        startSimulation, 
        TARGET_DIR, 
        NUMBER_OF_EXPERIMENTS_PER_WINDOW,
        FILE_NAME
        ]
    
    wealthPathOfStrategy = calRtnForWindows(*argsOfCalRtnForWindows)
    wealthPathOfUnderlying = injectFractionToExperiment(TIME_SERIES[-250:],1,1)
    wealthPathOfUnderlying.insert(0,1)
    Xs = range(0,251)
    Ys = [wealthPathOfStrategy, wealthPathOfUnderlying]
    print(wealthPathOfStrategy)
    legend = ["Moving Window", "0050.tw"]
    plotStrategyAndUnderlying(Xs, Ys, legend)



if __name__ == "__main__":
    main()

    # calRtnForEachWindow()