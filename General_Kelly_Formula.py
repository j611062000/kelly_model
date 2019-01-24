from bokeh.plotting import figure, output_file, show
from datetime import datetime

import json
import operator


"""
API Key: 8BHO3DV69A6T0OPC
API: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=8BHO3DV69A6T0OPC&outputsize=full
Source: Alpha Vantage

TODO:
1.以一般化凱莉當作基礎，i.e. 報酬為b1,b2(見留言附圖) 
2.用停損停利當作報酬向量，進場訊號為ma5跟ma10的黃金交叉 
3.moving windows當作勝率的估計，所以下注比率會改變 
4.用台股模擬 
"""


class stock_price_data():

    def __init__(self, price_data, time_data):
        self.price_data = price_data
        self.time_data = time_data
        self.MA5 = None
        self.MA10 = None
        self.entry_signal = None

def is_stop_loss_or_win(holding_cost, current_price):
    current_return = (current_price-holding_cost)

def so_far_return(entry_signal, holding_cost, current_price, is_holding):
    assert entry_signal==0 or entry_signal==1
    assert is_holding==0 or is_holding==1

    if is_holding:


def cal_entry_signal(MA5, MA10):
    assert len(MA5) == len(MA10)
    entry_signal = list()
    # MA5 - MA10
    difference = list(map(operator.sub, MA5, MA10))

    for count, element in enumerate(difference):
        if element >=0 and difference[count-1]<0:
            entry_signal.append(100)
        else:
            entry_signal.append(0)
    return entry_signal


def plot(x, y, MA5, MA10, entry_signal, legend_of_data="0050", file_name="graph.html"):

    # create a HTML file
    output_file(file_name)

    # create a plot with labels specified
    p = figure(title="0050", x_axis_label="time",
               x_axis_type="datetime", y_axis_label="closing price", plot_width=1600, plot_height=800)

    # add data
    p.circle(x, y, legend=legend_of_data, size=4, color="darkgrey", alpha=0.2)
    p.vbar(x, width=0.5, bottom=0, top=entry_signal, color="#CAB2D6")

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
            MA.append(round(accu))

        else:
            MA.append(-1)

    return MA


def optimal_f_of_general_kelly(b1, b2, p):

    assert p < 1 and p > 0, "p is not appropriate!"
    return (b1*p-b2*(1-p))/(b1*b2)


def test():
    # test of MA
    # print(MA_with_specified_period(3, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

    # test of signal
    print(cal_entry_signal([1, 6, 10], [4, 5, 7]))


def main():
    # x:time, y: price

    x, y = extract_data_from_json()
    TW0050 = stock_price_data(y, x)
    TW0050.MA5 = MA_with_specified_period(5, y)
    TW0050.MA10 = MA_with_specified_period(10, y)
    TW0050.entry_signal = cal_entry_signal(TW0050.MA5,TW0050.MA10)


    plot(x, y, TW0050.MA5, TW0050.MA10, TW0050.entry_signal)


if __name__ == '__main__':
    main()
    # test()
