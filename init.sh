#!/usr/bin/bash

# ToDo - Need to change paths so init can be called at any destination

echo 'Begining Initialization.'

# Declare Variables
cbdock="$(pwd)/resources/CB-Dock/setup.sh"
vina="$(pwd)/resources/autodock_vina_1_1_2_linux_x86/bin/vina"
mglTools="$(pwd)/resources/mgltools_x86_64Linux2_1.5.6/bin/python"

echo 'Begining File Preparation.'
./bin/filePreparation.py ./inputs/mutations.txt
echo 'File Preparation Complete.'

$cbdock $vina $mglTools
echo 'CB-Dock Initialization Complete.'

echo 'Initialization Complete.'
