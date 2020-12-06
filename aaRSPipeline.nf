#!/usr/bin/env nextflow

println """

################################################################################
THANKS FOR USING THE aaRS PIPELINE - AIDING GENETIC CODE EXPANSION.
Version - 1.0
Author - James Sanders
################################################################################

"""

// Declare Global Variables
optionFiles_ch = Channel.fromPath(launchDir + '/output/optionFiles/*')
rosettaCartesian = launchDir + '/resources/rosetta_bin_linux_2020.08.61146_bundle/main/source/build/src/release/linux/3.10/64/x86/gcc/4.8/static/cartesian_ddg.static.linuxgccrelease'
cbdock = launchDir + '/resources/CB-Dock/prog/AutoBlindDock.pl'

// Passes option Files to Rosetta Cartesian for Structure Prediction
process structurePrediction{

    input:
    file optionFile from optionFiles_ch

    output:
    path structureDir into structureDir_ch
    stdout mutantID_ch


    script:
    """
    dummyStructure.py @$optionFile > structureDir # replace with rossetaCartesian when in prod.
    echo ${optionFile}
    """

}
//structurePredictionCheckPoint_ch.view()


// Finds the Lowest Free Energy Structure and Outputs Path to .pdb File
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


// Docks Mutant with Native Substrate Supplied in /inputs/ dir
nativeLigand=launchDir + '/inputs/nativeLigand.mol2'
process nativeDocking{
    input:
    val mutantStructure from mutantStructure_ch

    output:
    path nativeDocking into nativeDocking_ch
    stdout mutantStructure2_ch

    shell:
    '''
    outputDir=$(pwd)

    # Create Replicate Dirs
    mkdir 1
    mkdir 2
    mkdir 3

    main="!{cbdock} !{mutantStructure}" # solves bug if concatanated together
    echo Replicate 1: >> nativeDocking
    $main !{nativeLigand} 1 "$outputDir/1" >> nativeDocking
    echo Replicate 2: >> nativeDocking
    $main !{nativeLigand} 1 "$outputDir/2" >> nativeDocking
    echo Replicate 3: >> nativeDocking
    $main !{nativeLigand} 1 "$outputDir/3" >> nativeDocking

    # Pass on mutant structure for use by exogenous docking
    echo !{mutantStructure}
    '''
}


// Docks Mutant with Target Substrate Supplied in /inputs/ dir
exogenousLigand=launchDir = launchDir + '/inputs/exogenousLigand.mol2'
process exogenousDocking{
    input:
    val mutantStructure from mutantStructure2_ch

    output:
    path exogenousDocking into exogenousDocking_ch

    shell:
    '''
    outputDir=$(pwd)

    mkdir 1
    mkdir 2
    mkdir 3

    main="!{cbdock} !{mutantStructure}" # solves bug if concatanated together
    echo Replicate 1: >> exogenousDocking
    $main !{exogenousLigand} 1 "$outputDir/1" >> exogenousDocking
    echo Replicate 2: >> exogenousDocking
    $main !{exogenousLigand} 1 "$outputDir/2" >> exogenousDocking
    echo Replicate 3: >> exogenousDocking
    $main !{exogenousLigand} 1 "$outputDir/3" >> exogenousDocking
    '''
}

// Process Docking Results into a JSON for Analysis
process docktoJSON{
    input:
    path nativeDocking from nativeDocking_ch
    path exogenousDocking from exogenousDocking_ch
    val mutantID from mutantID_ch

    output:
    stdout results

    shell:
    '''
    nativeDocking=$(dirname $(realpath !{nativeDocking}))
    exogenousDocking=$(dirname $(realpath !{exogenousDocking}))

    docktoJSON.py $nativeDocking $exogenousDocking !{mutantID}
    '''
}

results.view()
