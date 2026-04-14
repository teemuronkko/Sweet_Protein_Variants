#!/usr/bin/env python3
# Script to create pymol scripts for sweet protein variants
import pandas as pd
import re
import os

def get_variants(native, variant):
    """
    Function to get the mutations between a native and a variant sequence.
    """
    mutations = []
    for i in range(len(native)):
        if native[i] != variant[i]:
            mutations.append(f"{native[i]}{i+1}{variant[i]}")
    return mutations

def get_mutation_positions(df, sweet_protein, source):
    """
    Helper function to get the mutation positions for a sweet protein and a source.
    """
    mutations = list(df[(df['sweet_protein'] == sweet_protein) & (variant_df['Source'] == source)]['corrected_mutation'])
    return set(re.findall(r'\d+', "_".join(mutations)))

def add_line(object, pairs, pymol_script, color, grid_slot, chain = "A", dash_width = 4, dash_gap = 0.4):
    """
    Helper function to add a line between pairs of residues in a pymol script.
    """
    for pair in pairs:
        A = pair[0]
        B = pair[1]
        connection_name = f"{A}_{B}_bond"
        pymol_script += f"distance {connection_name}, /{object}//{chain}/{A}/CA, /{object}//{chain}/{B}/CA\n"
        pymol_script += f"set dash_width, {dash_width}, {connection_name}\n"
        pymol_script += f"set dash_color, {color}, {connection_name}\n"
        pymol_script += f"set dash_gap, {dash_gap}, {connection_name}\n"
        pymol_script += f"set grid_slot, {grid_slot}, {connection_name}\n"
        pymol_script += f"hide labels, {connection_name}\n"
    return pymol_script

# Get path to repository
repo_name = "WP2_SweetProteinDiscovery"
current_path = os.getcwd()
repo_path = current_path.split(repo_name)[0] + repo_name

# Read clustermapping dataframe
variant_df = pd.read_csv(f"{repo_path}/sweet_protein_variants/variant_df.csv")

# Replace "/ " with underscore in mutation column
variant_df["mutation"] = [str(i).replace("/", "_") for i in variant_df["mutation"]]
variant_df["mutation"] = [str(i).replace(" ", "") for i in variant_df["mutation"]]
variant_df["mutation"] = [str(i).rstrip("_") for i in variant_df["mutation"]]

 # Read file with source
variant_sources = pd.read_excel(f"{repo_path}/sweet_protein_variants/variants with parameters_with_groups.xlsx")
variant_sources = variant_sources[variant_sources["Source"].notna()]
variant_sources["Source"] = [str(i).replace("Bibliogtaphy", "Bibliography") for i in variant_sources["Source"]]
variant_sources = variant_sources[["Source", "strain"]]

# Merge with variant_df and remove native proteins
variant_df = pd.merge(variant_df, variant_sources, on="strain", how="left")

# Native strains for each sweet protein
native_strains = {
    "Brazzein": "ST0094",
    "MNEI": "ST0095",
    "Thaumatin-II": "ST0068"
}

# Create lists of variant positions for each sweet protein
brazzein_pos = []
mnei_pos = []
thaumatin_pos = []

# Read data from extra thaumatin variants
extra_thaumatin_df = pd.read_excel(f"{repo_path}/sweet_protein_variants/extra_thaumatin_sources.xlsx")
cols_to_keep = ["sweet_protein", "protein", "strain", "Source", "sequence"]

# Concatenate the dataframes
variant_df = pd.concat([variant_df[cols_to_keep], extra_thaumatin_df[cols_to_keep]])
variant_df.reset_index(drop=True, inplace=True)

# Empty column for corrected variants
variant_df["corrected_mutation"] = ""

# Loop through the dataframe and get the corrected mutations
for index, row in variant_df.iterrows():
    protein = row["sweet_protein"]
    native = variant_df[variant_df["strain"] == native_strains[protein]]["sequence"].values[0]
    variant = row["sequence"]
    mutations = get_variants(native, variant)
    variant_df.loc[index,"corrected_mutation"] = "_".join(mutations)
 
