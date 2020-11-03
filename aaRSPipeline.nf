#!/usr/bin/env nextflow

optionFiles_ch = Channel.fromPath(launchDir + '/output/optionFiles/*')
rosettaCartesian = launchDir + '/resources/rosetta_bin_linux_2020.08.61146_bundle/main/source/build/src/release/linux/3.10/64/x86/gcc/4.8/static/cartesian_ddg.static.linuxgccrelease'

//Passes option Files to Rosetta cartesian for output
process structurePrediction{

    input:
    file optionFile from optionFiles_ch

    output:
    path structureDir into structureDir_ch


    script:
    """
    test.py @$optionFile > structureDir
    echo 'Completed - ${optionFile}'
    """

}

//Pick up structure prediction dir from structureDir_ch, use basename path (as path will first go to output file)
process nativeDocking {
    input:
    path structureDir from structureDir_ch

    output:
    stdout results

    script:
    """
    realpath $structureDir
    """
}

results.view()
