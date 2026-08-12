set_color t1r2_color, [244,131,108]
set_color t1r3_color, [248,158,68]
set_color variant_color, [170,49,122]
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Thaumatin-II//with_templates/unrelaxed_model_5_multimer_batch_16_2.pdb, cluster_5
color t1r2_color, chain A
color t1r3_color, chain B
color grey, chain C
set label_size, 25
color variant_color, resi 105+184+23+60+26+153+136+148+109+32+157+89+207+104+68 and chain C and cluster_5
set label_color, black
bg_color white
