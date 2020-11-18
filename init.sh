#!/usr/bin/bash

# ToDo - Need to change paths so init can be called at any destination
# need to change path in option file
# add error checking for failed shell script runs 

echo 'Begining Initialization.'

# Declare Variables
cbdock="$(pwd)/resources/CB-Dock/setup.sh"
vina="$(pwd)/resources/autodock_vina_1_1_2_linux_x86/bin/vina"
mglTools="$(pwd)/resources/mgltools_x86_64Linux2_1.5.6/bin"

# Run Python script for creating file system
echo 'Begining File Preparation.'
./bin/filePreparation.py ./inputs/mutations.txt
echo 'File Preparation Complete.'

#Install mglTools - this needs to be re written with new variables - looks awful
cd "$(pwd)/resources/mgltools_x86_64Linux2_1.5.6"
"./install.sh" #has to be executed in the install.sh holding dir
cd ../..
echo 'MGL Tools Installed.'


# Run CB-Dock setup.sh script
$cbdock "$mglTools/python" $vina
echo 'CB-Dock Initialization Complete.'

echo 'Initialization Complete.'
