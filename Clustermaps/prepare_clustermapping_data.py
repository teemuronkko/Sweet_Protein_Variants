#!/usr/bin/env python3

# Script to prepare the data for clustermapping. Merges experimental and computational measures
# of protein stability and adds the protein sequence and structure features to the data.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from modlamp.descriptors import PeptideDescriptor, GlobalDescriptor
import os

# Get path to repository
repo_name = "WP2_SweetProteinDiscovery"
current_path = os.getcwd()
repo_path = current_path.split(repo_name)[0] + repo_name

# Read clustermapping dataframe
variant_df = pd.read_csv(f"{repo_path}/sweet_protein_variants/variant_df.csv")

def get_modlamp_descriptors(df, seq_column = "sequence"):
    # Get MODLABS descriptors for each sequence and add them to the dataframe
    sequences = list(df[seq_column])

    # GLOBAL DESCRIPTORS
    # Charge
    desc = GlobalDescriptor(sequences)
    desc.calculate_charge(ph=7.4, amide=True)
    df["Charge (at pH 7.4)"] = desc.descriptor

    # Charge density
    desc = GlobalDescriptor(sequences)
    desc.charge_density(ph=6, amide=True)
    df["Charge density"] = desc.descriptor

    # Isoelectric point
    desc = GlobalDescriptor(sequences)
    desc.isoelectric_point()
    df["Isoelectric point"] = desc.descriptor

    # Instability index 
    desc = GlobalDescriptor(sequences)
    desc.instability_index()
    df["Instability index"] = desc.descriptor

    # Aromaticity
    desc = GlobalDescriptor(sequences)
    desc.aromaticity()
    df["Aromaticity"] = desc.descriptor

    # Aliphatic index
    desc = GlobalDescriptor(sequences)
    desc.aliphatic_index()
    df["Aliphatic index"] = desc.descriptor

    # Boman index
    desc = GlobalDescriptor(sequences)
    desc.boman_index()
    df["Boman index"] = desc.descriptor

    # Hydrophobic ratio
    desc = GlobalDescriptor(sequences)
    desc.hydrophobic_ratio()
    df["Hydrophobic ratio"] = desc.descriptor

    # AA BASED DESCRIPTORS

    # bulkiness - Amino acid side chain bulkiness scale
    AMP = PeptideDescriptor(sequences,'bulkiness')
    AMP.calculate_global(window=1000, modality='mean')
    df["Sidechain bulkiness"] = AMP.descriptor

    # pepcats – modlabs pharmacophoric feature based PEPCATS scale
    AMP = PeptideDescriptor(sequences,'pepcats')
    AMP.calculate_global(window=1000, modality='mean')
    df["PEPCATS"] = AMP.descriptor

    # polarity – Amino acid polarity scale
    AMP = PeptideDescriptor(sequences,'polarity')
    AMP.calculate_global(window=1000, modality='mean')
    df["Amino acid polarity"] = AMP.descriptor

    # PPCALI – modlabs inhouse scale derived from a PCA of 143 amino acid property scales
    AMP = PeptideDescriptor(sequences,'PPCALI')
    AMP.calculate_global(window=1000, modality='mean')
    df["PPCALI"] = AMP.descriptor

    # t_scale – A PCA derived scale based on amino acid side chain properties calculated with 6 different probes of the GRID program
    AMP = PeptideDescriptor(sequences,'t_scale')
    AMP.calculate_global(window=1000, modality='mean')
    df["T-scale"] = AMP.descriptor

    # z3 – The original three dimensional Z-scale
    AMP = PeptideDescriptor(sequences,'z3')
    AMP.calculate_global(window=1000, modality='mean')
    df["Z3"] = AMP.descriptor

    return df

