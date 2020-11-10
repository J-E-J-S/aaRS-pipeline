#!/usr/bin/env python3
# This script is used to identify structure produced by Rosetta Cartesian
# with the lowest free energy.

import os
import sys

def main(file):
    ''' input = .ddg file generates by rosetta cartesian, output = filename of mutant structure with most favourable energy e.g. MUT_32THR_107THR_158PRO_159LEU_162ALA_bj3.pdb '''

    f = open(file, 'r')
    lines = f.readlines() # this generates list where each item is a line in .ddg file

    mutant_energies = {} # dictionary of key = mutant structure file name (.pdb) and value is free energy of structure e.g. {'MUT_32THR_107THR_158PRO_159LEU_162ALA_bj1.pdb': -335.174, 'MUT_32THR_107THR_158PRO_159LEU_162ALA_bj2.pdb': -334.593, 'MUT_32THR_107THR_158PRO_159LEU_162ALA_bj3.pdb': -335.658}

    # this loop goes through .ddg file and adds to dictionary the free energy + the local name for the mutant structure
    count = 3
    while count < 6:

        line = lines[count] # access lines in .ddg starting at first mutant line
        list_string = line.split() # splits line into strings

        mutant_energy = float(list_string[3]) # mutant energy is 4th strings in line
        mutant_name = list_string[2] + '_bj' + str(count-2) + '.pdb' # this is the local name for the cognate mutant file
        mutant_name = mutant_name.replace(':', '') # formatting

        mutant_energies[mutant_name] = mutant_energy

        count += 1

    f.close()

    fav_structure = min(mutant_energies, key=mutant_energies.get) # returns the file name of the most favourable energy structure from rosetta

    return fav_structure


print(main(sys.argv[1]))
