from pymol import cmd

def align_all(input_structure):
    
    # Get the list of all loaded structures
    structures = cmd.get_names("objects")

    # Remove the input structure from the list
    structures.remove(input_structure)

    # Align all structures to the input structure
    for structure in structures:
        cmd.align(structure, input_structure)

cmd.extend("align_all", align_all)
cmd.auto_arg[0]["align_all"] = [cmd.object_sc, "object", ""]