#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from itertools import product
import shutil

dirName = os.path.abspath(__file__) # path to bin directory
launchDir = str(Path(dirName).parent.parent) # path to pipeline directory

def readMutations(mutFile):

    with open(mutFile, 'r') as read_file:
        strings = read_file.read().split() # list of all strings in text file where even = position, odd = pool

        positions = [] # holds mutation position index e.g. Y32
        residues = [] # holds the string of pooled mutable residues

        # Sort text file
        for number in range(0, len(strings)):
            if number % 2 == 0:
                positions.append(strings[number])
            else:
                residues.append(strings[number])

        perms = list(product(*residues)) # calculates permutations [('S', 'R', 'R', 'S'), (),..]

        # Clean
        permutations = [] # in forms ['SRRS', 'SFFS', ... , ]
        for set in perms:
            mutant = ''
            for residue in set:
                mutant += residue
            permutations.append(mutant)


        read_file.close()

        print(permutations) # output to stdout channel as string (!)


        return permutations, positions

def writeMutFiles(permutations, positions):
    '''
    Takes positions and permutations lists and creates mutFiles in the output dir
    Needs to check if mutFile directory exists and make it if not
    Needs error checking and handling
    '''

    count = 0
    while count < len(permutations):
        f = open(launchDir + '/output/mutFiles/' + str(count) + '.mutfile', 'w+')
        f.write('total ' + str(len(positions)) + '\n' + str(len(positions)) + '\n')

        mutations = permutations[count] # string of mutations e.g. SRRS

        # positions list should be same length as mutations string - add an error check here (!)
        i = 0
        while i < len(positions):
            f.write(positions[i][0] + ' ' + positions[i][1:] + ' ' + mutations[i] + '\n') # formatting
            i += 1

        f.close()
        count += 1

def writeOptionFiles(permutations):

    count = 0
    while count < len(permutations):
        shutil.copy2(launchDir + '/resources/option', launchDir + '/output/optionFiles') #copy from template
        os.rename(launchDir + '/output/optionFiles/option', launchDir+'/output/optionFiles/' + str(count) + '_option')
        f = open(launchDir + '/output/optionFiles/' + str(count) + '_option', 'a')
        f.write('-ddg:mut_file ' + launchDir + '/output/mutFiles/' + str(count) + '.mutfile')  # replaces last line with .mutfile specific
        f.close()
        count += 1


def main():

    mutations_file = sys.argv[1] # user declared list of mutations as first passed argument
    permutations, positions = readMutations(mutations_file)

    writeMutFiles(permutations, positions)
    writeOptionFiles(permutations)

main()
