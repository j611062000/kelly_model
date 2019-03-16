x = [
        3,
        0,
        3,
        0,
        0,
        3,
        3,
        3,
        0,
        0,
        0,
        3,
        0,
        3,
        3,
        3,
        0,
        3,
        3,
        3
    ]
y = [
        3,
        0,
        0,
        3,
        0,
        3,
        0,
        0,
        3,
        0,
        0,
        3,
        3,
        3,
        3,
        3,
        3,
        0,
        3,
        3
    ]

def cal_price(outcomes, init_wealth, fixed_fraction):
    tmp = [1]
    for outcome in outcomes:
        last_return = tmp[-1]
        tmp.append((1-fixed_fraction) * last_return + (fixed_fraction*outcome*last_return))
        print((1-fixed_fraction) * last_return, (fixed_fraction*outcome*last_return))
    return tmp
print(cal_price(x,1,0.2))

print(cal_price(y,1,0.2))
