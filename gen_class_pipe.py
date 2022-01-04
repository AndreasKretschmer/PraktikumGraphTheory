from numpy.core.fromnumeric import size
from erdbeermet.simulation import simulate
from erdbeermet.recognition import recognize
from erdbeermet.visualize.BoxGraphVis import plot_box_graph
import numpy as np
import os

def create_diff_simulations():
    histories = []
    for bool in (True, False):
        for bool2 in (True, False):
            histories.append(simulate(np.random.randint(4,9), branching_prob=0.0, circular=bool, clocklike=bool2))

    return histories

def compare_first4leaves(history, rec_tree):
    first4leaves = history.d[:4]
    for candidate in rec_tree.preorder():
        print(f'Candidate: {candidate}.......... Actual first 4 leaves: {first4leaves}')

def recognize_histories(histories, first_candidate_only=False, print_info= False):
    for history in histories:
        rec_tree = recognize(history.D, first_candidate_only=first_candidate_only, print_info=print_info)
        
        is_rmap = (rec_tree.root.valid_ways > 0)
        if is_rmap:
            compare_first4leaves()
        else:
            handle_reconstruction_failure()

def handle_reconstruction_failure(rec_tree):
    print('reconstruction failed')
    for v in rec_tree.preorder():
        if v.n == 4 and v.info == 'spikes too short':
            V, D = v.V, v.D
            print(f'plotting box for {V} .........')
            print('matrix:')
            print(D)

            plot_box_graph(D, labels=V)

def __main__():
    histories = create_diff_simulations()
    recognize_histories(histories, first_candidate_only=True)

__main__()