def calculate_surface_properties(ply_path):
    """
    Function to calculate the average charge, hbond, and hphob properties of a surface from a PLY file outputted by MaSIF.
    """

    from plyfile import PlyData
    import numpy as np
    
    ply_data = PlyData.read(ply_path)

    # Assuming the properties are stored in vertex elements, access the vertex element
    vertices = ply_data['vertex']

    # Extract the custom properties: charge, hbond, hphob
    charges = np.array(vertices['charge'])
    hbonds = np.array(vertices['hbond'])
    hphobs = np.array(vertices['hphob'])

    # Calculate the averages of these properties
    average_charge = np.mean(charges)
    average_hbond = np.mean(hbonds)
    average_hphob = np.mean(hphobs)

    res_dict = {
        "avg_charge": average_charge,
        "avg_hbond": average_hbond,
        "avg_hphob": average_hphob
    }

    return res_dict

# Helper function to read ranking_debug.json files into a dictionary
def read_ranking_json(path):
    """
    Helper function to read ranking_debug.json files into a dictionary.
    Assumes that path contains a folder for each model.
    returns a dictionary with model names as keys and ranking_debug.json files as values.
    """
    import os
    import json

    # Make sure path ends with a slash
    if not path.endswith("/"):
        path = path + "/"

    # Make sure path exists
    if not os.path.exists(path):
        print(f"Error: Path {path} does not exist.")
        return None

    # List all ranking_debug.json files in the AF2 model folder using glob
    ranking_debugs = glob.glob(path + "*/ranking_debug.json")
 
    # Empty dictionary for storing the results
    model_metrics = {}

    # Loop over all ranking_debug.json files
    for p in ranking_debugs:
        model_name = p.split("/")[-2].strip()
            
        # Read json into a dictionary
        with open(p, 'r') as f:
            ranking_debug = json.load(f)

        model_metrics[model_name] = ranking_debug

    return model_metrics

def sasa(pdb_path):
    """
    Helper function to calculate the solvent accessible surface area (SASA) of a protein structure using FreeSASA.
    Outputs a dictionary with the total SASA, and SASA for apolar and polar residues.
    """
    import freesasa

    # Read the PDB file
    structure = freesasa.Structure(pdb_path)

    # Calculate SASA using default parameters
    result = freesasa.calc(structure)

    area_classes = freesasa.classifyResults(result, structure)

    res_dict = {"total": result.totalArea()}
    for key in area_classes:
        res_dict[key.lower()] = area_classes[key]

    return res_dict

