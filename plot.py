from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.models import Span, Range1d, LinearAxis
from loadDataFromJson import loadJson

import json

COLOR_OF_DATA = "Red"
COLOR_OF_SUB_DATA = "Red"
GRID_LINE_ALPHA = 0.3
SIZE_OF_DOT = 4
SUB_Y_AXIS_POSITION = "Right"




def generateVanilaDotGraph(desiredTitle, xLabel, yLabel, Xs, Ys, legenOfData, ifWithLine, colors = COLOR_OF_DATA):

    dotGraph = figure(title=desiredTitle, x_axis_label = xLabel, y_axis_label = yLabel)

    assert(len(Xs) == len(Ys))
    dotGraph.circle(Xs, Ys, fill_color=COLOR_OF_DATA, legend=legenOfData, size = SIZE_OF_DOT)

    show(dotGraph)

def generateDotGraphWithSubYAxis(dotGraph, Xs, mainYRange, subYRange, subYLabel, subYData, legendOfSubData):
    
    dotGraph.y_range = Range1d(start=mainYRange[0], end=mainYRange[1])
    dotGraph.extra_y_ranges = {subYLabel: Range1d(start=subYRange[0], end=subYRange[1])}
    dotGraph.add_layout(LinearAxis(y_range_name = subYLabel, axis_label=subYLabel), SUB_Y_AXIS_POSITION)
    dotGraph.circle(Xs, subYData, color = COLOR_OF_SUB_DATA, legend=legendOfSubData, size = SIZE_OF_DOT, y_range_name=subYLabel)

    return dotGraph

def calAbsValue(dic, isAbs = 0):
    tmp = list()
    for key in dic:
        if isAbs:
            appendData = abs(dic[key])
        else:
            appendData = dic[key]
        tmp.append(appendData)
    return tmp

# def f_MDD_HPR_single_asset(f, MDD,HPR):

#     p1.y_range = Range1d(start=-0.6, end=0)
#     p1.extra_y_ranges = {"HPR": Range1d(start=0.988, end=1.001)}
#     p1.add_layout(LinearAxis(y_range_name="HPR", axis_label='HPR'), 'right')

#     p1.circle(f,MDD, color='#A6CEE3', legend='MDD', size = 4)
#     p1.circle(f,HPR, color='red', legend='HPR', size = 4, y_range_name="HPR")

#     show(p1)
# class InitializationOfPlot():
#     def __init__(self, xLabel, yLabel,desiredTitle, legenOfData, colorOfData):
#         self.xLabel = xLabel
#         self.yLabel = yLabel
#         self.desiredTitle = desiredTitle
#         self.legenOfData = legenOfData
#         self.colorOfData = colorOfData

#         return figure

# def intervalBarGrap(intervalString, yDataxLabel, yLabel,desiredTitle, legenOfData, colorOfData):
#     counts = [5, 3, 4, 2, 4, 6]
#     p = figure(x_range=fruits, plot_height=250, title="Fruit Counts",
#             toolbar_location=None, tools="")
#     p.vbar(x=intervalString, top=counts, width=0.9)
#     p.xgrid.grid_line_color = None
#     p.y_range.start = 0

#     show(p)

#     return circleGraph


# def plot(RTN, MDD, alpha, beta,T):

#     p1 = figure(title="RTN x MDD, P(MDD<{}) = {}, Time_Period = {}, # of experiment = {}".format(abs(alpha), beta, T, 10000))
#     p1.grid.grid_line_alpha=0.3
#     p1.xaxis.axis_label = 'RTN'
#     p1.yaxis.axis_label = 'MDD'
#     # p1.line(RTN,MDD, color='#A6CEE3', legend='Accu_Rtn')
#     p1.circle(RTN,MDD, color='#A6CEE3', legend='MDD', size = 4)
#     hline = Span(location=-0.3, dimension='width', line_color='green', line_width=3)
#     p1.renderers.extend([hline])

#     return p1

# def main():
    
#     tmp = list()
#     T = 30
#     file_name = "10000_T"+str(T)
#     with open("./data/"+file_name+"_experiment_MDD.json", "r") as MDD:
#         MDD_data = json.load(MDD)

#     with open("./data/"+file_name+"_experiment_finalRtn.json","r") as finalRtn:
#         finalRtn_data = json.load(finalRtn)
#     for x in range(len(MDD_data)):
#         tmp.append((finalRtn_data[str(x)], MDD_data[str(x)]))
#     tmp.sort(key = lambda x:x[0] ) 
#     X = [x[0] for x in tmp]
#     Y = [x[1] for x in tmp]
    
#     c = 0
#     alpha = -0.3
#     for mdd in Y:
#         if mdd>alpha:
#             c+=1
#     p = plot(X,Y,alpha, c/10000, T)
#     show(p)
#     # print(c)


if __name__ == '__main__':
    # main()
    # fraction = list()
    # HPR = list()
    # MDD = list()
    # with open("./data/0050/0050_f_With_MDD.json", "r") as file:
    #     data = json.load(file)
    #     for f in data:
    #         fraction.append(float(f)/100)
    #         MDD.append(data[f])
    # with open("./data/0050/0050_HPR_and_f.json", "r") as file:
    #     data = json.load(file)
    #     for f in data:
    #         HPR.append(data[f])
    # f_MDD_HPR_single_asset(fraction, MDD,HPR)
    
    with open("./data/0050/backTesting/0050_yearly_fraction_MDD.json", "r") as file:
        data = json.load(file)
        tmp = list()
        for i in range(0,100):
            tmp.append(data[str(i)])
        
    Ys = tmp
    Xs = [x/100 for x in range(0,100)]
    xLabel = "Fraction"
    yLabel = "MDD"
    desiredTitle = yLabel+" x "+xLabel
    legenOfData = yLabel
    generateVanilaDotGraph(desiredTitle, xLabel, yLabel, Xs, Ys, legenOfData, 0)
