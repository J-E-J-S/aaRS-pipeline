#!/usr/bin/env python

# Feed in dirname $(realpath <dockfile>) so sysargv is directory holding replicates
# First arg is native, Second is exogenous

import os
import sys
from biopandas.mol2 import PandasMol2
from biopandas.mol2 import split_multimol2
import pandas as pd
import json

# Declare Global Variables
nativeDockingDir = sys.argv[1]
binDir = os.path.dirname(sys.argv[0])
exogenousDockingDir = sys.argv[2]
mutantID = sys.argv[3].replace('_option', '')

#Tested - working
def findLogFiles(mutantDockDir):
    ''' Input = path to mutant docking dir holding CB-Dock outputs (replicates),
    Output = list of paths to log files for each replicates holding docking scores in order 1_pAF, 1_Tyr, 2_pAF... '''

    log_paths = [] # holds list of paths to log files for replicates in order 1_pAF, 1_Tyr, 2_pAF..

    for root, dirs, files in os.walk(mutantDockDir):
        for file in files:
            if file.endswith('log.txt'):
                log_file = os.path.join(root, file) # creates path for log file
                log_paths.append(log_file)

    return log_paths

#Tested - working
def calculateDockScore(log_file):
    ''' Input = CB-Dock generated log file, Output = list of docking scores in order '''

    dockscore_list = [] # holds docking scores from log file  - [highest, ... , lowest]

    f = open(log_file, 'r')
    lines = f.readlines()

    for number in range(35, 44): # some dockings don't generate 9 dockings, check for errors in handling log file
        try:
            mode = lines[number].split() # docking score line as list of items
        except IndexError:
            continue
        try:
            score = float(mode[1])
            dockscore_list.append(score)
        except ValueError: # error if item is a str
            continue
        except IndexError: # error if item != exist
            continue

    return dockscore_list

def findCoreAtoms(moleculePath):
    '''Locates corner stone atoms in an amino acid (CA, CB, OXT)'''

    molecule = PandasMol2().read_mol2(moleculePath)

    CaId = molecule.df['atom_name'][molecule.df['atom_name'] == 'CA'].index[0] + 1
    CbId = molecule.df['atom_name'][molecule.df['atom_name'] == 'CB'].index[0] + 1
    OxtId = molecule.df['atom_name'][molecule.df['atom_name'] == 'OXT'].index[0] + 1

    return CaId, CbId, OxtId

# Please forgive me for this fn, future implement a better Graph Theory solution. Only works if amino acid has CA, CB, OXT labelled as such
def calculateBackbone(moleculePath):
    ''''Input = amino acid .mol2 file, Output = Dictionary of backbone residues to atom id in .mol2 file '''

    moleculeFile = open(moleculePath).readlines()

    # Remove residual .mol2 formatting --> really quite unnecessary
    for i in range(len(moleculeFile)):
        moleculeFile[i] = moleculeFile[i].replace('\n', '')

    index_bond = moleculeFile.index('@<TRIPOS>BOND')
    index_sub = moleculeFile.index('@<TRIPOS>SUBSTRUCTURE')

    bondNetwork = [] # Holds list of bond network as list of lists ready for df conversion
    for i in range(index_bond+1, index_sub):
        bondNetwork.append(moleculeFile[i].split())

    df = pd.DataFrame(bondNetwork)
    df = df.drop([0,3], axis=1) # These columns contain bond_id and bond_type --> unneccesary
    df = df.rename(columns={1:'origin', 2:'target'}) # Make df more clear

    CaId, CbId, OxtId = findCoreAtoms(moleculePath) # Retrieve core atom ids from .mol2 file

    backbone = {'CA':CaId, 'OXT':OxtId} # Holds atom name to atom_id in .mol2 of backbone atoms

    bondPairs = [] # Holds pair of bonds
    for index,row in df.iterrows():
        pair = [int(row['origin']), int(row['target'])]
        bondPairs.append(pair)

    # Find atoms bonded to CA that arnt CB
    CaNeighbours = []
    for pair in bondPairs:
        if (CaId in pair) and (CbId not in pair):
            pair.remove(CaId)
            CaNeighbours.append(pair[0])

    # Find CA neighbouring atoms pairing
    miscNeighbours = []
    for pair in bondPairs:
        if (CaNeighbours[0] in pair or CaNeighbours[1] in pair) and (len(pair) != 1):
            miscNeighbours.append(pair[0])
            miscNeighbours.append(pair[1])

    # Find N and C by process of deduction
    if (CaNeighbours[0] not in miscNeighbours):
        backbone['N'] = CaNeighbours[0]
        backbone['C'] = CaNeighbours[1]
    else:
        backbone['N'] = CaNeighbours[1]
        backbone['C'] = CaNeighbours[0]

    # Find O through deduction
    for pair in bondPairs:
        if (backbone['C'] in pair) and (len(pair) != 1) and (backbone['OXT'] not in pair):
            pair.remove(backbone['C'])
            backbone['O'] = pair[0]

    return backbone

