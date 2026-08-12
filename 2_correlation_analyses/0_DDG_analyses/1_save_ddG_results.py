import pandas as pd
import os
import glob
repo_name = "Sweet_Protein_Variants"
current_path = os.path.abspath(__file__)
repo_path = current_path.split(repo_name)[0] + repo_name
variants_path = f"{repo_path}/1_variant_data/variants with parameters.xlsx"
ddg_path = f"{repo_path}/2_correlation_analyses/0_DDG_analyses"

# Read updated tsv file containing information about the variants
variants = pd.read_excel(variants_path)
variants = variants.replace(' ', '-', regex=True)
variants["protein_id"] = variants["protein"] + "_" + variants["strain"]

# Rename average column to Tm_average
variants = variants.rename(columns={"average": "Tm_average"})

# Make a column for Dynamut2 mutation string
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

# Read CartesianDDG output files
DDG_files = glob.glob(f"{ddg_path}/*/DDG_predictions/*/*.ddg")

# Empty list for results
rosetta_ddgs = []
protein = None

# Loop over DDG output files and calculate DDG as the difference between minimum energy of mutated protein
# and relaxed PDB wild type structure: DDG = DG_MT - DG_WT. In this case, DG_MT and DG_WT are outputted by 
# Rosetta and they are given in Rosetta Energy Units (REU). Negative DDG means stabilizing mutation and vice versa.
for file in DDG_files:
    with open(file) as f:
        lines = f.readlines()

    WT_min_energy=float('inf')
    MT_min_energy=float('inf')

    for line in lines:
        sep = "fa_atr:"
        line = line.split(sep, 1)[0]
        line = line.strip()
        mut_name = line.split(":")[2].strip()
        energy = float(line.split(":")[-1])
        if "WT" in line and energy < WT_min_energy:
            WT_min_energy = energy
        elif "MUT" in line and energy < MT_min_energy:
            MT_min_energy = energy

    if 'THAUMATIN' in file.upper():
        protein = "Thaumatin"
    elif 'BRAZZEIN' in file.upper():
        protein = "Brazzein"
      
    prot_id = file.split("/")[-2].strip()
    
    ddG=MT_min_energy - WT_min_energy
    rosetta_ddgs.append([protein, prot_id, mut_name, ddG])

rosetta_ddgs_df = pd.DataFrame(rosetta_ddgs, columns = ['protein', 'protein_id', 'mutation','ddG'])
rosetta_ddgs_df = rosetta_ddgs_df.sort_values(['protein','ddG'])

### Combine Rosetta CartesianDDG results with experimental delta-Tm measurements and DynaMut2 predictions

# Get native melting temperature (Tm) for Brazzein and Thaumatin from the variants dataframe
brazzein_tm = float(variants[variants["protein"] == "Brazzein-native"]["Tm_average"].values[0])
thaumatin_tm = float(variants[variants["protein"] == "thaumatin-II-native"]["Tm_average"].values[0])
variants["delta_tm"] = None

# Calculate change in melting temperature (Delta-Tm): Tm_mutation - Tm_wildtype
# Positive delta_tm means stabilizing mutation and vice versa.  
for index, row in variants.iterrows():
    if "Brazzein" in row["protein"]:
        native_tm = brazzein_tm
    if "thaumatin" in row["protein"]:
        native_tm = thaumatin_tm
    
    mut_tm = row["Tm_average"]
    try: 
        delta_tm = float(mut_tm) - native_tm
    except ValueError:
        pass
    
    # Save delta_tm to the dataframe in delta_tm column
    variants.loc[index, "delta_tm"] = delta_tm

# Subset dataframe to only contain information on protein and its delta_tm
variants_tm = variants[["protein", "protein_id", "delta_tm", "dynamut_str"]].sort_values(["protein", "delta_tm"], ascending=[True,False])
variants_tm = variants_tm[["protein_id", "delta_tm", "dynamut_str"]]

# Merge results from Cartesian DDG protocol with the experimental delta_tm measurements
results_df = rosetta_ddgs_df.merge(variants_tm, how='left', on='protein_id')

# Read DynaMut2 output files for single and multiple mutations for Brazzein and Thaumatin
thaumatin_single_dynamut = pd.read_csv(f"{ddg_path}/Thaumatin_3aok/Dynamut/Thaumatin_single_mut_results_169099668279.csv")
thaumatin_multiple_dynamut = pd.read_csv(f"{ddg_path}/Thaumatin_3aok/Dynamut/Thaumatin_multiple_mut_results_169099895464.csv")
brazzein_single_dynamut = pd.read_csv(f"{ddg_path}/Brazzein_4he7/Dynamut/Brazzein_single_mut_results_169099630467.csv")
brazzein_multiple_dynamut = pd.read_csv(f"{ddg_path}/Brazzein_4he7/Dynamut/Brazzein_multiple_mut_results_169099881928.csv")

# Make a column for DynaMut2 mutation string containing mutation in the format required for DynaMut2 webserver
results_df["dynamut_id"] = results_df["protein"] + "_" + results_df["dynamut_str"]

# Concatenate DynaMut2 results for single and multiple mutations for Brazzein and Thaumatin
dynamut_single_values = pd.concat([thaumatin_single_dynamut, brazzein_single_dynamut])                           
dynamut_multiple_values = pd.concat([thaumatin_multiple_dynamut, brazzein_multiple_dynamut,])
dynamut_multiple_values = dynamut_multiple_values.rename(columns={"mutations": "dynamut_id"})
dynamut_single_values = dynamut_single_values.rename(columns={"mutation": "dynamut_id", "prediction": "dynamut2_prediction"})
dynamut_values = pd.concat([dynamut_single_values, dynamut_multiple_values])
dynamut_values = dynamut_values.drop("chain", axis = 1)

# Merge results from Cartesian DDG protocol with the experimental delta_tm measurements and DynaMut2 predictions
merged_results_df = results_df.merge(dynamut_values, how='left', on='dynamut_id')
merged_results_df = merged_results_df.drop(["average_distance", "sum_single_predictions", "dynamut_id", "mutation"], axis = 1)
merged_results_df = merged_results_df.sort_values(["protein", "ddG"], ascending=[True,True])
merged_results_df["delta_tm"] = pd.to_numeric(merged_results_df["delta_tm"])
merged_results_df["ddG"] = pd.to_numeric(merged_results_df["ddG"])
merged_results_df.round(4).to_csv(f"{ddg_path}/DDG_results.csv", index= False)