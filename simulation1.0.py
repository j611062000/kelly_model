import matplotlib.pyplot as plt
from numpy.random import choice
from collections import defaultdict

# input: list containing prices


def Cal_MDD(prices):
    high = prices[0]
    maxDrawdown = 0
    for price in prices:
        if price == 0:
            return maxDrawdown
        elif high > price:
            maxDrawdown = min(maxDrawdown, (price - high) / high)
        else:
            high = price

    return maxDrawdown


def is_MDD_LT_Alpha(MDD_Value, alpha):
    return True if 1 - abs(MDD_Value) < alpha else False

# output: expirements


def simulation_of_return(return_vector, prob_vector, time_period, number_of_experiment):
    return [[choice(return_vector, p=prob_vector) for x in range(time_period)] for i in range(number_of_experiment)]


def alpha_curve_dic(f_range, number_of_experiment, time_period, return_vector, prob_vector, alpha, beta):
    experiments = simulation_of_return(return_vector, prob_vector, time_period, number_of_experiment)
    dic_f_MDD = defaultdict(list)
    for f in f_range:
        dic_f_MDD[f] = list(map(Cal_MDD, ))



if __name__ == '__main__':

    time_period = 20
    return_vector = [0, 3]
    number_of_experiment = 10
    alpha, beta,  = [0.5], 0.1
    f_range = [x / 100 for x in range(0, 101)]
    prob_vector = [1 / len(return_vector)] * len(return_vector)

    alpha_curve_dic(f_range, number_of_experiment, time_period,
                    return_vector, prob_vector, alpha, beta)

    """
    logic: 
    1. generating experiments
    
    2. f from 0 to 1:
        find out MDD of specified f (say f') and corresponding final wealth : ( MDD(i,f'), final_wealth(i,f') ), 
        i and f' stands for ith experiment and f = f' respectively
        --> DS: dic[ f: [ MDD(1), ..., MDD(n) ]]

    
    3. alpha from start to end:
        say current alpha is 0.5, 
        
        for every f:
            say current f is f'', 

            find out the prob ( MDD < 0.5 ) = p(f'', 0.5) 
            --> DS: dic[ alpha: [ p(f1,alpha), ..., p(f100,alpha) ]]

    output = prob ( MDD < alpha ) < beta, alpha = 0, 0.1, 0.2, ..., 1
    """
