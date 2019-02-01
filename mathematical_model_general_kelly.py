from bokeh.plotting import figure, output_file, show
from bokeh.models import BoxAnnotation, Range1d, LinearAxis

from functools import reduce
from math import log

import operator as op


def plot(x, alpha, beta, b1, b2, time_period, *y_data):

    # create a HTML file
    output_file("graph.html")

    # create a plot with labels specified
    _title = "alpha:{}, beta:{}, b1:{}, b2:{}, time_period:{}".format(
        alpha, beta, b1, b2, time_period)
    p = figure(title=_title, x_axis_label="l",
               plot_width=1600, plot_height=800, y_range=(0, 0.2))

    # add data
    p.circle(x, y_data[0], legend="final_wealth",
             size=10, color="darkgrey", alpha=0.8)

    # color area
    # p.add_layout(BoxAnnotation(top=beta, fill_alpha=0.08, fill_color='green', line_color='red'))

    # twin y_axis
    p.extra_y_ranges = {"foo": Range1d(start=0, end=0.2)}
    p.add_layout(LinearAxis(y_range_name="foo"), 'left')
    p.circle(x, y_data[1], legend="f", size=10, color="blue", alpha=0.8,)
    p.circle(x, y_data[2], legend="prob_of_MDD",
             size=10, color="red", alpha=0.8)

    # show the graph
    show(p)


def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


def most_suitable_f(alpha, number_of_consecutive_loss):
    # b1: return of win
    # b2: return of loss
    return 1-(1-alpha)**(1/number_of_consecutive_loss)


def final_wealth(alpha, beta, b1, b2, prob_of_win, number_of_consecutive_loss):
    # f = most_suitable_f(alpha, beta, b1, b2, prob_of_win)
    # return log(A(T)/A(0))
    f = 1-(1-alpha)**(1/number_of_consecutive_loss)

    win_part = prob_of_win*log(1 + b2*f, 10)
    loss_part = (1-prob_of_win)*log(1 - b1*f, 10)
    return win_part+loss_part


def test_final_wealth():
    # relation of number_of_consecutive_loss and final_wealth
    alpha = 0.9999999
    beta = 1
    b1 = 1
    b2 = 2
    prob_of_win = 0.5
    time_period = 1000

    def sigma(T, i, p): return ncr(T, i)*(p**(i))*((1-p)**(T-i))
    wealth, f, prob_of_MDD = list(), list(
    ), [1-sigma(time_period, 0, prob_of_win)]

    for l in range(1, time_period):
        wealth.append(final_wealth(alpha, beta, b1, b2, prob_of_win, l))
        f.append(most_suitable_f(alpha, l))
        prob_of_MDD.append(prob_of_MDD[-1]-sigma(time_period, l, prob_of_win))

    plot(range(1, time_period), alpha, beta, b1,
         b2, time_period, wealth, f, prob_of_MDD)


def main():
    def sigma(T, i, p): return ncr(T, i)*(p**(i))*((1-p)**(T-i))

    print(1-sigma(40, 1, 0.5))


if __name__ == '__main__':
    test_final_wealth()
    # main()
