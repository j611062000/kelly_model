import json
import matplotlib.pyplot as plt

from collections import defaultdict
from numpy.random import choice

# def simulation_of_return(return_vector, prob_vector, time_period):
#     """
#     This function generates the simulation of return with the following given arguments.
#     Input: return vector, probability vector and time period.
#     Output: A list with "time_period" elements.
#     """
#     return [choice(return_vector, p=prob_vector) for x in range(time_period)]

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


# def f_with_max_return(f_range, number_of_experiment, f_MDD_below_alpha, f_expected_wealth, beta,max_f=0):

#     # verify if the prob. of f is greater than beta.
#     def GTBeta(f, f_MDD_below_alpha):
#         if (f_MDD_below_alpha[f] / number_of_experiment) >= beta:

#             return True

#         else:

#             return False

#     # find out the f with maximum expected return
#     for f in f_MDD_below_alpha:
#         if not GTBeta(f, f_MDD_below_alpha) and f_expected_wealth[f] > f_expected_wealth[max_f]:
#             max_f = f

#     return max_f


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
            # init_wealth = init_wealth * (1 + f * (outcome - 1))
            simulation_f[f].append(init_wealth)

        f_expected_wealth[f] += init_wealth

    # counting the number of f which is below the alpha
    for f in f_range:
        if abs(MDD(simulation_f[f])) < alpha:

            f_MDD_below_alpha[f] += 1


def f_star(experiments, f_range, number_of_experiment, time_period, alpha, beta, f_MDD_below_alpha, f_expected_wealth):

    for index in range(0, len(experiments)):
        simulation_of_f(experiments[index], 
                        alpha,
                        f_range, 
                        f_MDD_below_alpha, 
                        f_expected_wealth)
        # simulation_of_f(experiments[index + 1], alpha,
        #                 f_range, f_MDD_below_alpha, f_expected_wealth)
        # simulation_of_f(experiments[index + 2], alpha,
        #                 f_range, f_MDD_below_alpha, f_expected_wealth)
        # simulation_of_f(experiments[index + 3], alpha,
        #                 f_range, f_MDD_below_alpha, f_expected_wealth)


def data_to_graph(f_range, number_of_experiment, beta, alpha, f_MDD_below_alpha, f_expected_wealth, prob=0):

    # print out f which MDD is below alpha and prob is smaller than beta
    temp = []
    # alpha_optimal_f = f_with_max_return(f_range, number_of_experiment, f_MDD_below_alpha, f_expected_wealth)

    for f in f_MDD_below_alpha:
        # if f == alpha_optimal_f:
            # prob = f_MDD_below_alpha[f] / number_of_experiment
        temp.append((f, f_MDD_below_alpha[f] / number_of_experiment))
    temp = sorted(temp)

    plt.figure(1)
    plt.plot([x[0] for x in temp], [x[1]
                                    for x in temp], label="alpha = {}".format(alpha))

    # plot
    # plt.figure(2)
    # for f in f_expected_wealth:
    #     x_data, y_data = f, f_expected_wealth[f]
    # plt.plot(x_data, y_data , label="alpha = {}".format(alpha))


def plot_info(time_period, number_of_experiment, plt):
    plt.figure(1)
    plt.xlabel('fraction', fontsize=20)
    plt.ylabel('Prob(MDD < alpha)', fontsize=20)

    # plt.axhline(y=beta, linewidth=1, color='black')
    plt.text(0.5, 1.15, 'Experiments: {}, Plays: {}'.format(number_of_experiment, time_period), 
    {'fontsize': 15})
    
    plt.text(0.5, 1.1, 
    'Odds: {}'.format('Normal Distribution (mean = 0, std = 0.3333)'), 
    {'fontsize': 15})
    
    plt.legend()

    plt.show()


if __name__ == '__main__':

    """
    alpha: 0~1, precision = 100
    beta: 0~1, precision = 100
    time_period = range(10,51,10)
    risk_constrained_f (f_star)= f(alpha, beta, time_period, number_of_experiments)
    """
    alpha_optimal_f = dict()
    alpha = [x / 100 for x in range(10, 99, 10)]
    beta  =  0.1
    f_range = [x / 100 for x in range(0, 101)]
    number_of_experiment = 10000
    time_period = 30

    with open("./data/normal_dist_"+str(number_of_experiment)+"exps.json", "r") as file:
        data = json.load(file)["data"]
        experiments = [data[x] for x in data]
        # print(experiments)


    for alp in alpha:
        # f_MDD_below_alpha: storing how many times of every f which is below MDD
        f_expected_wealth =  defaultdict(lambda: 0)
        f_MDD_below_alpha = defaultdict(lambda: 0)

        f_star(
            experiments,
            f_range,
            number_of_experiment,
            time_period,
            alp,
            beta,
            f_MDD_below_alpha,
            f_expected_wealth
        )

        data_to_graph(
            f_range,
            number_of_experiment,
            beta,
            alp,
            f_MDD_below_alpha,
            f_expected_wealth
        )

    # optimal_f_to_graph(alpha_optimal_f)
    plot_info(
        time_period,
        number_of_experiment,
        plt,
        # f_with_max_return(
        #     f_range,
        #     number_of_experiment,
        #     f_MDD_below_alpha,
        #     beta,
        #     f_expected_wealth
        # )
    )
    # print(f_MDD_below_alpha)