#!/usr/bin/env nextflow

optionFiles_ch = Channel.fromPath(launchDir + '/output/optionFiles/*')
rosettaCartesian = launchDir + '/resources/rosetta_bin_linux_2020.08.61146_bundle/main/source/build/src/release/linux/3.10/64/x86/gcc/4.8/static/cartesian_ddg.static.linuxgccrelease'
cbdock = launchDir + '/resources/CB-Dock/prog/AutoBlindDock.pl'

//Passes option Files to Rosetta cartesian for output
process structurePrediction{

    input:
    file optionFile from optionFiles_ch

    output:
    path structureDir into structureDir_ch
    stdout structurePredictionCheckPoint_ch


    script:
    """
    dummyStructure.py @$optionFile > structureDir
    echo 'Completed - ${optionFile}'
    """

}
structurePredictionCheckPoint_ch.view()

//Find lowest free energy structure and outputs path to .pdb file
process minimizedStructure{
    input:
    path structureDir from structureDir_ch

    output:
    stdout mutantStructure into mutantStructure_ch

    shell:
    '''
    min=$(minimizedStructure.py $(dirname $(realpath !{structureDir}))/*.ddg)
    minPath=$(dirname $(realpath !{structureDir}))'/'$min

    echo $minPath
    '''
}
//mutantStructure_ch.view() //debug

//Dock mutant with native substrate
ligand=launchDir + '/inputs/ligand.mol2'
template=launchDir + '/inputs/receptor.pdb'
process nativeDocking{
    input:
    val mutantStructure from mutantStructure_ch

    output:
    stdout results

    shell:
    '''
    outputDir=$(pwd)
    !{cbdock} !{template} !{ligand} 1 $outputDir
    '''
}
results.view()
