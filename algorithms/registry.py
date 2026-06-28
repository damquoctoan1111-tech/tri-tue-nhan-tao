from algorithms.uninformed_search.bfs import bfs
from algorithms.uninformed_search.dfs import dfs
from algorithms.uninformed_search.ucs import ucs
from algorithms.uninformed_search.ids import ids

from algorithms.informed_search.gbfs import gbfs
from algorithms.informed_search.astar import astar
from algorithms.informed_search.idastar import idastar

from algorithms.local_search.simple_hill_climbing import simple_hill_climbing
from algorithms.local_search.stochastic_hill_climbing import stochastic_hill_climbing
from algorithms.local_search.random_restart_hill_climbing import random_restart_hill_climbing
from algorithms.local_search.local_beam_search import local_beam_search
from algorithms.local_search.simulated_annealing import simulated_annealing

from algorithms.complex_environment.belief_no_observation import belief_no_observation
from algorithms.complex_environment.belief_partial_observation import belief_partial_observation
from algorithms.complex_environment.and_or_graph_search import and_or_graph_search

from algorithms.csp.backtracking_search import backtracking_search
from algorithms.csp.forward_checking import forward_checking
from algorithms.csp.ac3_search import ac3_search
from algorithms.csp.min_conflicts import min_conflicts

from algorithms.adversarial_search.minimax import minimax
from algorithms.adversarial_search.alpha_beta_pruning import alpha_beta_pruning
from algorithms.adversarial_search.expectimax import expectimax

ALGORITHM_GROUPS = {
    'Uninformed Search': {'BFS': bfs, 'DFS': dfs, 'UCS': ucs, 'IDS': ids},
    'Informed Search': {'GBFS': gbfs, 'A*': astar, 'IDA*': idastar},
    'Local Search': {
        'Simple Hill Climbing': simple_hill_climbing,
        'Stochastic Hill Climbing': stochastic_hill_climbing,
        'Random Restart Hill Climbing': random_restart_hill_climbing,
        'Local Beam Search': local_beam_search,
        'Simulated Annealing': simulated_annealing,
    },
    'Searching in Complex Environments': {
        'Belief State Search (No observation)': belief_no_observation,
        'Belief State Search (Partial observation)': belief_partial_observation,
        'AND-OR Graph Search': and_or_graph_search,
    },
    'Constraint Satisfaction Problems - CSP': {
        'Backtracking Search': backtracking_search,
        'Forward Checking': forward_checking,
        'AC-3 Search': ac3_search,
        'Min-Conflicts': min_conflicts,
    },
    'Adversarial Search': {
        'Minimax': minimax,
        'Alpha-Beta Pruning': alpha_beta_pruning,
        'Expectimax': expectimax,
    },
}

HEURISTIC_ALGORITHMS = {
    'GBFS','A*','IDA*','Simple Hill Climbing','Stochastic Hill Climbing','Random Restart Hill Climbing',
    'Local Beam Search','Simulated Annealing','Belief State Search (No observation)',
    'Belief State Search (Partial observation)','AND-OR Graph Search','Forward Checking','AC-3 Search',
    'Min-Conflicts','Minimax','Alpha-Beta Pruning','Expectimax'
}
