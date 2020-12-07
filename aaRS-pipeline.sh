#!/usr/bin/bash

run=false
install=false
while getopts ":ihnr" opt; do
    case ${opt} in
        i )
            install=true
            ;;
        n )
            install=false
            ;;
        h )
            echo "Usage:"
            echo "       ./aaRS-pipeline.sh -i        Install Pipeline Resources and Initialize Mutant File System."
            echo "       ./aaRS-pipeline.sh -n        Initialize Mutant File System, No Install."
            echo "       ./aaRS-pipeline.sh -r        Run Nextflow main.nf ."
            echo "       ./aaRS-pipeline.sh -h        Display this Help Message."
            exit 0
            ;;
        r )
            run=true
            ;;
        \? )
            echo "Usage: ./aaRS-pipeline.sh [-i] [-n] [-r ][-h]"
            exit 1
        ;;
    esac
done

if $install; then
    echo 'Begining Installation of Pipeline Resources.'

    # Declare Variables
    cbDock="$(pwd)/resources/CB-Dock/setup.sh"
    vina="$(pwd)/resources/autodock_vina_1_1_2_linux_x86/bin/vina"
    mglTools="$(pwd)/resources/mgltools_x86_64Linux2_1.5.6/bin"

    # Install mglTools
    cd "$(pwd)/resources/mgltools_x86_64Linux2_1.5.6"
    echo "Begining Installation of MGL Tools - This May Take Some Time."
    "./install.sh" &>/dev/null # Has to be executed in install.sh holding dir, remove &>/dev/null for error checking
    if [[ $? -eq 0 ]]
    then
        echo "MGL Tools Installation Complete."
        cd ../..
    else
        echo "Error in MGL Tools Installation."
        exit 1
    fi

    # Initialize CB-Dock
    $cbDock "$mglTools/python" $vina
    if [[ $? -eq 0 ]]
    then
        echo "CB-Dock Initialization Complete."
    else
        echo "Error in CB-Dock Initialization."
        exit 1
    fi

fi

# Create .mutfiles and option files for mutant run
echo "Begining Initialization of Mutant File System."
./bin/filePreparation.py ./inputs/mutations.txt
if [[ $? -eq 0 ]]
then
    echo "File Preperation Complete."
else
    echo "Error in Mutant File Preperation."
    exit 1
fi

# Commence Pipeline if -r (run) used
if $run
then
    echo "Commencing Pipeline Flow."
    nextflow run main.nf
    if [[ $? -eq 0 ]]
    then
        echo "Pipeline Flow Complete."
        echo "Results in /output/results.json"
        exit 0
    else
        echo "Error in Pipeline Flow."
        exit 1
    fi
else
    echo "Pipeline Ready for Flow."
    echo "Initiate with cmd <nextflow run main.nf>"
    exit 0
fi
