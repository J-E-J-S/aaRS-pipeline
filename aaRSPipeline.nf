#!/usr/bin/env nextflow

mutations = Channel.fromPath(launchDir + '/inputs/*mutations.txt')

//Calculates a list of permutations for mutations
process mutationPerms{

    input:
    file mutations

    output:
    stdout permutations_ch


    """
    mutationPerms.py ${mutations}
    """

}
//permutations_ch.view() //debug

mutFiles = Channel.fromPath(launchDir + '/output/mutFiles/*.mutfile')
process structurePrediction{

    input:
    file mutFile from mutFiles

    output:
    stdout results

    """
    echo $mutFile
    """
}

results.view()
