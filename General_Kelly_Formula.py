from bokeh.plotting import figure, output_file, show
from datetime import datetime

import json
import operator


"""
API Key: 8BHO3DV69A6T0OPC
API: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=8BHO3DV69A6T0OPC&outputsize=full
Source: Alpha Vantage

TODO:
0. refinement: price, MA5, MA10, gold_cross(bool), 

1. Price, MA5, MA10, gold cross with win or loss--> find out p
2. Price, gold cross with realized entry, total return 

"""

# one class stands for an underlying


class stock_price_data():

    def __init__(self):
        self.price_data = list()
        self.time_data = list()
        self.MA5 = list()
        self.MA10 = list()
        self.gold_cross = list()
        self.win_loss = None
        self.wealth = list()
# def extract_data_from_json(file_name="./data/0050_2008_2019_data.json",
#                            target_key="Time Series (Daily)",
#                            open_mode="r"):

#     x = list()
#     y = list()

#     with open(file_name, open_mode) as data_source:

#         value_of_daily_time_series = json.load(data_source)[target_key]

#         for daily_data in value_of_daily_time_series:
#             if float(value_of_daily_time_series[daily_data]["4. close"]) != 0:
#                 # x stores timestamp
#                 x.append(parse_time(daily_data))
#                 # y stores daily closing price
#                 y.append(
#                     float(value_of_daily_time_series[daily_data]["4. close"]))

#     return x[::-1], y[::-1]


# def MA_with_specified_period(days, data):

#     # The data should be asscending by date !
#     # based on rolling window
#     MA, accu = list(), 0

#     for count, element in enumerate(data):
#         accu += element/days
#         if count > days-1:
#             accu -= data[count-days]/days

#         if count >= days-1:
#             MA.append(accu)

#         else:
#             MA.append(-1)

#     return MA

# def cal_gold_cross(MA5, MA10, start=5):
#     assert len(MA5) == len(MA10)
#     gold_cross = [None]*start

#     # stores (MA5 - MA10) of each trading day
#     difference = list(map(operator.sub, MA5, MA10))

#     for count, element in enumerate(difference[start:]):
#         # if gold cross appears, then
#         if element > 0 and difference[count+start-1] <= 0:
#             gold_cross.append(True)
#         else:
#             gold_cross.append(False)
#     return gold_cross

# def dump_to_json(stock_price_data):
#     data = dict()
#     aggregation = zip(
#         stock_price_data.price_data,
#         stock_price_data.time_data,
#         stock_price_data.MA5,
#         stock_price_data.MA10,
#         stock_price_data.gold_cross,
#     )
#     for price, time, MA5, MA10, gold_cross in aggregation:
#         data[str(time)] = {
#             "price": price,
#             "MA5": MA5,
#             "MA10": MA10,
#             "gold_cross": gold_cross,
#         }

#     with open("./data/0050_refinement.json", "w") as file:
#         json.dump(data, file, indent = 4)

# def test():
#     # test of MA
#     stock_price = [100,10,10,11,15,1600,10,8,210]
#     print("stock_price:", stock_price)
#     MA3 = (MA_with_specified_period(3, stock_price))
#     MA5 = (MA_with_specified_period(5, stock_price))
#     print("MA3:", MA3)
#     print("MA5:", MA5)

#     # test of signal
#     signal = cal_gold_cross(MA3, MA5,3)
#     print("signal:",signal)

#     # test of is_stop_loss_or_win(holding_cost, current_price, stop_loss, take_profit)
#     # print(is_stop_loss_or_win(10, 2, -0.1, 0.1))

#     # so_far_return(holding_cost, current_price, stop_loss, take_profit)
#     # print(so_far_return(10, 12, -0.1, 0.1))

#     # cal_win_loss(stock_price, gold_cross, stop_loss, take_profit)
#     print("cal_win_loss:",cal_win_loss(stock_price, signal, -0.05, 0.05,3))

#     pass


def optimal_f_of_general_kelly(b1, b2, p):

    assert p < 1 and p > 0, "p is not appropriate!"
    return (b1*p-b2*(1-p))/(b1*b2)


def win_loss_refine(win_loss):
    def func(x):
        if x == True:
            return 100
        elif x == False:
            return -100
        elif x == "entry":
            return 50
        else:
            return 0

    return list(map(func, win_loss))


def cal_prob(stock_price, gold_cross, stop_loss, take_profit, start=5):
    win, loss = 0, 0
    total_cross = 0
    for count, cross in enumerate(gold_cross):
        if cross:
            total_cross += 1
            cross_price = stock_price[count]
            for price in stock_price[count:]:
                if (price-cross_price)/cross_price >= take_profit:
                    win += 1
                    break
                elif (price-cross_price)/cross_price <= stop_loss:
                    loss += 1
                    break
    # print("win:{}, loss:{}".format(win, loss))
    return (win/total_cross)


