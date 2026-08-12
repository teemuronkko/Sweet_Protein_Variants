set_color t1r2_color, [244,131,108]
set_color t1r3_color, [248,158,68]
set_color variant_color, [170,49,122]
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Brazzein//with_templates/unrelaxed_model_5_multimer_batch_20_5.pdb, cluster_1
color t1r2_color, chain A
color t1r3_color, chain B
color grey, chain C
set label_size, 25
color variant_color, resi 21+32+15+45+19+12+50+5+33+13+35+34+11+54+51+8+7+31+46 and chain C and cluster_1
set label_color, black
bg_color white
