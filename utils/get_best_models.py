#!/usr/bin/env python3

# A script  for reading .json files from a folder and getting the best models from them using AFsample results

import os 
import sys
import json
import glob
import numpy as np

input_folder="/Users/pqh443/Documents/AFsample_results/Sweet_Thaumatin-II/"

# Look for .pkl.json files in the input folder and save them in a list using glob
json_files = glob.glob(os.path.join(input_folder, "*.pkl.json"))

# Get the file names from the list of .json files
file_names = [os.path.basename(json_file) for json_file in json_files]

# Get the "ranking_confidence" values from the .json files and save them in a dictionary where the key is the fille name without the extension
ranking_confidence = {}
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
        ranking_confidence[os.path.basename(json_file)[:-9]] = data["ranking_confidence"]

# Get top 10 best models based on ranking_confidence from the dictionary
best_models = sorted(ranking_confidence, key=ranking_confidence.get, reverse=True)[:10]

for model in best_models:
    name = model.replace("result", "unrelaxed")
    print(model, ranking_confidence[model])
    #print(f"load {name}.pdb")

print(np.mean(list(ranking_confidence.values())))
print(np.std(list(ranking_confidence.values())))