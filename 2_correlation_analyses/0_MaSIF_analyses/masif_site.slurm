#!/bin/bash
#SBATCH --partition=standard
#SBATCH --qos=normal
#SBATCH --nodes=1                         
#SBATCH --ntasks-per-node=1                      
#SBATCH --cpus-per-task=1               
#SBATCH --job-name masif
#SBATCH --mem=16384
#SBATCH --time=03:00:00

module load miniconda
source activate /maps/projects/ilfgrid/apps/masif/masif-env/

# Text file containing paths to the input pdbs
FILEPATHS=$1

# Read a line from the path file
INPUT_PDB=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "${FILEPATHS}")
BASENAME=`basename $INPUT_PDB .pdb`

# Create output directory for the results
output_dir=/projects/ilfgrid/people/pqh443/WP2/MaSIF_analyses/output/$BASENAME
mkdir -p $output_dir

# Run masif data preparation script
cd /projects/ilfgrid/apps/masif/data/masif_site

# Prepare PDB using data preparation script
./data_prepare_one.sh --file $INPUT_PDB ${BASENAME}_A

# Run the prediction on the prepared structure
./predict_site.sh ${BASENAME}_A

# Color the prediction structure (produces .ply file)
./color_site.sh ${BASENAME}_A

# Copy results to the output directory
cp /maps/projects/ilfgrid/apps/masif/data/masif_site/data_preparation/00-raw_pdbs/$BASENAME.pdb $output_dir
cp /maps/projects/ilfgrid/apps/masif/data/masif_site/output/all_feat_3l/pred_data/pred_${BASENAME}_A.npy $output_dir
cp /maps/projects/ilfgrid/apps/masif/data/masif_site/output/all_feat_3l/pred_surfaces/${BASENAME}_A.ply $output_dir
