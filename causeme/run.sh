#!/usr/bin/bash
# Setup anaconda
. /etc/profile.d/anaconda.sh
setup-anaconda

# Activate conda environment
if [ $1 == "pcmci" ]
then
    source activate PCMCI 
else
    source activate SDA4
fi

# Use R CMD BATCH to print all stdout into a .out file
python /smartdata/uqeih/causeme/causeme_runner.py $1 $2 $3
