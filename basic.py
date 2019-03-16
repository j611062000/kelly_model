import json
with open("./data/5000_experiment.json", "r") as file:
            print(json.load(file).values())