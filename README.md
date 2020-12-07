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
followed by blind docking of native and target (exogenous) amino acids.

## Scoring
