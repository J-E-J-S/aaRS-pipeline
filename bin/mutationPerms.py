#!/usr/bin/env python

import os
import sys
from itertools import product

def readMutFile(mutFile):

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


        return positions




mutations_file = sys.argv[1] # user declared list of mutations as first passed argument
readMutFile(mutations_file)
