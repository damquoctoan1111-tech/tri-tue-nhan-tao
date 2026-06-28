import random
from algorithms.core import (
    BoardState,
    benchmark_timer,
    generate_adjacent_states,
    build_result_pack,
    get_heuristic_function,
    MAX_NODE_LIMIT
)

@benchmark_timer
def simple_hill_climbing(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    curr = start_state
    current_path = [curr]
    action_history = []
    nodes_expanded = 0
    nodes_generated = 1
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    while nodes_expanded < node_limit:
        if curr == goal_state:
            return build_result_pack(True, current_path, action_history, nodes_expanded, nodes_generated, 1, "Tìm thấy lời giải bằng Hill Climbing.")
        nodes_expanded += 1
        adj_options = [(h_func(nxt), nxt, mv) for nxt, mv, _ in generate_adjacent_states(curr)]
        nodes_generated += len(adj_options)
        best_h = min(item[0] for item in adj_options)
        if best_h >= h_func(curr):
            return build_result_pack(False, current_path, action_history, nodes_expanded, nodes_generated, 1, "Bị kẹt tại cực trị cục bộ/vùng bằng phẳng.")
        candidates = [item for item in adj_options if item[0] == best_h]
        _, next_state, action_label = candidates[0]
        curr = next_state
        current_path.append(curr)
        action_history.append(action_label)
    return build_result_pack(False, current_path, action_history, nodes_expanded, nodes_generated, 1, "Vượt giới hạn nút tối đa.")