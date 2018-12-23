import matplotlib.pyplot as plt
from numpy.random import choice
from random import uniform
from collections import defaultdict
from itertools import repeat

"""
To do: 1. alpha 2. equation 3.plot
Given: alpha and beta 
Goal: By simulation, figure out the f_star which fulfulls the constraint, P( MDD < alpha ) < beta.
element of return_vector is in [0,1]
Todo: expected return
"""


def MDD(prices):
    """
    data: a list stores the wealth(i), i=1~n
    definition of MDD: (price-high)/high
    """

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


# not yet: why there is no 0~0.5
def f_with_max_return(f_range, number_of_experiment,f_MDD_below_alpha, f_expected_wealth):

    max_f = 0
    LTBeta = lambda f, f_MDD_below_alpha: True if (
        f_MDD_below_alpha[f] / number_of_experiment) >= beta else False

    for f in f_MDD_below_alpha:
        if not LTBeta(f, f_MDD_below_alpha) and f_expected_wealth[f] > f_expected_wealth[max_f]:
            max_f = f
    return max_f


def simulation_of_return(return_vector, prob_vector, time_period):
    return [choice(return_vector, p=prob_vector) for x in range(time_period)]


def simulation_of_f(simulation_path, alpha, f_range,f_MDD_below_alpha, f_expected_wealth):
    """
    Input: simulation of return with specified time periods, and parameters of f
    Output: An individual simulation with f from 0.00~1.00

    """
    simulation_f = defaultdict(list)

    # accumulation of wealth given specified f
    for f in f_range:
        init_wealth = 1
        for outcome in simulation_path:
            init_wealth = init_wealth * (1 + f * (outcome - 1))
            simulation_f[f].append(init_wealth)

        f_expected_wealth[f] += init_wealth

    # account the number of f which is below the alpha
    for f in f_range:
        if 1 - abs(MDD(simulation_f[f])) < alpha:
            f_MDD_below_alpha[f] += 1


def f_star(experiments,f_range, number_of_experiment, time_period, return_vector, prob_vector, alpha, beta, f_MDD_below_alpha, f_expected_wealth):
    
    for index in range(0, len(experiments), 4):
        simulation_of_f(experiments[index], alpha, f_range,f_MDD_below_alpha, f_expected_wealth)
        simulation_of_f(experiments[index + 1], alpha, f_range,f_MDD_below_alpha, f_expected_wealth)
        simulation_of_f(experiments[index + 2], alpha, f_range,f_MDD_below_alpha, f_expected_wealth)
        simulation_of_f(experiments[index + 3], alpha, f_range,f_MDD_below_alpha, f_expected_wealth)


def data_to_graph(f_range,number_of_experiment, beta, alpha, f_MDD_below_alpha, f_expected_wealth):
    """
    print out f which MDD is below alpha and prob is smaller than beta
    """
    temp = []
    alpha_optimal_f = f_with_max_return(f_range, number_of_experiment, f_MDD_below_alpha, f_expected_wealth)
    prob = 0

    for f in f_MDD_below_alpha:
        if f == alpha_optimal_f:
            prob = f_MDD_below_alpha[f] / number_of_experiment
        temp.append((f, f_MDD_below_alpha[f] / number_of_experiment))
    temp = sorted(temp)

    # printout each data
    # for data in temp:
    #     print("f:{}, Prob.:{}, Wealth:{}".format(
    #         round(data[0], 4), data[1], f_expected_wealth[data[0]]))
    with plt.style.context('ggplot'):
        plt.plot([x[0] for x in temp], [x[1] for x in temp],label="alpha = {}".format(alpha))
        # plt.plot(alpha_optimal_f, prob, 'bp', markersize=14)


       
# def optimal_f_to_graph(alpha_optimal_f):
#     temp = []
#     for alpha in alpha_optimal_f:
#         temp.append((alpha_optimal_f[alpha], alpha))

#     temp = sorted(temp, key = lambda x:x[0])
#     for pair in temp:





def plot_info(time_period,number_of_experiment, plt, f_with_max_return):
    plt.xlabel('fraction (time_period = {})'.format(time_period), fontsize=30)
    plt.ylabel('Prob(MDD < alpha)', fontsize=30)

    # plt.axhline(y=beta, linewidth=1, color='black')
    plt.text(0.5, 0.6, 'Number of experiments is {}'.format(
        number_of_experiment), {'fontsize': 25})
    plt.legend()


    plt.show()

if __name__ == '__main__':

    """
    alpha: 0~1, precision = 100
    beta: 0~1, precision = 100
    time_period = range(10,51,10)
    risk_constrained_f (f_star)= f(alpha, beta, time_period, number_of_experiments)
    """
    
    return_vector = [0, 3]
    alpha_optimal_f = {}
    alpha, beta,  = [x / 100 for x in range(10, 99,10)], 0.1
    f_range = [x / 100 for x in range(0, 101)]
    number_of_experiment = 10000
    T = [30]
    prob_vector = [1 / len(return_vector)] * len(return_vector)
    for time_period in T:
        experiments = [simulation_of_return(
        return_vector, prob_vector, time_period) for i in range(number_of_experiment)]
       
        for alp in alpha:
            f_MDD_below_alpha,f_expected_wealth = defaultdict(lambda: 0),defaultdict(lambda: 0)
            f_star(experiments,f_range, number_of_experiment, time_period,return_vector, prob_vector, alp, beta, f_MDD_below_alpha, f_expected_wealth)
            data_to_graph(f_range,number_of_experiment, beta, alp,f_MDD_below_alpha, f_expected_wealth)
       
        # optimal_f_to_graph(alpha_optimal_f)
        plot_info(time_period,number_of_experiment, plt, f_with_max_return(f_range, number_of_experiment, f_MDD_below_alpha, f_expected_wealth))
