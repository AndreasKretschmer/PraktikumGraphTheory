from numpy.core.fromnumeric import size
from erdbeermet.simulation import simulate
from erdbeermet.simulation import load
from erdbeermet.recognition import recognize
from erdbeermet.visualize.BoxGraphVis import plot_box_graph
from itertools import permutations
import numpy as np
import os
import timeit

# from erdbeermet.recognition import alt_recognize
from recognition import alt_recognize

def write_simulation_to_file(circular, clocklike, size, history, id):
    result_dir = os.path.join(os.getcwd(), 'sim')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    filename = f'{id}_simulation_circular{circular}_clocklike_{clocklike}_size{size}'
    filename = os.path.join(result_dir,filename)
    history.write_history(filename)

def load_simulations_from_files():
    histories = []
    result_dir = os.path.join(os.getcwd(), 'sim')
    for file in next(os.walk(result_dir), (None, None, []))[2]:
        histories.append(load(os.path.join(result_dir, file)))

    return histories

def create_diff_simulations():
    histories = []
    runtimes = []
    for i in range(15):
        for bool in (True, False):
            for bool2 in (True, False):
                start = timeit.default_timer()
                size = np.random.randint(8, 10)
                history = simulate(size, branching_prob=0.0, circular=bool, clocklike=bool2)
                histories.append(history)

                stop = timeit.default_timer()
                runtimes.append(stop - start)
                write_simulation_to_file(bool, bool2, size, history, i)

    return histories, runtimes

def get_simulations(import_from_file = False):
    if import_from_file:
        return load_simulations_from_files(), []
    else:
        return create_diff_simulations()

def compare_first_leaves(history, candidate):
    first_leaves = history.history[:4]

    leaves_indices = []

    for leaf in first_leaves:
        leaves_indices.append(leaf[2])

    leaves_equal = False
    if candidate.n == 4 and not candidate.info:
        if (set(candidate.V) == set(leaves_indices)):
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


def recognize_histories(histories, first_candidate_only=True, print_info=False, use_modified=False, b_unknown= False):
    runtimes = []
    n_cnt = 0
    errors = 0

    for history in histories:
        n_cnt += 1
        if not b_unknown:
            start = timeit.default_timer()
            rec_tree = recognize(history.D, first_candidate_only=first_candidate_only, print_info=print_info, B={0,1,2,3}, use_modified=use_modified)
            stop = timeit.default_timer()
            runtimes.append(stop - start)
            errors += handle_reconstruction_result(rec_tree, history)
        else:
            V = [i for i in range(history.D.shape[0])]
            for x, y, z in permutations(V, 3):
                start = timeit.default_timer()
                rec_tree = recognize(history.D ,first_candidate_only=first_candidate_only, print_info=print_info, B={x,y,z}, use_modified=use_modified)
                stop = timeit.default_timer()
                runtimes.append(stop - start)
                errors += handle_reconstruction_result(rec_tree, history)
    
    return runtimes, n_cnt, errors

def handle_reconstruction_result(rec_tree, history):
    is_rmap = (rec_tree.root.valid_ways > 0)

    if is_rmap:
        handle_reconstruction_success(history, rec_tree)
        return 0
    else:
        handle_reconstruction_failure(rec_tree)
        return 1

def handle_reconstruction_success(history, rec_tree, print_info=False):
    if print_info: print('Is R-Map!')

    #select an candidate radomly
    candidates = []
    for node in rec_tree.preorder():
        if node.n == 4 and not node.info:
            candidates.append(node)

    if len(candidates) > 1:
        candidate = candidates[np.random.randint(len(candidates)-1)]
    else:
        candidate = candidates[0]

    if print_info:
        print(f'Possible R-Maps: {len(candidates)}')

        leaves_equal = compare_first_leaves(history, candidate)
        print(f'Are first 4 simulation leaves and final 4-leaf map equal? {leaves_equal}')

        common_triple_cnt = divergence_measure(history, rec_tree)
        print(f'Common triples: {common_triple_cnt}')

        print('\n')

def handle_reconstruction_failure(rec_tree, print_info=False):
    print('reconstruction failed')
    for node in rec_tree.preorder():
        V, D, R_step = node.V, node.D, node.R_step
        if print_info:
            print(f'plotting box for {V} .........')
            print('matrix:')
            print(D)

            print('\n')
            print('step:')
            print(R_step)

            # plot_box_graph(D, labels=V)


def average_runtimes(sim_runtimes, rec_runtimes):
    print('\n')
    if len(sim_runtimes) > 0:
        print(f'# sim runtimes: {len(sim_runtimes)}')
        print(f'Average simulation time: {np.mean(sim_runtimes)}s')

    print(f'# rec runtimes: {len(rec_runtimes)}')
    print(f'Average recognition runtime: {np.mean(rec_runtimes)}s')

def reconstruction_success_errors(n, err):
    print('\n')
    print(f'# of errors: {err}')
    print(f'# of succesful steps: {n-err}')
    print(f'succesfull in %: {((n-err)/n)*100}')


def __main__():
    histories, sim_runtimes = get_simulations(import_from_file=True)

    #WP1, WP2
    rec_runtimes, nwp2, err_wp2 = recognize_histories(histories)
    average_runtimes(sim_runtimes, rec_runtimes)
    reconstruction_success_errors(nwp2, err_wp2)

    # #WP3
    rec_runtimes, n_wp3, err_wp3 = recognize_histories(histories, use_modified=True)
    average_runtimes(sim_runtimes, rec_runtimes)
    reconstruction_success_errors(n_wp3, err_wp3)
    # #WP3.1
    rec_runtimes, n_wp3_1, err_wp3_1 = recognize_histories(histories, use_modified=True, b_unknown=True)
    average_runtimes(sim_runtimes, rec_runtimes)
    reconstruction_success_errors(n_wp3_1, err_wp3_1)

    # #WP4
    for history in histories:
        rec_tree = alt_recognize(history.D)

__main__()