variant_df = variant_df[~variant_df["protein"].str.contains("native")]
variant_df = variant_df[variant_df["strain"] != "ST0129"]

variant_df = variant_df[["sweet_protein", "protein", "strain", "Source", "corrected_mutation", "sequence"]]

# Get the mutation positions for each source
brazzein_disulfide = get_mutation_positions(variant_df, "Brazzein", "Disulfide bridge")
mnei_disulfide = get_mutation_positions(variant_df, "MNEI", "Disulfide bridge")
thaumatin_disulfide =  get_mutation_positions(variant_df, "Thaumatin-II", "Disulfide bridge")

brazzein_rosetta = get_mutation_positions(variant_df, "Brazzein", "Rosetta")
mnei_rosetta = get_mutation_positions(variant_df, "MNEI", "Rosetta")
thaumatin_rosetta = get_mutation_positions(variant_df, "Thaumatin-II", "Rosetta")

brazzein_consensus = get_mutation_positions(variant_df, "Brazzein", "consensus")
mnei_consensus = get_mutation_positions(variant_df, "MNEI", "consensus")
thaumatin_consensus = get_mutation_positions(variant_df, "Thaumatin-II", "consensus")

brazzein_biblography = get_mutation_positions(variant_df, "Brazzein", "Bibliography")
mnei_bibliography = get_mutation_positions(variant_df, "MNEI", "Bibliography")
thaumatin_biobliography = get_mutation_positions(variant_df, "Thaumatin-II", "Bibliography")

# Get pairs of brazzein disulfide mutations for visualising disulfide bridges in pymol
disulfide_bridges = {
    "Thaumatin-II": [],
    "MNEI": [],
    "Brazzein": []
}

for index, row in variant_df.iterrows():
    if row["Source"] == "Disulfide bridge":
        numbers = re.findall(r'\d+', row["corrected_mutation"])
        if len(numbers) == 2:
            disulfide_bridges[row["sweet_protein"]].append(numbers)

# Set PDB codes for Brazzein, MNEI, and Thaumatin-II
pdbs = {
    "Brazzein": "4HE7",
    "MNEI": "1IV7",
    "Thaumatin-II": "3AOK"
}

# Set colors for different types of mutations
mutation_colors = {
    "disulfide" : "[170,49,122]",
    "consensus" : "[224,79,103]",
    "rosetta" : "[244,131,108]",
    "bibliography" : "[248,158,68]"
}

# Save different types of mutations in dictionaries for each sweet protein
disulfide_mutations = {
    "Brazzein": brazzein_disulfide,
    "MNEI": mnei_disulfide,
    "Thaumatin-II": thaumatin_disulfide 
}

consensus_mutations = {
    "Brazzein": brazzein_consensus,
    "MNEI": mnei_consensus,
    "Thaumatin-II": thaumatin_consensus 
}

rosetta_mutations = {
    "Brazzein": brazzein_rosetta,
    "MNEI": mnei_rosetta,
    "Thaumatin-II": thaumatin_rosetta 
}

bibliography_mutations = {
    "Brazzein": brazzein_biblography,
    "MNEI": mnei_bibliography,
    "Thaumatin-II": thaumatin_biobliography 
}


