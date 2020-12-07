# aaRS Engineering Pipeline 🧬

## A Scalable Pipeline for the Discovery of aaRS Mutants to Aid in Genetic Code Expansion.

## Introduction
Aminoacyl-tRNA Synthetases (aaRSs) are a class of enzyme central in translation,
facilitating the interaction of tRNAs to a cognate canonical amino acid (CAA).
To enable expansion of the natural chemical toolbox to incude non-canonical
amino acids (NCAAs), new enzymes of this class have to be enginereed to accept
the alternative chemistries offered by NCAAs, while remaining inert to
pre-existing CAAs.

## Workflow
This pipeline is built using Nextflow for innate concurrency and scalability.
The engineering workflow facilitates structure prediction of mutant enzymes
through Rosetta Cartesian energy minimization, followed by blind docking of
native and target (exogenous) amino acids by CB-Dock.

### Scoring
**Delta:**\n
    *NCAA Dock Score - Native Dock Score
    *Lower the score, the greater the engineered affinity for the NCAA over the
    native substrate
**RMSD:**\n
    *Root-Mean-Square Deviation of native and exogenous docked amino acids
    *Measures likelihood of mutant producing a productive docking pose
    *Lower the RMSD, the greater the mutant appears to dock the NCAA in a
    productive pose.
