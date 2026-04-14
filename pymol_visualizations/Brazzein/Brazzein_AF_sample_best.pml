set_color t1r2_color, [244,131,108]
set_color t1r3_color, [248,158,68]
set_color variant_color, [170,49,122]
load /Users/pqh443/Documents/AFsample_results/Sweet_Brazzein//unrelaxed_model_5_multimer_batch_20_5.pdb, cluster_1
color t1r2_color, chain A
color t1r3_color, chain B
color grey, chain C
set label_size, 25
color variant_color, resi 8+34+35+46+5+12+45+21+31+32+19+51+33+54+13+11+15+7+50 and chain C and cluster_1
set label_color, black
bg_color white
