from algorithms.core import (
    BoardState,
    benchmark_timer,
    generate_adjacent_states,
    trace_solution_path,
    build_result_pack,
    MAX_NODE_LIMIT
)

@benchmark_timer
def backtracking_search(start_state: BoardState, goal_state: BoardState, depth_limit=35, **kwargs):
    parent_map = {start_state: (None, None)}
    nodes_expanded = 0
    nodes_generated = 1
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)

    def execute_backtrack(curr, depth, seen_states):
        nonlocal nodes_expanded, nodes_generated
        if curr == goal_state:
            return curr
        if depth <= 0 or nodes_expanded >= node_limit:
            return None
        nodes_expanded += 1
        for next_state, action_label, _ in generate_adjacent_states(curr):
            if next_state in seen_states:
                continue
            parent_map[next_state] = (curr, action_label)
            nodes_generated += 1
            found_node = execute_backtrack(next_state, depth - 1, seen_states | {next_state})
            if found_node:
                return found_node
        return None

    target_found = execute_backtrack(start_state, depth_limit, {start_state})
    if target_found:
        final_path, final_moves = trace_solution_path(parent_map, target_found)
        return build_result_pack(True, final_path, final_moves, nodes_expanded, nodes_generated, depth_limit, "Tìm thấy bằng CSP Backtracking.")
    return build_result_pack(False, expanded=nodes_expanded, generated=nodes_generated, max_frontier=depth_limit, message="Backtracking không tìm thấy trong giới hạn.")