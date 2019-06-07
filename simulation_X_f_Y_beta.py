import numpy
import json
import matplotlib.pyplot as plt
import time

from batchProcess import MDD
from collections import defaultdict
from loadDataFromJson import loadAllDataFromJson
from matplotlib.ticker import PercentFormatter
from multiprocessing import Pool
from numpy.random import choice


# TODO expected value

def calProbBelowAlphaOfEachF(simulation_path, alpha, f_range, f_MDD_below_alpha, f_expected_wealth,increment):
    """
    Input: simulation of return with specified time periods, and parameters of f
    Output: An individual simulation with f from 0.00~1.00

    """
    simulation_f = defaultdict(list)
    # numpy
    # wealthPath = numpy.zeros((timePeriod, numberOfExperiment))
    # numpy

    for f in f_range:
        
        
        
        init_wealth = 1

        # numpy 
        # def calWealth(rtn):
        #     return 1+f*rtn
        # init_wealth = numpy.ones((1, numberOfExperiment))
        # numpy 

        for outcome in simulation_path:
            # init_wealth = init_wealth * (1 - f) + init_wealth * f * (1+outcome)
            init_wealth = init_wealth*(1+f*outcome)
            simulation_f[f].append(init_wealth)

            # numpy 
            # init_wealth = numpy.append(init_wealth, init_wealth[-1]*calWealth(outcome),axis=0)
            # numpy

        f_expected_wealth[f] += init_wealth

    for f in f_range:
        if abs(MDD(simulation_f[f])) < alpha:
            f_MDD_below_alpha[f] += increment
    
    return f_MDD_below_alpha, f_expected_wealth

def batchCalProbBelowAlphaOfEachF(experiments, f_range, numberOfExperiment, timePeriod, alpha, beta, f_MDD_below_alpha, f_expected_wealth):

    increment = 1/numberOfExperiment
    # # [[Exp1(1)...ExpN(1)],...,[Exp1(K)...ExpN(K)]]
    # transposeAry = numpy.transpose(numpy.array(experiments))

    # calProbBelowAlphaOfEachF(transposeAry, 
    #                 alpha,
    #                 f_range, 
    #                 f_MDD_below_alpha, 
    #                 f_expected_wealth,
    #                 increment,
    #                 numberOfExperiment, 
    #                 timePeriod)

    for experiment in experiments:
        calProbBelowAlphaOfEachF(experiment, 
                        alpha,
                        f_range, 
                        f_MDD_below_alpha, 
                        f_expected_wealth,
                        increment)
        
    return f_MDD_below_alpha, f_expected_wealth

def data_to_graph(f_range, numberOfExperiment, beta, alpha, f_MDD_below_alpha, f_expected_wealth, prob=0):

    # print out f which MDD is below alpha and prob is smaller than beta
    temp = list()
    # alpha_optimal_f = f_with_max_return(f_range, numberOfExperiment, f_MDD_below_alpha, f_expected_wealth)

    for f in f_MDD_below_alpha:
        temp.append((f, f_MDD_below_alpha[f]))

    temp = sorted(temp)

    plt.figure(1)
    plt.plot([x[0] for x in temp], [x[1] for x in temp], label="alpha = {}".format(alpha))



def plot_info(timePeriod, numberOfExperiment, plt):
    plt.figure(1)
    plt.xlabel('fraction', fontsize=20)
    plt.ylabel('Prob(MDD < alpha)', fontsize=20)
    

    # plt.axhline(y=beta, linewidth=1, color='black')
    plt.text(0.5, 1.15, 'Experiments: {}, Plays: {}'.format(numberOfExperiment, timePeriod), 
    {'fontsize': 15})
    
    plt.text(0.5, 1.1, 
    'Odds: {}'.format('Normal Distribution (mean = 0, std = 0.3333)'), 
    {'fontsize': 15})

    # plt.gca().xaxis.set_major_formatter(PercentFormatter(1))
    plt.legend()
    plt.show()


if __name__ == '__main__':

    dataLabel = "data"
    flagLabel = "flag"
    returnStyleLabel = "returnStyle"
    beta  =  0.1
    alpha = [x / 100 for x in range(0, 100, 10)]
    # f_range = [0.624]
    f_range = [x / 100 for x in range(0, 101, 1)]
    filename = "./data/0050/0050_simulated_return.json"
    onlyLoadData = 1
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

            data_to_graph(
                f_range,
                numberOfExperiment,
                beta,
                alp,
                f_MDD_below_alpha,
                f_expected_wealth
            )

        # optimal_f_to_graph(alpha_optimal_f)
        
        plot_info(
            timePeriod,
            numberOfExperiment,
            plt,
        
        )
