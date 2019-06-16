import json
import matplotlib.pyplot as plt
import numpy as np
import os
import time

from batchProcess import MDD
from configuration import Plot
from collections import defaultdict
from datetime import datetime
from loadDataFromJson import loadAllDataFromJson
from matplotlib.ticker import PercentFormatter
from multiprocessing import Pool
from numpy.random import choice



# TODO expected value

def calProbBelowAlphaOfEachF(simulation_path, alpha, f_range, f_MDD_below_alpha, f_expected_wealth,increment, numOfExp):
   
    """
    Input: simulation of return with specified time periods, and parameters of f
    Output: An individual simulation with f from 0.00~1.00
    """
    try:
        simulation_f = allFractionOutcomeOfEachExperiemnt[numOfExp]
    
    except IndexError:
        simulation_f = defaultdict(list)

        for f in f_range:
            
            init_wealth = 1

            for outcome in simulation_path:
                # init_wealth = init_wealth * (1 - f) + init_wealth * f * (1+outcome)
                init_wealth = init_wealth*(1+f*outcome)
                simulation_f[f].append(init_wealth)

            f_expected_wealth[f] += init_wealth

        allFractionOutcomeOfEachExperiemnt.append(simulation_f)


    for f in f_range:
        try:
            mdd = allMDDOutcomeOfEachExperiment[numOfExp][f]
        
        except:
            if len(allMDDOutcomeOfEachExperiment) <= numOfExp:
                allMDDOutcomeOfEachExperiment.append({})
            
            mdd = abs(MDD(simulation_f[f]))
            allMDDOutcomeOfEachExperiment[numOfExp][f] = mdd

        if mdd < alpha:
            f_MDD_below_alpha[f] += increment
    
    return f_MDD_below_alpha, f_expected_wealth


def batchCalProbBelowAlphaOfEachF(experiments, f_range, numberOfExperiment, timePeriod, alpha, beta, f_MDD_below_alpha, f_expected_wealth):

    mode = 0

    if mode:
        # numpy
        transposeOfExperiments = np.array(experiments).T

        for f in f_range:
            
            init_wealth = np.ones(len(transposeOfExperiments[0]))
            wealthPath  = np.empty_like(transposeOfExperiments)
            
            for count, row in enumerate(transposeOfExperiments):
                init_wealth = init_wealth*(1+f*row)
                wealthPath[count] =  init_wealth

    else:
        # original version
        increment = 1/numberOfExperiment

        for count, experiment in enumerate(experiments):
            calProbBelowAlphaOfEachF(experiment, 
                            alpha,
                            f_range, 
                            f_MDD_below_alpha, 
                            f_expected_wealth,
                            increment,
                            count)
        
    return f_MDD_below_alpha, f_expected_wealth


def clean_f_MDD_below_alpha_for_graphing(f_MDD_below_alpha):
    
    # print out f which MDD is below alpha and prob is smaller than beta
    temp = list()

    for f in f_MDD_below_alpha:
        temp.append((f, f_MDD_below_alpha[f]))

    temp = sorted(temp)
    
    return temp


def buildFinalResult(purified_f_MDD_below_alpha, alpha):

    alpha_fraction_beta[str(alpha)] = {
        "fraction": [x[0] for x in purified_f_MDD_below_alpha], 
        "beta": [x[1] for x in purified_f_MDD_below_alpha]
        }


def data_to_graph(alpha, purified_f_MDD_below_alpha):

    plt.figure(1)
    plt.plot([x[0] for x in purified_f_MDD_below_alpha], 
             [x[1] for x in purified_f_MDD_below_alpha], 
             label="alpha = {}".format(alpha))  
    

def storeFinalRsult(alpha_fraction_beta, filename, prefix):
    
    today = datetime.today().date()

    try:
        with open(prefix + str(today) + filename,"w") as file:
            json.dump(alpha_fraction_beta, file, indent = 4)
    
    except FileNotFoundError:
        os.mkdir(prefix)
        with open(prefix + str(today) + filename,"w") as file:
            json.dump(alpha_fraction_beta, file, indent = 4)


def plot_info(timePeriod, numberOfExperiment, plt):
    
    plt.figure(1)
    plt.xlabel('fraction', fontsize=Plot.LABEL_SIZE)
    plt.ylabel('Prob(MDD < alpha)', fontsize=Plot.LABEL_SIZE)
    plt.xticks(size = Plot.TICK_SIZE)
    plt.yticks(size = Plot.TICK_SIZE)

    plt.text(0.5, 1.15, 'Experiments: {}, Plays: {}'.format(numberOfExperiment, timePeriod), 
    {'fontsize': 15})
    
    # plt.text(0.5, 1.1, 
    # 'Odds: {}'.format('Normal Distribution (mean = 0, std = 0.3333)'), 
    # {'fontsize': 15})

    plt.legend()
    plt.show()


if __name__ == '__main__':

    '''
    Input  : A simulated return path
    Process: Run all the possbile of fraction and alpha, and then calculate out the value of beta
    Output : A graph that x-axis is fraction and y-axis is beta (prob(MDD<alpha))
    '''
    dataLabel = "data"
    flagLabel = "flag"
    returnStyleLabel = "returnStyle"
    
    beta  =  0.1
    alpha = [x / 100 for x in range(0, 101, 10)]
    f_range  = [x / 100 for x in range(1, 99, 2)]
  
    tickers = ["1301", "1303", "1326", "2317", "2330", "2412", "2454", "2882", "3008", "6505"]
    ticker  = "2317"

    filename = "./data/"+ticker+"/simulated_rtn.json"
    prefix   = "./data/"+ticker+"/result/"
    
    onlyLoadData = 0
    alpha_fraction_beta = defaultdict(list)
    allFractionOutcomeOfEachExperiemnt = list()
    allMDDOutcomeOfEachExperiment      = list()
    experiments ,timePeriod, numberOfExperiment, returnStyle, flag = loadAllDataFromJson(filename)

    if not onlyLoadData:

        for alp in alpha:
            f_expected_wealth = defaultdict(lambda: 0)
            f_MDD_below_alpha = defaultdict(lambda: 0)

            batchCalProbBelowAlphaOfEachF(
                experiments,
                f_range,
                numberOfExperiment,
                timePeriod,
                alp,
                beta,
                f_MDD_below_alpha,
                f_expected_wealth
            )

            purified_f_MDD_below_alpha = clean_f_MDD_below_alpha_for_graphing(f_MDD_below_alpha)
            buildFinalResult(purified_f_MDD_below_alpha,alp)
            data_to_graph(
                alp,
                purified_f_MDD_below_alpha,
            )

        storeFinalRsult(alpha_fraction_beta, "alpha_fraction_beta.json", prefix)
        # optimal_f_to_graph(alpha_optimal_f)
        
        plot_info(
            timePeriod,
            numberOfExperiment,
            plt,
        
        )