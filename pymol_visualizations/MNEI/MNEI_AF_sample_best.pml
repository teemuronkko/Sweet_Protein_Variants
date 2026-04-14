set_color t1r2_color, [244,131,108]
set_color t1r3_color, [248,158,68]
set_color variant_color, [170,49,122]
load /Users/pqh443/Documents/AFsample_results/Sweet_MNEI//unrelaxed_model_5_multimer_batch_12_2.pdb, cluster_1
color t1r2_color, chain A
color t1r3_color, chain B
color grey, chain C
set label_size, 25
color variant_color, resi 8+41+66+34+12+23+48+1+29+44+20+16+56+47+32+17+73+19+93+89+91+60+22+54+86+6+42+43 and chain C and cluster_1
set label_color, black
bg_color white
