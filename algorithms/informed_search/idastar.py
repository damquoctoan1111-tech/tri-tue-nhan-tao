import math
from algorithms.core import (
    BoardState,
    benchmark_timer,
    check_solvability,
    generate_adjacent_states,
    build_result_pack,
    get_heuristic_function,
    MAX_NODE_LIMIT
)

@benchmark_timer
def idastar(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    if not check_solvability(start_state, goal_state):
        return build_result_pack(False, msg="Trạng thái bàn cờ không có lời giải.")
    h_func = get_heuristic_function(heuristic, goal_state)
    current_bound = h_func(start_state)
    current_path = [start_state]
    action_history = []
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)

    def recursive_search(g_cost, bound, active_set):
        nonlocal nodes_expanded, nodes_generated, max_frontier_size
        curr_node = current_path[-1]
        f_cost = g_cost + h_func(curr_node)
        if f_cost > bound:
            return f_cost
        if curr_node == goal_state:
            return 'FOUND'
        nodes_expanded += 1
        if nodes_expanded > node_limit:
            return math.inf
        minimum_bound = math.inf
        for next_state, action_label, edge_cost in generate_adjacent_states(curr_node):
            if next_state in active_set:
                continue
            current_path.append(next_state)
            action_history.append(action_label)
            active_set.add(next_state)
            nodes_generated += 1
            max_frontier_size = max(max_frontier_size, len(current_path))
            search_status = recursive_search(g_cost + edge_cost, bound, active_set)
            if search_status == 'FOUND':
                return 'FOUND'
            minimum_bound = min(minimum_bound, search_status)
            active_set.remove(next_state)
            current_path.pop()
            action_history.pop()
        return minimum_bound

    while True:
        search_status = recursive_search(0, current_bound, {start_state})
        if search_status == 'FOUND':
            return build_result_pack(True, current_path.copy(), action_history.copy(), nodes_expanded, nodes_generated, max_frontier_size, "Tìm thấy lời giải bằng IDA*.")
        if search_status == math.inf or nodes_expanded > node_limit:
            return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_frontier_size, msg="Không tìm thấy hoặc vượt giới hạn node.")
        current_bound = search_status