# Make a pymol for visualising the mutations for each sweet protein
for sweet_protein in ["Brazzein", "MNEI", "Thaumatin-II"]:
    
    # Set up basic variables for the pymol script
    pymol_script = "reinit\nset grid_mode, 1\nbg_color white\n"
    pymol_script += "set cartoon_loop_radius, 0.3\n"
    pymol_script += "set cartoon_fancy_helices, 0\n"
    pymol_script += "set cartoon_fancy_sheets, 0\n"
    pymol_script += "set cartoon_oval_length, 1.0\n"
    pymol_script += "set cartoon_oval_width, 0.25\n"
    pymol_script += "set cartoon_rect_width, 0.25\n"
    pymol_script += "set cartoon_rect_length, 1.5\n"
    pymol_script += "set cartoon_rect_length, 1.5\n"

    # Initialize in grid slot 1 and set transparency variable for later use
    grid_slot = 1
    transparency = 0.2

    # Get the PDB code for the sweet protein
    pdb_code = pdbs[sweet_protein]

    # Get disulfide mutations and 
    pairs = disulfide_bridges[sweet_protein]
    mutation_type = "disulfide"

    # Get disulfide mutations
    mutations = "+".join(disulfide_mutations[sweet_protein])
    object = f"{sweet_protein}_{mutation_type}_object"
    color = mutation_colors[mutation_type]

    # Add the mutations to the pymol script
    pymol_script += f"fetch {pdb_code}, {object}\n"
    pymol_script += f"set grid_slot, {grid_slot}, {object}\n"
    pymol_script += f"hide everything, {object}\n"
    pymol_script += f"show cartoon, {object} and chain A\n"
    pymol_script += f"color grey80, {object}\n"
    pymol_script += f"set cartoon_transparency, {transparency}, {object}\n"
    pymol_script += f"select {sweet_protein}_{mutation_type}, {object} and resi {mutations}\n"
    pymol_script += f"set cartoon_transparency, 0, {sweet_protein}_{mutation_type}\n"
    pymol_script += f"set_color {mutation_type}_color, {color}\n"
    pymol_script += f"color {mutation_type}_color, {sweet_protein}_{mutation_type}\n\n\n"
    pymol_script += add_line(object, pairs, "", f"{mutation_type}_color", grid_slot)

    # Plot next variants in a different grid slot
    grid_slot += 1

    # Add the mutations to the pymol script
    object = f"{sweet_protein}_object_2"

    # Fetch pdb to the next grid slot and visualize other types of mutations
    pymol_script += f"fetch {pdb_code}, {object}\n"
    pymol_script += f"set grid_slot, {grid_slot}, {object}\n"
    pymol_script += f"hide everything, {object}\n"
    pymol_script += f"show cartoon, {object} and chain A\n"
    pymol_script += f"color grey80, {object}\n"
    pymol_script += f"set cartoon_transparency, {transparency}, {object}\n"

    # Loop through mutation types and add them to the pymol script, coloring by source
    for mutation_type in ["consensus", "rosetta", "bibliography"]:
        if mutation_type == "consensus":
            mutations = "+".join(consensus_mutations[sweet_protein])
        elif mutation_type == "rosetta":
            mutations = "+".join(rosetta_mutations[sweet_protein])
        elif mutation_type == "bibliography":
            mutations = "+".join(bibliography_mutations[sweet_protein])

        # Skip if no mutations are found for the mutation type
        if len(mutations) == 0:
            continue

        # Get color from the mutation_colors dictionary for the mutation type
        color = mutation_colors[mutation_type]

        # Select on color variants
        pymol_script += f"select {sweet_protein}_{mutation_type}, {object} and resi {mutations}\n"
        pymol_script += f"set cartoon_transparency, 0.0, {sweet_protein}_{mutation_type}\n"
        pymol_script += f"set_color {mutation_type}_color, {color}\n"
        pymol_script += f"color {mutation_type}_color, {sweet_protein}_{mutation_type}\n"
        pymol_script += f"deselect\n"

    # Remove B chain from MNEI (structure has dimer)
    if sweet_protein == "MNEI":
        pymol_script += f"remove {object} and chain B\n"

    # Align all objects to the last added object and center and orient the view
    pymol_script += f"alignto {object}\n"
    pymol_script += "center\n"
    pymol_script += "orient\n"

    # Save the pymol script to a file
    if not os.path.exists(f"{repo_path}/pymol_visualizations/{sweet_protein}"):
        os.makedirs(f"{repo_path}/pymol_visualizations/{sweet_protein}")
    with open(f"{repo_path}/pymol_visualizations/{sweet_protein}/{sweet_protein}_variants.pml", "w") as f:
        f.write(pymol_script)