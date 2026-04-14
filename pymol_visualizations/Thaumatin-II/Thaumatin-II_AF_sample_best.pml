set_color t1r2_color, [244,131,108]
set_color t1r3_color, [248,158,68]
set_color variant_color, [170,49,122]
load /Users/pqh443/Documents/AFsample_results/Sweet_Thaumatin-II//unrelaxed_model_5_multimer_batch_16_2.pdb, cluster_5
color t1r2_color, chain A
color t1r3_color, chain B
color grey, chain C
set label_size, 25
color variant_color, resi 136+23+26+157+89+60+207+68+148+105+153+32+104+109+184 and chain C and cluster_5
set label_color, black
bg_color white
