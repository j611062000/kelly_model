from bokeh.plotting import figure, output_file, show
from datetime import datetime

import json
import operator


"""
API Key: 8BHO3DV69A6T0OPC
API: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=8BHO3DV69A6T0OPC&outputsize=full
Source: Alpha Vantage

TODO:
a. general kelly, with alpha, beta--> what is the optimal RCF when given alpha, beta and general kelly?
b. mathematical model merged with general kelly f(p, b1,b2, alpha, beta, not l)
c. two outcome (TODO: multiple outcome)
d. theory-->ch3
e. experiment-->ch4

"""


class stock_price_data():

    def __init__(self, price_data, time_data):
        self.price_data = price_data
        self.time_data = time_data
        self.MA5 = None
        self.MA10 = None
        self.entry_signal = None
        self.win_loss = None

def win_loss_refine(win_loss):
    def func(x): 
        if x==True: 
            return 100
        elif x==False:
            return -100
        elif x=="entry":
            return 50
        else:
            return 0

    return list(map(func, win_loss))



def cal_win_loss(stock_price, entry_signal, stop_loss, stop_win, start=5):
    is_holding = False
    holding_cost = 0
    win_loss = [None]*start
    c=0
    for price, signal in zip(stock_price[start:], entry_signal[start:]):
        if signal==100 and not is_holding:
            is_holding = True
            holding_cost = price
            win_loss.append("entry")

        elif is_holding:
            current_return = (price - holding_cost)/holding_cost
            if current_return >= stop_win:
                win_loss.append(True)
                is_holding = False
            elif current_return <= stop_loss:
                # print("current_return:",current_return)
                # print("price",price, "holding_cost",holding_cost)
                win_loss.append(False)
                is_holding = False
            else:
                win_loss.append(None)


        else:
            # no signal and no holding
            win_loss.append(None)
    return win_loss_refine(win_loss)


def cal_entry_signal(MA5, MA10, start=5):
    assert len(MA5) == len(MA10)
    entry_signal = [None]*start
    # MA5 - MA10
    difference = list(map(operator.sub, MA5, MA10))
    # print("difference:",difference)

    for count, element in enumerate(difference[start:]):
        # print(count, element,difference[count+start-1])
        if element > 0 and difference[count+start-1] <= 0:
            entry_signal.append(100)
        else:
            entry_signal.append(0)
    return entry_signal


def plot(x, y, MA5, MA10, entry_signal,win_loss, 
    legend_of_data="0050", file_name="graph.html"):

    # create a HTML file
    output_file(file_name)

    # create a plot with labels specified
    p = figure(title="0050", x_axis_label="time",
               x_axis_type="datetime", y_axis_label="closing price", plot_width=1600, plot_height=800)

    # add data
    p.circle(x, y, legend=legend_of_data, size=10, color="darkgrey", alpha=0.2)
    p.vbar(x, width=0.5, bottom=0, top=entry_signal, color="#CAB2D6")
    p.vbar(x, width=0.5, bottom=0, top=win_loss, color="red")


    # p.circle(x, entry_signal, legend="entry_signal", size=4, color="red", alpha=0.2)

    p.line(x, MA5, legend="MA5", line_width=2, color="yellow")
    p.line(x, MA10, legend="MA10", line_width=2, color="navy")

    # show the graph
    show(p)


def parse_time(time_as_string, format="%Y-%m-%d"):

    assert type(time_as_string) == str
    return datetime.strptime(time_as_string, format)


def extract_data_from_json(file_name="0050_2008_2019_data.json",
                           target_key="Time Series (Daily)",
                           open_mode="r"):

    x = list()
    y = list()

    with open(file_name, open_mode) as data_source:

        value_of_daily_time_series = json.load(data_source)[target_key]

        for daily_data in value_of_daily_time_series:
            if float(value_of_daily_time_series[daily_data]["4. close"]) != 0:
                x.append(parse_time(daily_data))
                y.append(
                    float(value_of_daily_time_series[daily_data]["4. close"]))

    return x[::-1], y[::-1]


def MA_with_specified_period(days, data):

    # The data should be asscending by date !
    # based on rolling window
    MA, accu = list(), 0

    for count, element in enumerate(data):
        accu += element/days
        if count > days-1:
            accu -= data[count-days]/days

        if count >= days-1:
            MA.append(accu)

        else:
            MA.append(-1)

    return MA


def optimal_f_of_general_kelly(b1, b2, p):

    assert p < 1 and p > 0, "p is not appropriate!"
    return (b1*p-b2*(1-p))/(b1*b2)


def test():
    # test of MA
    stock_price = [100,10,10,11,15,1600,10,8,210]
    print("stock_price:", stock_price)
    MA3 = (MA_with_specified_period(3, stock_price))
    MA5 = (MA_with_specified_period(5, stock_price))
    print("MA3:", MA3)
    print("MA5:", MA5)

    # test of signal
    signal = cal_entry_signal(MA3, MA5,3)
    print("signal:",signal)

    # test of is_stop_loss_or_win(holding_cost, current_price, stop_loss, stop_win)
    # print(is_stop_loss_or_win(10, 2, -0.1, 0.1))

    # so_far_return(holding_cost, current_price, stop_loss, stop_win)
    # print(so_far_return(10, 12, -0.1, 0.1))

    # cal_win_loss(stock_price, entry_signal, stop_loss, stop_win)
    print("cal_win_loss:",cal_win_loss(stock_price, signal, -0.05, 0.05,3))

    pass


def dump_to_json(stock_price_data):
    data = dict()
    aggregation = zip(
        stock_price_data.price_data,
        stock_price_data.time_data,
        stock_price_data.MA5,
        stock_price_data.MA10,
        stock_price_data.entry_signal,
    )
    for price, time, MA5, MA10, signal in aggregation:
        data[str(time)] = {
            "price": price,
            "MA5": MA5,
            "MA10": MA10,
            "signal": signal,
        }

    with open("0050_refinement.json", "w") as file:
        json.dump(data, file)


def main():
    # x:time, y: price

    x, y = extract_data_from_json()
    TW0050 = stock_price_data(y, x)
    TW0050.MA5 = MA_with_specified_period(5, y)
    TW0050.MA10 = MA_with_specified_period(10, y)
    TW0050.entry_signal = cal_entry_signal(TW0050.MA5, TW0050.MA10)
    TW0050.win_loss = cal_win_loss(
        TW0050.price_data, 
        TW0050.entry_signal,
        -0.05,
        0.05,
        10
        )
    # print(TW0050.win_loss)

    plot(x, y, TW0050.MA5, TW0050.MA10, TW0050.entry_signal,TW0050.win_loss)


if __name__ == '__main__':
    # TODO: win/loss/entry
    main()
    # test()