def calculateRMSD(replicateDir, nativeLigandPath, exogenousLigandPath):
    ''' Input = path of greatest docking score pAF replicate and Tyr.mol2 from pdb:1j1u, Output = list of rmsd values for all docking modes '''

    rmsds = [] # holds rmsd values for docking modes (in order)

    nlDic = calculateBackbone(nativeLigandPath) # Dictionary of backbone atoms to atom_id in .mol2
    nativeLigand = PandasMol2().read_mol2(nativeLigandPath)
    nativeLigandSele = nativeLigand.df.iloc[[nlDic['N']-1,nlDic['CA']-1,nlDic['C']-1,nlDic['O']-1,nlDic['OXT']-1 ], :] # Just backbone atoms

    elDic = calculateBackbone(exogenousLigandPath)
    # Caculates RMSD for each mode frame in the docking generated results.mol2 file
    for root, dirs, files in os.walk(replicateDir):
        for file in files:
            if file.endswith('.mol2') and file != 'ligand.mol2': # two .mol2 files in docking output, one called ligand.mol2 always, other = result
                exogenousModePath = os.path.join(root, file)
                for mol2 in split_multimol2(exogenousModePath): # splits multi .mol2 into seperate mol2 dataframes
                    exogenousDockingMode = PandasMol2().read_mol2_from_list(mol2_lines=mol2[1], mol2_code=mol2[0])
                    exogenousModeSele = exogenousDockingMode.df.iloc[[elDic['N']-1, elDic['CA']-1, elDic['C']-1, elDic['O']-1, elDic['OXT']-1], :]
                    rmsd = PandasMol2.rmsd(nativeLigandSele, exogenousModeSele, heavy_only=True) # calculates rmsd score for individual frame to Tyrosine docked in pdb:1j1u, H exluded
                    rmsds.append(rmsd)

    return rmsds

def createSummaryDic(nativeDockingDir, exogenousDockingDir):
    '''Input = parent dirs of mutants native and exogenous Docking Dirs, Output = Results Dic '''

    nlLogs = findLogFiles(nativeDockingDir) # Returns list of 3 log file paths
    elLogs = findLogFiles(exogenousDockingDir)

    nlScores = [] # Holds greatest Dock Scores for native across 3 log files
    for path in nlLogs:
        nlScores.append(calculateDockScore(path)[0]) # Only need first item of list as this will be greatest native score

    elScores = {} # Holds greatest dock score : path of its log file
    for path in elLogs:
        elScores[calculateDockScore(path)[0]] = path # This needs to be path to log file because will be looped later

    summaryDic = {'exogenousScores': '', 'nativeScore':'', 'Delta':'', 'RMSD':'' } # Results for mutant

    elMaxDock = min(elScores) # finds lowest key value in dic i.e. greatest docking score
    elMaxLog = elScores[elMaxDock] # finds path to log file of greatest docking scoring replicate
    elScoreList = calculateDockScore(elMaxLog) # Docking Scores for all modes in highest scoring replicate as list
    summaryDic['exogenousScores'] = elScoreList # Updates the results dictionary to hold all modes scores

    nlMaxDock = min(nlScores) # Find lowest tyrosine score i.e. Greatest docking scoring
    summaryDic['nativeScore'] = nlMaxDock # Update results dictionary for native score

    deltas = []
    for score in elScoreList:
        deltas.append(round(score-nlMaxDock,1)) # Bug if don't round
    summaryDic['Delta'] = deltas # Update results dictionary for deltas

    rmsd = calculateRMSD(os.path.dirname(elScores[elMaxDock]), binDir+'/../inputs/nativeLigand.mol2', binDir+'/../inputs/exogenousLigand.mol2')
    summaryDic['RMSD'] = rmsd

    return summaryDic

def updateJSON(summaryDic):
    '''Input = the mutants summary results dictionary, fn updates the results JSON file'''
    mutantObject = {'mutant_'+ mutantID:summaryDic} # {mutant_1: {pAF_scores:, Tyr_score:, Delta:}, mutant_2:{pAF_score:, Tyr_score:, Delta:}....}

    # Checks to see if this is first mutant result
    if os.path.isfile(binDir+'/../output/results.json') != True:
        f = open(binDir+'/../output/results.json', 'w')
        f.write('{}')
        f.close()

    with open(binDir+'/../output/results.json', 'r+') as file:
        data = json.load(file)
        data.update(mutantObject)
        file.seek(0)
        json.dump(data, file)


def main():

    updateJSON(createSummaryDic(nativeDockingDir, exogenousDockingDir))
    print("Completed - Mutant " + mutantID) # output to nextflow console for progress check

main()