def main():
    # Path to variant data
    variant_df = pd.read_excel(f"{repo_path}/sweet_protein_variants/variants with parameters Teemu.xlsx")
    variant_df['sweet_protein'] = np.nan
    variant_df['sweet_protein'] = variant_df['sweet_protein'].mask(variant_df['protein'].str.upper().str.contains('BRAZZEIN'), 'Brazzein')
    variant_df['sweet_protein'] = variant_df['sweet_protein'].mask(variant_df['protein'].str.upper().str.contains('MNEI'), 'MNEI')
    variant_df['sweet_protein'] = variant_df['sweet_protein'].mask(variant_df['protein'].str.upper().str.contains('THAUMATIN'), 'Thaumatin-II')

    # Build protein id 
    variant_df["protein_id"] = variant_df["protein"] + "_" + variant_df["strain"]
    variant_df["protein_id"] = [i.replace(" native", "") for i in variant_df["protein_id"]]
    variant_df["protein_id"] = [i.replace(" ", "-") for i in variant_df["protein_id"]]

    # Read ddg data
    ddg_df = pd.read_csv(f"{repo_path}/ddg_analyses/DDG_results.csv")
    ddg_df = ddg_df[["protein_id","ddG", "dynamut2_prediction", "delta_tm"]].copy()

    # Merge two dataframes on protein id
    variant_df = pd.merge(variant_df, ddg_df, on="protein_id", how = "left")

    # Rename average to Tm_average
    variant_df = variant_df.rename(columns={
        'Tm': 'Tm_1',
        'average':'Tm',
        'average.1': 'acetonitrile_average',
        'Unnamed: 6': 'Tm_2',
        'Unnamed: 9': 'acetonitrile_2',
        'number of cysteines': 'Number of cysteines',
        'yield (mg/L/OD)': 'Yield',
        'final OD600': 'OD600',
        'growth rate': 'Growth rate',
        'delta_tm': 'ΔTm',
        'ddG': 'ΔΔG (Rosetta)',
        'dynamut2_prediction': 'ΔΔG (DynaMut2)'
    })

    # Native strains for each sweet protein
    native_strains = {
        "Brazzein": "ST0094",
        "MNEI": "ST0095",
        "Thaumatin-II": "ST0068"
    }

    # Columns to drop
    cols_to_keep = ['sweet_protein', 'strain', 'protein', 'plasmid', 'mutation', 'sequence', 'Tm', 'Number of cysteines', 'Yield', 'OD600', 'Growth rate', 'ΔΔG (Rosetta)', 'ΔTm', 'ΔΔG (DynaMut2)']
    variant_df = variant_df[cols_to_keep].copy()

    # Make sure that numeric columns are numeric
    numeric_cols = ['Tm', 'Number of cysteines', 'Yield', 'OD600', 'Growth rate']
    for col in numeric_cols:
        variant_df[col] = pd.to_numeric(variant_df[col], errors='coerce') 

    # Add modlamp descriptors to the dataframe
    variant_df = get_modlamp_descriptors(variant_df, "sequence")

    # List ply files from MaSIF output directory
    ply_folder = f"{repo_path}/MaSIF_analyses/MaSIF_results/*/*.ply"

    # Empty dictionary to store the masif features for each structure
    masif_features = dict()

    for ply_path in glob.glob(ply_folder):
        # Get model name
        protein = ply_path.split("/")[-2]
        protein = protein.replace("-ST", "_ST")

        # Save masif features in a dictionary
        masif_features[protein] = calculate_surface_properties(ply_path)

    # Make a dataframe
    masif_features = pd.DataFrame(masif_features)

    # Transpose dataframe
    masif_features = masif_features.transpose()

    # Drop irrelevant models
    masif_features["strain"] = list(masif_features.index)
    masif_features["strain"] = [i.split("_")[-1] for i in masif_features["strain"]]
    masif_features = masif_features[~masif_features.strain.str.contains("model")]

    # List ply files from MaSIF output directory
    af_model_folder = f"{repo_path}/AF2_Models/SweetProteinVariants/"

    # Read model qualities into dictionary
    model_qualities = read_ranking_json(af_model_folder)

    # Get best model quality for each strain
    for key in model_qualities.keys():
        model_qualities[key] = max(list(model_qualities[key]["plddts"].values()))

    # Make a dataframe
    model_qualities = pd.DataFrame(model_qualities, index=[0]).transpose()
    model_qualities["strain"] = [i.split("_")[-1] for i in model_qualities.index]
    model_qualities.columns = ["plddt", "strain"]

    # Specify the path to your PDB file
    pdb_path = f"{repo_path}/AF2_Models/SweetProteinVariants/*/ranked_0.pdb"

    # Empty dictionary to store the SASA for each structure
    sasa_dict = dict()
    for pdb in glob.glob(pdb_path):
        model = pdb.split("/")[-2]
        sasa_dict[model] = sasa(pdb)

    # Make a dataframe of SASA values
    sasa_df = pd.DataFrame(sasa_dict).transpose()
    sasa_df["strain"] = [i.split("_")[-1] for i in sasa_df.index]

    # Merge the three dataframes containing the structural features
    structural_features = pd.merge(masif_features, model_qualities, on="strain", how="inner")
    structural_features = pd.merge(structural_features, sasa_df, on="strain", how="inner")

    # Input the strain names from the variant_df dataframe
    for index, row in structural_features.iterrows():
        if row["strain"] in native_strains.keys():
            structural_features.at[index, "strain"] = native_strains[row["strain"]]

    # Rename columns
    structural_features = structural_features.rename(columns={
        "avg_charge": "Avg. surface charge",
        "avg_hbond": "Avg. surface hbond",
        "avg_hphob": "Avg. surface hydrophobicity",
        "plddt": "Avg. pLDDT",
        "total": "Total SASA",
        "apolar": "Apolar SASA",
        "polar": "Polar SASA"
    })

    # Merge the structural features with the variant_df dataframe
    all_features_df = pd.merge(variant_df, structural_features, on="strain", how="inner")
    all_features_df.to_csv(f"{repo_path}/sweet_protein_variants/variant_df.csv", index=False)

if __name__ == "__main__":
    main()