def cal_win_loss(stock_price, gold_cross, stop_loss, take_profit, p,SL_TP, return_threshold,start=5):
    is_holding = False
    holding_cost = 0
    win_loss = [None]*start
    init_wealth = 1
    f = optimal_f_of_general_kelly(take_profit, abs(stop_loss), p)

    for price, signal in zip(stock_price[start:], gold_cross[start:]):
        if signal == 100 and not is_holding:
            is_holding = True
            holding_cost = price
            win_loss.append("entry")

        elif is_holding:
            current_return = (price - holding_cost)/holding_cost
            if current_return >= take_profit:
                win_loss.append(True)
                is_holding = False
                init_wealth += init_wealth*f*take_profit
            elif current_return <= stop_loss:
                # print("current_return:",current_return)
                # print("price",price, "holding_cost",holding_cost)
                win_loss.append(False)
                is_holding = False

                init_wealth += init_wealth*f*stop_loss

            else:
                win_loss.append(None)
        else:
            # no signal and no holding
            win_loss.append(None)
    
    if init_wealth >=1 and init_wealth<1.05:
        SL_TP["1-1.05"].append([stop_loss, take_profit])
    elif init_wealth >=1.05 and init_wealth<1.1:
        SL_TP["1.05-1.1"].append([stop_loss, take_profit])
    elif init_wealth >=1.1 and init_wealth<1.15:
        SL_TP["1.1-1.15"].append([stop_loss, take_profit])
    elif init_wealth >=1.15 and init_wealth<1.2:
        SL_TP["1.15-1.2"].append([stop_loss, take_profit])

    elif init_wealth >=1.2:
        SL_TP["1.2-"].append([stop_loss, take_profit])

        # print("final wealth", init_wealth)
        # print("f", f)
        # print("stop_loss:{}, take_profit:{}".format(stop_loss, take_profit))

    return win_loss_refine(win_loss)


def plot_relation_stopLoss_takeProfit(return_threshold,SL_TP, file_name="./graph/relation_TP_SL.html"):
    output_file(file_name)

    p = figure(title="Relation of TakeProfit and StopLoss", x_axis_label="TakeProfit"
               , y_axis_label="StopLoss", plot_width=1600, plot_height=800)
    colors = ["red", "blue", "black", "green","darkgrey"]
    legends = ["1~1.05","1.05~1.1","1.1~1.15","1.15~1.2",">1.2"]
    for interval, color ,leg in zip(SL_TP,colors, legends):
        SL = [E[0] for E in SL_TP[interval]]
        TP = [E[1] for E in SL_TP[interval]]

        p.circle(TP, SL, legend="final wealth: {}".format(leg),
             size=20, color=color)

    show(p)

def plot(price, time, MA5, MA10, gold_cross, win_loss,
         legend_of_data="0050", file_name="./graph/0050.html"):

    # create a HTML file
    output_file(file_name)

    # confugured a new graph framework
    p = figure(title="0050", x_axis_label="time",
               x_axis_type="datetime", y_axis_label="closing price", plot_width=1600, plot_height=800)

    # draw closing price
    p.circle(time, price, legend="closing price",
             size=10, color="darkgrey", alpha=0.2)

    p.vbar(time, width=0.5, bottom=0, top=gold_cross,
           color="pink", legend="gold_cross")
    p.vbar(time, width=0.5, bottom=0, top=win_loss, color="black")
    # p.circle(time, gold_cross, legend="gold_cross", size=4, color="red", alpha=0.2)

    p.line(time, MA5, legend="MA5", line_width=2, color="yellow")
    p.line(time, MA10, legend="MA10", line_width=2, color="navy")

    # show the graph
    show(p)


def extract_data_from_refinement_json(file_name="./data/0050_refinement.json", open_mode="r"):

    def parse_time(time_as_string, format="%Y-%m-%d"):
        assert type(time_as_string) == str
        return datetime.strptime(time_as_string, format)

    TW0050 = stock_price_data()

    with open(file_name, open_mode) as data_source:
        value_of_daily_time_series = json.load(data_source)
        for daily_data in value_of_daily_time_series:
            TW0050.price_data.append(
                value_of_daily_time_series[daily_data]["price"])
            TW0050.time_data.append(parse_time(daily_data[:10]))
            TW0050.MA5.append(value_of_daily_time_series[daily_data]["MA5"])
            TW0050.MA10.append(value_of_daily_time_series[daily_data]["MA10"])
            if value_of_daily_time_series[daily_data]["gold_cross"]:
                TW0050.gold_cross.append(100)
            else:
                TW0050.gold_cross.append(0)

    return TW0050


def main(stop_loss=-0.2, take_profit=0.05):
    # x:time, y: price

    TW0050 = extract_data_from_refinement_json()
    # TW0050.MA5 = MA_with_specified_period(5, y)
    # TW0050.MA10 = MA_with_specified_period(10, y)
    # TW0050.gold_cross = cal_gold_cross(TW0050.MA5, TW0050.MA10)
    # dump_to_json(TW0050)
    SL_TP = {"1-1.05":[],"1.05-1.1":[],"1.1-1.15":[],"1.15-1.2":[],"1.2-":[]}
    # SL,TP = list(),list()
    return_threshold = 1.1
    for win in range(5, 101, 5):
        for loss in range(5, 101, 5):
            p = cal_prob(TW0050.price_data, TW0050.gold_cross, -
                         loss/100, win/100, start=10)

            TW0050.win_loss = cal_win_loss(
                TW0050.price_data,
                TW0050.gold_cross,
                -loss/100,
                win/100,
                p,
                SL_TP,
                return_threshold,
                10
            )
    # print(SL,TP)
    plot_relation_stopLoss_takeProfit(return_threshold,SL_TP)

    # plot(TW0050.price_data, TW0050.time_data, TW0050.MA5, TW0050.MA10, TW0050.gold_cross,TW0050.win_loss)


if __name__ == '__main__':
    # test()
    main()
