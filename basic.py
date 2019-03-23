from bokeh.plotting import figure, output_file, show
from numpy.random import choice
import json

# Generator of experiment path



import json
with open("./data/5000_experiment.json", "r") as file:
            print(json.load(file).values())