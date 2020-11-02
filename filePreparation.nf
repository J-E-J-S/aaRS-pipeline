#!/usr/bin/env nextflow

mutations = Channel.fromPath(launchDir + '/inputs/*mutations.txt')

//Calculates a list of permutations for mutations
process filePreperation{

    input:
    file mutations

    output:
    stdout results

    """
    filePreparation.py ${mutations}
    echo 'File Preparation Complete.'
    """

}
//permutations_ch.view() //debug
results.view()
