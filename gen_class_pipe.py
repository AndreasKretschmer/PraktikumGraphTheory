from time import time
from numpy.core.fromnumeric import size
from erdbeermet.simulation import simulate
from erdbeermet.simulation import load
from erdbeermet.recognition import recognize
from erdbeermet.visualize.BoxGraphVis import plot_box_graph
from itertools import permutations

import numpy as np
import os
import timeit

from loguru import logger
from recognition import alt_recognize

def write_simulation_to_file(path, filename, history):
    full_path = os.path.join(os.getcwd(), path)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    filename = os.path.join(full_path, filename)
    history.write_history(filename)



def load_simulations_from_files(max_files = -1):
    logger.debug(f'Loading simulations...')

    histories = []

    result_dir = os.path.join(os.getcwd(), 'sim')
    for index, file in enumerate(next(os.walk(result_dir), (None, None, []))[2]):
        histories.append((load(os.path.join(result_dir, file)), file))

        if max_files > 0 and index + 1 == max_files:
            break

    logger.debug(f'Successfully loaded {max_files if max_files >= 0 else "all"} simulations!')

    return histories



def create_diff_simulations(n):
    logger.debug(f'Creating {4 * n} histories...')

    histories = []
    for circular in (True, False):
        for clocklike in (True, False):
            logger.debug(f'Creating{" circular" if circular else " NOT circular"}{" clocklike" if clocklike else " NOT clocklike"} simulations...')
            for i in range(n):
                size = np.random.randint(6, 10)
                history = simulate(size, branching_prob=0.0, circular=circular, clocklike=clocklike)

                path = f'sim'
                filename = f'{i}_{size}'

                if circular: filename += f'_circular'
                if clocklike: filename += f'_clocklike'
                histories.append((history, filename))

                write_simulation_to_file(path, filename, history)

    logger.debug(f'Finished creating histories!')

    return histories



def compare_first_leaves(history, candidate):
    first_leaves = [0,1,2,3] 
    # die ersten 4 Blätter wurden gleich [1,2,3,4] gesetzt, diese wurden jetzt mit den richtigen 4 Blättern gefüllt

    leaves_equal = False
    if candidate.n == 4 and not candidate.info:
        if (set(candidate.V) == set(first_leaves)):
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



def recognize_histories(histories, first_candidate_only=True, print_info=False, use_modified=False, mode=''):
    runtimes = []
    runs = 0
    errors = []
    common_triplets_total = []
    leaves_equal_total = []

    logger.debug(f'Recognizing {len(histories)} histories...')

    for (history, file) in histories:
        runs += 1

        if runs % 100 == 0:
            logger.debug(f'{runs} histories recognized!')

        if (mode == 'WP2'):
            start = timeit.default_timer()
            rec_tree = recognize(
                history.D,
                first_candidate_only=first_candidate_only,
                print_info=print_info,
                B={0,1,2,3},
                use_modified=use_modified
            )
            stop = timeit.default_timer()

        elif (mode == 'WP3'):
            start = timeit.default_timer()
            rec_tree = recognize(
                history.D,
                first_candidate_only=first_candidate_only,
                print_info=print_info,
                B={0,1,2,3},
                use_modified=use_modified
            )
            stop = timeit.default_timer()

        elif (mode == 'WP31'):
            V = [i for i in range(history.D.shape[0])]
            rec_tree = any

            start = timeit.default_timer()
            for x, y, z in permutations(V, 3):
                rec_tree = recognize(
                    history.D,
                    first_candidate_only=first_candidate_only,
                    print_info=print_info,
                    B={x,y,z},
                    use_modified=use_modified
                )

                if (rec_tree.root.valid_ways > 0): break
            stop = timeit.default_timer()

        elif (mode == 'WP4'):
            start = timeit.default_timer()
            rec_tree = alt_recognize(history.D, first_candidate_only=True, print_info=print_info) # das "first_candidate_only=True" wurde in der ersten Auswertung leider vergessen
            stop = timeit.default_timer()

        runtimes.append(stop - start)
        error, leaves_equal, common_triplets = handle_reconstruction_result(rec_tree, history)
        errors.append(error)
        if error:
            logger.error(f'File: {file}')
        common_triplets_total.append(common_triplets)
        leaves_equal_total.append(leaves_equal)

    logger.debug(f'Finished recognizing {runs} histories!')

    return runtimes, runs, errors, leaves_equal_total, common_triplets_total



