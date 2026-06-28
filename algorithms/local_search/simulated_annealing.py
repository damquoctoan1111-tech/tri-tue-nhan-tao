import random
import math
from algorithms.core import (
    BoardState,
    benchmark_timer,
    generate_adjacent_states,
    build_result_pack,
    get_heuristic_function,
    MAX_NODE_LIMIT
)

@benchmark_timer
def simulated_annealing(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    curr = start_state
    current_path = [curr]
    action_history = []
    nodes_expanded = 0
    nodes_generated = 1
    temperature = 25.0
    cooling_rate = 0.995
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    while nodes_expanded < node_limit and temperature > 0.001:
        if curr == goal_state:
            return build_result_pack(True, current_path, action_history, nodes_expanded, nodes_generated, 1, "Tìm thấy bằng Simulated Annealing.")
        nodes_expanded += 1
        adj_options = generate_adjacent_states(curr)
        nodes_generated += len(adj_options)
        next_state, action_label, _ = random.choice(adj_options)
        delta_energy = h_func(next_state) - h_func(curr)
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temperature):
            curr = next_state
            current_path.append(curr)
            action_history.append(action_label)
        temperature *= cooling_rate
    return build_result_pack(curr == goal_state, current_path, action_history, nodes_expanded, nodes_generated, 1, "Tìm thấy." if curr == goal_state else "Dừng SA; có thể chưa đạt goal.")