"""
f_star = the fraction of the current bankroll to wager, i.e. how much to bet;

"""
import matplotlib.pyplot as plt

def optimal_f(return_vector = [-1, 1.68], prob_vector = [0.5, 0.5], division = 10000, plot = True):

    p = prob_vector[1]
    q = prob_vector[0]
    adjustment = 1 / division


    def result(fraction):
        result = ((1 + fraction * return_vector[1]) **p) * ((1 + fraction * return_vector[0])**q)
        return round(result, 10)

    x, y = [], []
    max_expected_return, f_star = 0, 0

    for fraction in range(division + 1):
        expected_return = result(fraction * adjustment)
        x.append(fraction * adjustment)
        y.append(expected_return)

        if expected_return > max_expected_return:
            max_expected_return = expected_return
            f_star = fraction * adjustment
    if plot:
        plt.plot(x, y, 'ro')
        plt.grid(True)
        plt.show()

    return [max_expected_return, f_star]

if __name__ == '__main__':
    pass