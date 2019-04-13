import json
import matplotlib.pyplot as plt
import time

from collections import defaultdict
from loadDataFromJson import loadAllDataFromJson
from matplotlib.ticker import PercentFormatter
from multiprocessing import Pool
from numpy.random import choice


def MDD(prices, maxDrawdown=0):
    """
    data: a list stores the wealth(i), i=1~n
    definition of MDD: (price-high)/high
    """
    high = prices[0]
    for price in prices:
        if price == 0:
            # you lose all wealth when second round (=prices[0])
            return -1

        elif high > price:
            maxDrawdown = min(maxDrawdown, (price - high) / high)

        else:
            high = price

    return maxDrawdown



def simulation_of_f(simulation_path, alpha, f_range, f_MDD_below_alpha, f_expected_wealth):
    """
    Input: simulation of return with specified time periods, and parameters of f
    Output: An individual simulation with f from 0.00~1.00

    """
    simulation_f = defaultdict(list)

    # accumulation of wealth given specified f
    for f in f_range:
        init_wealth = 1
        for outcome in simulation_path:
            init_wealth = init_wealth * (1 - f) + init_wealth * f * (1+outcome)
            simulation_f[f].append(init_wealth)

        f_expected_wealth[f] += init_wealth

    # counting the number of f which is below the alpha
    increment = 1/numberOfExperiment

    for f in f_range:
        if abs(MDD(simulation_f[f])) < alpha:
            f_MDD_below_alpha[f] += increment

def f_star(experiments, f_range, numberOfExperiment, timePeriod, alpha, beta, f_MDD_below_alpha, f_expected_wealth):

    for index in range(0, len(experiments)):
        simulation_of_f(experiments[index], 
                        alpha,
                        f_range, 
                        f_MDD_below_alpha, 
                        f_expected_wealth)
        


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

    start_time = time.time()

    dataLabel = "data"
    flagLabel = "flag"
    returnStyleLabel = "returnStyle"

    beta  =  0.1
    alpha = [x / 100 for x in range(0, 100, 10)]
    f_range = [0.624]
    # f_range = [x / 100 for x in range(0, 101, 1)]
    
    filename = "./data/0050/0050_simulated_return.json"
    
    onlyLoadData = 1

    argsForLoadDataFromJson = [dataLabel, flagLabel, returnStyleLabel, filename]
    experiments ,timePeriod, numberOfExperiment, returnStyle, flag = loadAllDataFromJson(*argsForLoadDataFromJson)

    if not onlyLoadData:

        for alp in alpha:
            f_expected_wealth = defaultdict(lambda: 0)
            f_MDD_below_alpha = defaultdict(lambda: 0)

            f_star(
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
        print("--- %s seconds ---" % (time.time() - start_time))
        
        plot_info(
            timePeriod,
            numberOfExperiment,
            plt,
        
        )
