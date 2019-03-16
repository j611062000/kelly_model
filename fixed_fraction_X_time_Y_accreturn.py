from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from numpy.random import choice

time = 100
prob = [0.5, 0.5]
return_vector = [3, 0]
fixed_fraction = 0.25
init_wealth = 1


def generate_flip_outcome(time, prob, return_vector):
    # retrun: a list of outcome which length is defined by time
    return [choice(return_vector, p=prob) for x in range(time)]


def cal_accum_return(fixed_fraction, init_wealth,flip_outcome):
    accum_return = [init_wealth]

    for outcome in flip_outcome:
        last_period_wealth = accum_return[-1]
        accum_return.append((1-fixed_fraction) * last_period_wealth + 
                             fixed_fraction*outcome*last_period_wealth)
    return accum_return, flip_outcome

def init_plot():
    p1 = figure(title="Accumulated Return")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Time Period'
    p1.yaxis.axis_label = 'Accumulated Return'
    return p1


def plot(accu_rtn, flip_outcome, p1):
    
    p1.line([x for x in range(time+1)],accu_rtn, color='#A6CEE3' )
    # p1.circle([x for x in range(time+1)],accu_rtn, color='#A6CEE3')
    # p1.circle([x for x in range(time+1)],flip_outcome, color='Red', legend='Sim_Outcome')

    return p1



def main():
    p1 = init_plot()
    for x in range(1):
        accu_rtn,  flip_outcome= cal_accum_return(fixed_fraction, init_wealth,generate_flip_outcome(time, prob, return_vector))
        # print(accu_rtn,  flip_outcome)

        p1 = plot(accu_rtn,  flip_outcome, p1)
    
    show(p1)


if __name__ == '__main__':
    main()
