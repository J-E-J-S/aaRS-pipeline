#!/bin/env python

# USAGE: python queryResults.py mutantQn rmsdCutOff results.json
# A 2Å RMSD Cut-Off is recommended 

import json
import os
import sys
from shutil import copyfile
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import PPBuilder

mutantQn = int(sys.argv[1])
rmsdCutOff = float(sys.argv[2])
resultsJSON = sys.argv[3]


def outputDir(mutantQn, rmsdCutOff, resultsJSON):
    '''Filters mutants based on an RMSD cut off and compiled a results directory '''

    filteredMutants = {} # Results dictionary filtered on RMSD cut-off

    with open(resultsJSON) as json_file:
        data = json.load(json_file)

        # Filter by RMSD cut-off value
        for mutant in data:
            if data[mutant]['RMSD'][0] <= rmsdCutOff:
                filteredMutants[mutant] = data[mutant]

    # Rank mutants based on delta values
    deltaDic = {}
    for mutant in filteredMutants:
        deltaDic[mutant] = filteredMutants[mutant]['Delta'][0]

    rankedMutants = sorted(deltaDic, reverse=True) # lower delta = better

    outputFolder = str(mutantQn) + '_rankedResults'
    os.mkdir(outputFolder)

    if len(rankedMutants) < mutantQn:
        mutantQn = len(rankedMutants) # To stay in index range in event of few mutants

    count = 0
    while count < mutantQn:
        mutantDir = outputFolder + '/' + str(count+1)
        os.mkdir(mutantDir)

        structurePath = filteredMutants[rankedMutants[count]]['structurePath']
        dockingPath = filteredMutants[rankedMutants[count]]['dockingPath']

        copyfile(structurePath, mutantDir + '/' + rankedMutants[count] + '.pdb')
        copyfile(dockingPath, mutantDir + '/' + rankedMutants[count] + '_docking.mol2')

        f = open(mutantDir + '/' + rankedMutants[count] + '.fasta', 'a+')

        f.write('>' + rankedMutants[count] + ' | rank=' + str(count+1) + ' | delta=' + str(filteredMutants[rankedMutants[count]]['Delta'][0]) + ' kcal/mol | dockScore=' + str(filteredMutants[rankedMutants[count]]['exogenousScores'][0]) + ' kcal/mol' + ' | RMSD=' + str(filteredMutants[rankedMutants[count]]['RMSD'][0]) + ' Å\n' )

        structure = PDBParser().get_structure('mutant', structurePath)
        ppb = PPBuilder()
        seq = [] # If dimers then only 1 included (1 polypeptide)
        for pp in ppb.build_peptides(structure):
            seq.append(str(pp.get_sequence()))
        f.write(seq[0] + '\n')
        f.close()

        count += 1



    return outputFolder

def createSummaryFasta(outputFolder):
    ''' Collates all the fasta files into one '''

    f = open(outputFolder + '/rankedResults.fasta', 'a+')

    for root, dirs, files in os.walk(outputFolder):
        for file in files:
            if file.endswith('.fasta'):
                mutantFile = open(os.path.join(root, file), 'r')
                f.write(mutantFile.read())
                mutantFile.close()

    f.close()


def main():

    outputFolder = outputDir(mutantQn, rmsdCutOff, resultsJSON)
    createSummaryFasta(outputFolder)

main()
