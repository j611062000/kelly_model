from datetime import datetime
from numpy.random import normal

import json

# Generator of experiment path
def distribution_model(mean, std, time):

    return normal(mean, std, time)
    

def generate_normal_dist_to_jason(mean, std, num_of_exp,file_name, time):
    data = dict()
    with open(file_name+".json","w") as file:
        for exp in range(num_of_exp):
            data[str(exp+1)] = [x for x in distribution_model(mean, std, time)]
        
        dic = {
            "metaData":
                {
                    "mean":mean, 
                    "std":std, 
                    "num_of_exp":num_of_exp, 
                    "model":"normal",
                    "Time":str(datetime.today())
                },
            "data": data
            }
        json.dump(dic, file, indent = 4)

        
if __name__ == "__main__":
    mean = 0
    std = 0.1

    num_of_exp = 100
    time = 30
    file_name = "./data/normal_dist_"+str(num_of_exp)+"exps"
    generate_normal_dist_to_jason(mean, std, num_of_exp, file_name, time)
