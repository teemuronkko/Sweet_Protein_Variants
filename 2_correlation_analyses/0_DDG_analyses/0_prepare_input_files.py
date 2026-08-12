import pandas as pd
import numpy as np
import csv
import os
import glob

# Get path to repository
repo_name = "Sweet_Protein_Variants"
current_path = os.path.abspath(__file__)
repo_path = current_path.split(repo_name)[0] + repo_name
variants_path = f"{repo_path}/1_variant_data/variants with parameters.xlsx"
ddg_path = f"{repo_path}/2_correlation_analyses/0_DDG_analyses"

# Read updated tsv file containing information about the variants
variants = pd.read_excel(variants_path)
variants = variants.replace(' ', '-', regex=True)
variants["protein_id"] = variants["protein"] + "_" + variants["strain"]

# Replace _, _ and , characters in the mutation field
variants["mutation"] = variants["mutation"].replace('_', '; ', regex=True)
variants["mutation"] = variants["mutation"].replace('-', '', regex=True)
variants["mutation"] = variants["mutation"].replace(',', '; ', regex=True)
variants = variants.rename(columns={"Tm": "Tm_1", 
                         "Unnamed: 7": "Tm_2", 
                         "average": "Tm_average",
                         "acetonitrile 0,8%": "acetonitrile_1",
                         "Unnamed: 10": "acetonitrile_2",
                         "average.1": "acetonitrile_average",
                         "wb": "western_blot",
                        })

# Replace commas with dots in T_m and 
variants["Tm_1"] = [str(i).replace(",", ".") for i in variants["Tm_1"]]
variants["Tm_2"] = [str(i).replace(",", ".") for i in variants["Tm_2"]]
variants["Tm_average"] = [str(i).replace(",", ".") for i in variants["Tm_average"]]
variants["acetonitrile_1"] = [str(i).replace(",", ".") for i in variants["acetonitrile_1"]]
variants["acetonitrile_2"] = [str(i).replace(",", ".") for i in variants["acetonitrile_2"]]
variants["acetonitrile_average"] = [str(i).replace(",", ".") for i in variants["acetonitrile_average"]]