def handle_reconstruction_result(rec_tree, history):
    is_rmap = (rec_tree.root.valid_ways > 0)

    if is_rmap:
        leaves_equal, common_triplets_cnt = handle_reconstruction_success(history, rec_tree, False)
        return 0, leaves_equal, common_triplets_cnt
    else:
        handle_reconstruction_failure(rec_tree, True)
        return 1, 0, 0



def handle_reconstruction_success(history, rec_tree, print_info=False):
    candidates = []

    for node in rec_tree.preorder():
        if node.n == 4 and not node.info:
            candidates.append(node)

    if len(candidates) > 1:
        candidate = candidates[np.random.randint(len(candidates)-1)]
    else:
        candidate = candidates[0]

    leaves_equal = compare_first_leaves(history, candidate)
    common_triple_cnt = divergence_measure(history, rec_tree)

    if print_info:
        logger.info('r-map found!')

        message = """
            possible r-maps: {possible_rmaps}
            are first 4 simulation leaves and final 4-leaf map equal? {leaves_equal}
            common triples: {common_triple_cnt}
        """.format(
            possible_rmaps=len(candidates),
            leaves_equal=leaves_equal,
            common_triple_cnt=common_triple_cnt
        )

        logger.info(message)

    return leaves_equal, common_triple_cnt



def handle_reconstruction_failure(rec_tree, print_info=False):
    if print_info:
        logger.info('reconstruction failed!')

        for node in rec_tree.preorder():
            message = """
                plotting box for {V}

                matrix:
                {D}

                step:
                {r_step}
            """.format(
                V=node.V,
                D=node.D,
                r_step=node.R_step
            )

            logger.info(message)



def average_runtimes(rec_runtimes):
    message = """
        # rec runtimes: {runtimes}
        average recognition runtime: {mean_runtimes}s
    """.format(
        runtimes=len(rec_runtimes),
        mean_runtimes=np.mean(rec_runtimes)
    )

    logger.info(message)



def reconstruction_success_errors(n, err, leaves_equal, common_triplet_cnt):
    message = """
        # of errors: {error_count}
        # of succesful steps: {successful_steps_count}
        succesfull in %: {successful_steps_percentage}
        # average common triplets: {average_common_triplets}
        sum of leaves rmap equal to first leaves: {equal_leaves}
    """.format(
        error_count=np.sum(err),
        successful_steps_count=n - np.sum(err),
        successful_steps_percentage=((n - np.sum(err)) / n) * 100,
        average_common_triplets=np.mean(common_triplet_cnt),
        equal_leaves=np.sum(leaves_equal)
    )

    logger.info(message)


def __main__():
    logger.add("logs/debug.log", filter=lambda record: record["level"].name == "DEBUG")
    logger.add("logs/info.log", filter=lambda record: record["level"].name == "INFO")
    logger.add("logs/warn.log", filter=lambda record: record["level"].name == "WARN")
    logger.add("logs/error.log", filter=lambda record: record["level"].name == "ERROR")

    histories = create_diff_simulations(10)
    # histories = load_simulations_from_files()

    # WP1, WP2
    logger.debug(f'Running workpages 1 and 2...')
    rec_runtimes, runs, errors, leaves_equal_total, common_triplets_total = recognize_histories(
        histories,
        mode='WP2'
    )
    average_runtimes(rec_runtimes)
    reconstruction_success_errors(runs, errors, leaves_equal_total, common_triplets_total)


    # # WP3
    logger.debug(f'Running workpage 3...')
    rec_runtimes, runs, errors, leaves_equal_total, common_triplets_total = recognize_histories(
        histories,
        use_modified=True,
        mode='WP3'
    )
    average_runtimes(rec_runtimes)
    reconstruction_success_errors(runs, errors, leaves_equal_total, common_triplets_total)


    # # WP3.1
    logger.debug(f'Running workpage 3.1...')
    rec_runtimes, runs, errors, leaves_equal_total, common_triplets_total = recognize_histories(
        histories,
        use_modified=True,
        mode='WP31'
    )
    average_runtimes(rec_runtimes)
    reconstruction_success_errors(runs, errors, leaves_equal_total, common_triplets_total)


    # # WP4
    logger.debug(f'Running workpage 4...')
    rec_runtimes, runs, errors,leaves_equal_total, common_triplets_total = recognize_histories(
        histories,
        use_modified=False, # bei der ersten Auswertung wurde die Erweiterung von WP3 in WP4 mit benutzt das wurde hier korrigiert
        mode='WP4'
    )
    average_runtimes(rec_runtimes)
    reconstruction_success_errors(runs, errors, leaves_equal_total, common_triplets_total)

__main__()
