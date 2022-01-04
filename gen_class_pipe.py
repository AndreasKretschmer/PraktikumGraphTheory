from numpy.core.fromnumeric import size
from erdbeermet.simulation import simulate
from erdbeermet.recognition import recognize
from erdbeermet.visualize.BoxGraphVis import plot_box_graph
import numpy as np
import os
import timeit


def create_diff_simulations():
    histories = []
    runtimes = []
    for bool in (True, False):
        for bool2 in (True, False):
            start = timeit.default_timer()

            histories.append(simulate(np.random.randint(
                4, 9), branching_prob=0.0, circular=bool, clocklike=bool2))

            stop = timeit.default_timer()
            runtimes.append(stop - start)

    return histories, runtimes


def compare_first_leaves(history, rec_tree):
    first_leaves = history.history[:4]

    leaves_indices = []

    for leaf in first_leaves:
        leaves_indices.append(leaf[2])

    leaves_equal = False
    for node in rec_tree.preorder():
        if node.n == 4 and not node.info:
            # print(
            #     f'Candidate: {node.V}.......... Actual first 4 leaves: {leaves_indices}')

            if (node.V == leaves_indices):
                leaves_equal = True

    return leaves_equal


def divergence_measure(history, rec_tree):
    reconstructed_steps = []
    for node in rec_tree.preorder():
        if node.R_step:
            n = node.R_step
            reconstructed_steps.append((n[0], n[1], n[2]))

    true_steps = []
    for s in history.history:
        true_steps.append((s[0], s[1], s[2]))

    common_triple_cnt = 0

    for reconstructed_step in reconstructed_steps:
        for true_step in true_steps:
            if reconstructed_step == true_step:
                common_triple_cnt += 1

    return common_triple_cnt


def recognize_histories(histories, first_candidate_only=True, print_info=False):
    runtimes = []

    for history in histories:
        start = timeit.default_timer()
        rec_tree = recognize(
            history.D, first_candidate_only=first_candidate_only, print_info=print_info)

        stop = timeit.default_timer()
        runtimes.append(stop - start)

        is_rmap = (rec_tree.root.valid_ways > 0)

        if is_rmap:
            print('Is R-Map!')

            leaves_equal = compare_first_leaves(history, rec_tree)
            print(
                f'Are first 4 simulation leaves and final 4-leaf map equal? {leaves_equal}')

            common_triple_cnt = divergence_measure(history, rec_tree)
            print(f'Common triples: {common_triple_cnt}')

            print('\n')

        else:
            handle_reconstruction_failure()

    return runtimes


def handle_reconstruction_failure(rec_tree):
    print('reconstruction failed')
    for node in rec_tree.preorder():
        V, D, R_step = node.V, node.D, node.R_step
        print(f'plotting box for {V} .........')
        print('matrix:')
        print(D)

        print('\n')
        print('step:')
        print(R_step)

        plot_box_graph(D, labels=V)


def average_runtimes(sim_runtimes, rec_runtimes):
    print(f'Average simulation time: {np.mean(sim_runtimes)}s')

    print(f'Average recognition runtime: {np.mean(rec_runtimes)}s')


def __main__():
    histories, sim_runtimes = create_diff_simulations()
    rec_runtimes = recognize_histories(histories)

    average_runtimes(sim_runtimes, rec_runtimes)


__main__()