# Write fasta files for each mutation in a separate file in their own subfolders per protein
for index, row in variants.iterrows():
    protein = None
    if "Brazzein" in row["protein"]:
        protein = "Brazzein_4he7"
    elif "thaumatin" in row["protein"]:
        protein = "Thaumatin_3aok"
    else:
        continue
        
    try:
        os.makedirs(f'{ddg_path}/{protein}/Fastas/')
    except FileExistsError:
        pass
    
    filename = f'{ddg_path}/{protein}/Fastas/{row["protein_id"]}.fasta'  
    if not os.path.exists(filename):
        with open(filename, 'w', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([">" + row["protein_id"]])
            writer.writerow([row["sequence"]])
    else:
        print(f"File {filename} already exists. Skipping.")

# Prepare input files for ddG calculations for Rosetta and Dynamut 2
# Make a column for mutation string containing mutation in the format required for DynaMut2 webserver
variants["mut_positions"] = ""
variants["dynamut_str"] = ""

for index, row in variants.iterrows():
    
    mut_str = ""
    mut_positions = []
    
    if "Brazzein" in row["protein"]:
        original = variants[variants["strain"] == "ST0094"]["sequence"].values[0] 
        mutation = variants.iloc[index]["sequence"]
    elif "thaumatin" in row["protein"]:
        original = variants[variants["strain"] == "ST0068"]["sequence"].values[0] 
        mutation = variants.iloc[index]["sequence"]
        
    for letter in range(0, len(original)):
        if original[letter] != mutation[letter]:
            mut_str += "A " + original[letter]+ str(letter+1) + mutation[letter] + ";"
            mut_positions.append(letter+1)
            
    variants.iloc[index, -2] = "+".join([str(i) for i in mut_positions])
    variants.iloc[index, -1] = mut_str.rstrip(";")
    
brazzein_mutations = list(variants[variants['protein'].str.contains("Brazzein")]["dynamut_str"])
thaumatin_mutations = list(variants[variants['protein'].str.contains("thaumatin")]["dynamut_str"])

brazzein_mutations = [a for a in brazzein_mutations if len(a) > 0]
thaumatin_mutations = [a for a in thaumatin_mutations if len(a) > 0]

try:
    os.makedirs(f"{ddg_path}/Brazzein_4he7/Dynamut/")
except FileExistsError:
    pass

try:
    os.makedirs(f"{ddg_path}/Thaumatin_3aok/Dynamut/")
except FileExistsError:
    pass

# Save mutations as txt files
if not os.path.exists(f"{ddg_path}/Brazzein_4he7/Dynamut/brazzein_dynamutlist.txt"):
    with open(f"{ddg_path}/Brazzein_4he7/Dynamut/brazzein_dynamutlist.txt", 'w') as f:
        f.write('\n'.join(brazzein_mutations))

if not os.path.exists(f"{ddg_path}/Thaumatin_3aok/Dynamut/thaumatin_dynamutlist.txt"):
    with open(f"{ddg_path}/Thaumatin_3aok/Dynamut/thaumatin_dynamutlist.txt", 'w') as f:
        f.write('\n'.join(thaumatin_mutations))

# Create _resfile.txt files that contain the mutations in the correct format for Rosetta CartesianDDG protocol
for index, row in variants.iterrows():
    mut_list = []
    if "Brazzein" in row["protein"]:
        original = variants[variants["strain"] == "ST0094"]["sequence"].values[0]
        mutation = row["sequence"]
        protein = "Brazzein"
        folder = "Brazzein_4he7"
    elif "thaumatin" in row["protein"]:
        original = variants[variants["strain"] == "ST0068"]["sequence"].values[0]
        mutation = row["sequence"]
        protein= "Thaumatin"
        folder = "Thaumatin_3aok"
    
    if "native" in row["protein_id"]:
        continue

    for letter in range(0, len(original)):
        if original[letter] != mutation[letter]:
            mut_list.append(original[letter]+ " " + str(letter+1) + " " + mutation[letter])
    
    protein_id = row["protein_id"]
    if not os.path.exists(f'{ddg_path}/{folder}/Resfiles/{protein_id}_resfile.txt'):
        with open(f'{ddg_path}/{folder}/Resfiles/{protein_id}_resfile.txt', 'w') as f:
            f.write(f'total {len(mut_list)}\n')
            f.write(f'{len(mut_list)}\n')
            f.write('\n'.join(mut_list))
            f.write('\n')

# Additional variants for Thaumatin-II
# Extra thaumatin variants – create fasta and resfiles
extra_thaumatin_variants = pd.read_excel(f'{repo_path}/1_variant_data/extra_thaumatin_sources.xlsx')
protein_name = "Thaumatin_3aok" # Output folder name
native_thaumatin_sequence = variants[variants["strain"] == "ST0068"]["sequence"].values[0]

# Save fastas for each variant
for index, row in extra_thaumatin_variants.iterrows():
    protein = f'{protein_name}_{row["protein"]}'
    sequence = row["sequence"]
    try:
        os.makedirs(f"{ddg_path}/{protein_name}/Fastas/")
    except FileExistsError:
        pass
    
    filename = f'{ddg_path}/{protein_name}/Fastas/{protein}.fasta'  
    if not os.path.exists(filename):  
        with open(filename, 'w', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([">" + protein])
            writer.writerow([row["sequence"]])

# Create _resfile.txt files that contain the mutations in the correct format for Rosetta CartesianDDG protocol
mut_positions = []
for index, row in extra_thaumatin_variants.iterrows():
    mut_list = []

    # Get the mutated sequence
    mutation = row["sequence"]

    # Compile mutation list
    for letter in range(0, len(native_thaumatin_sequence)):
        if native_thaumatin_sequence[letter] != mutation[letter]:
            mut_positions.append(int(letter+1))
            mut_list.append(native_thaumatin_sequence[letter]+ " " + str(letter+1) + " " + mutation[letter])
    
    protein = protein_name
    file_name = f'{protein_name}_{row["strain"]}'
    os.makedirs(f'{ddg_path}/{protein}/Resfiles/', exist_ok=True)
    if not os.path.exists(f'{ddg_path}/{protein}/Resfiles/{file_name}_resfile.txt'):
        with open(f'{ddg_path}/{protein}/Resfiles/{file_name}_resfile.txt', 'w') as f:
            f.write(f'total {len(mut_list)}\n')
            f.write(f'{len(mut_list)}\n')
            f.write('\n'.join(mut_list))
            f.write('\n')
    else:
        print(f"File {file_name}_resfile.txt already exists. Skipping.")