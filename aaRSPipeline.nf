#!/usr/bin/env nextflow

mutations = Channel.fromPath(launchDir + '/inputs/*mutations.txt')

//Calculates a list of permutations for mutations
process mutationPerms{

    input:
    file mutations

    output:
    stdout x into permutations_ch

    script:

    """
    mutationPerms.py ${mutations}
    """

}
//permutations_ch.view() //debug

process writeMutFile{

    input:
    val permutations_ch
    output:
    stdout results

    """
    test.py $permutations_ch
    """
}

results.view()
