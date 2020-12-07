#!/usr/bin/bash

while getopts ":ihn" opt; do
    case ${opt} in
        i )
            install=true
            ;;
        n )
            install=false
            ;;
        h )
            echo "Usage:"
            echo "       ./init.sh -i        Install Pipeline Resources and Initialize Mutant File System."
            echo "       ./init.sh -n        Initialize Mutant File System, No Install."
            echo "       ./init.sh -h        Display this Help Message."
            exit 0
            ;;
        \? )
            echo "Usage: ./init.sh [-i] [-n] [-h]"
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
    exit 0
else
    echo "Error in Mutant File Preperation."
    exit 1
fi
