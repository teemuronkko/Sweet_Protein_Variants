set_color t1r2_color, [244,131,108]
set_color t1r3_color, [248,158,68]
set_color variant_color, [170,49,122]
set_color sweet_protein_color, [170,49,122]
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Brazzein//with_templates/unrelaxed_model_5_multimer_batch_20_5.pdb, cluster_1
label resi 1 and name CA and chain C and cluster_1, 'Cluster 1'
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Brazzein//with_templates/unrelaxed_model_5_multimer_v2_no_templates_batch_16_4.pdb, cluster_2
label resi 1 and name CA and chain C and cluster_2, 'Cluster 2'
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Brazzein//with_templates/unrelaxed_model_3_multimer_v2_batch_12_1.pdb, cluster_3
label resi 1 and name CA and chain C and cluster_3, 'Cluster 3'
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Brazzein//with_templates/unrelaxed_model_5_multimer_v2_batch_9_4.pdb, cluster_4
label resi 1 and name CA and chain C and cluster_4, 'Cluster 4'
load /Users/pqh443/Documents/Git_projects/Sweet_Protein_Variants/3_structural_analyses/AFsample_models/Brazzein//with_templates/unrelaxed_model_5_multimer_v2_batch_18_5.pdb, cluster_5
label resi 1 and name CA and chain C and cluster_5, 'Cluster 5'
alignto cluster_1
color t1r2_color, chain A
color t1r3_color, chain B
color sweet_protein_color, chain C
set label_size, 25
set label_color, black
bg_color white
hide everything, chain A and not cluster_1
hide everything, chain B and not cluster_1
