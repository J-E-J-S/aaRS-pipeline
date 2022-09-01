# An aaRS Engineering Pipeline 🧬

## A Scalable Pipeline for the Discovery of aaRS Mutants to Aid in Genetic Code Expansion.

## Introduction
Aminoacyl-tRNA Synthetases (aaRSs) are a class of enzyme central to translation,
facilitating the interaction of tRNAs to a cognate canonical amino acid (CAA).
To enable expansion of the natural chemical toolbox to encompass non-canonical
amino acids (NCAAs), new enzymes of this class have to be enginereed to accept
the alternative chemistries offered by NCAAs, while remaining inert to
pre-existing CAAs.

![](assets/translation.jpg)

## Workflow
The engineering workflow facilitates structure prediction of the complete  
permutational complexity of the defined mutant landscape through [Rosetta Cartesian](https://www.rosettacommons.org/docs/latest/cartesian-ddG) energy minimization, followed by blind docking of
native and target (exogenous) amino acids by [CB-Dock](http://clab.labshare.cn/cb-dock/php/).
Mutants are then scored for fitness using the Delta and RMSD metrics.

![](assets/pipeline.jpg)

## Scoring
**Delta:**
* Measures enzyme engineered favourability as: `NCAA Dock Score - Native Dock Score`
* Lower the score, the greater the engineered affinity for the NCAA over the
native substrate

**RMSD:**
* Estimation metric of the mutant producing a productive docking pose with the
target NCAA
* Root-Mean-Square Deviation of the exogenously docked NCAA to the crystal-structure
derived docking position of the native amino acid
* Lower the RMSD, the greater the mutant appears to dock the NCAA in a
productive binding pose.

## Prerequisites  
This pipeline uses the Rosetta 3 cartesian_ddg script for structure prediction.
This software suite is incredibly large (~18Gb compressed) and so can't be packaged
within this repository. [Download here](https://www.rosettacommons.org/software/license-and-download) and move the uncompressed directory with binaries (or compile yourself), to the /resources/ directory.  
(Version rossetta_bin_linux_2020.08.61146_bundle)     

## Quick Start  
This is a [Nextflow](https://www.nextflow.io/) pipeline and as such, can only be
run on a POSIX OS, if using windows I'd recommend using the [Windows Subsystem for
Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10)  
1. `git clone https://github.com/J-E-J-S/aaRS-pipeline`
2. `conda env create -f environment.yml`
3. `conda activate aaRS-pipeline`
4. `./aaRS-pipeline.sh -i -m -r`

## Usage
### Inputs
1. Create a `mutations.txt` file in the `/inputs/` directory   
Must be in form:
```
X99 MNQ
Y100 MNQ
Z101 MNQ
```
Where:
* X is the single-letter ID for the wild-type residue to be mutated
* The number '99' is the residue number of the mutable position
* MNQ is the pool of residues to be mutated at this position

2. Add the native and exogenous (target) amino acids to the `/inputs/` directory
* Amino acids have to be labelled as `nativeLigand.mol2` and `exogenousLigand.mol2` respectively
* Amino acids must be in `.mol2` standard
* The native amino acids must be taken from the known crystal structure of the template enzyme
    * This permits the RMSD calculation to estimate the productivity of the NCAA docking pose

3. Add the template enzyme `.pdb` file to the `/inputs/` directory
### Running the Pipeline
* To install the prerequisite scripts run the shell script with the `-i` option (this only has to be performed once)
`./aaRS-pipeline.sh -i `
* To prepare the mutational file system to begin pipeline flow, run the shell script with the `-m` option (this has to be performed for every new template enzyme or mutational context)    
`./aaRS-pipeline.sh -m`
* To begin the pipeline, run the shell script with the `-r` option  
`./aaRS-pipeline.sh -r` or run cmd `nextflow run main.nf`
* To run pipeline from beginning to end as a new user, combine all options  
`./aaRS-pipeline.sh -i -m -r`
### Results
Results are compiled into a JSON object that can be found in the `/output/`
directory, in the form:  
```
{
    mutantID:
                {
                    'exogenousScores': [],
                    'nativeScore': float,
                    'Delta': [],
                    'RMSD' : [],
                    'structurePath': string,
                    'dockingPath': string
                }
}
```  
This file becomes the store for all the data for the pipeline run.  
### Querying Results  
1. Run the script: `python queryResults.py <mutantQn> <rmsdCutOFf> <./../output/results.json>`
in the /bin/ dir  
Where:      
* mutantQn = number of mutants desired to filter down to  
* rmsdCutOff = the minimal accepted RMSD value (2Å recommended)  
* /output/results.json = path to the pipeline generated results.json  
Creates individual summary directories for mutants with the structure`.pdb`,  
docking_results`.mol2` and a summary `.fasta` file, as well as an overall  
summary `.fasta` file.     
2. Manually inspect the results in PyMOL against the wild-type template  
* Look for similarity in binding mode of the target NCAA to the native CAA  
* Mutant Structure `.pdb` and NCAA docking results `.mol2` are compiled into
the queried results generated directory  
