from algorithms.core import (
    BoardState,
    benchmark_timer,
    generate_adjacent_states,
    trace_solution_path,
    build_result_pack,
    get_heuristic_function,
    MAX_NODE_LIMIT
)

@benchmark_timer
def and_or_graph_search(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', depth_limit=30, **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    parent_map = {start_state: (None, None)}
    nodes_expanded = 0
    nodes_generated = 1
    max_frontier_size = 1
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)

    def recursive_dfs(curr, depth, seen_states):
        nonlocal nodes_expanded, nodes_generated, max_frontier_size
        if curr == goal_state:
            return curr
        if depth <= 0 or nodes_expanded >= node_limit:
            return None
        nodes_expanded += 1
        sorted_options = sorted(generate_adjacent_states(curr), key=lambda x: h_func(x[0]))
        for next_state, action_label, _ in sorted_options:
            if next_state in seen_states:
                continue
            parent_map[next_state] = (curr, action_label)
            nodes_generated += 1
            max_frontier_size = max(max_frontier_size, len(seen_states) + 1)
            found_node = recursive_dfs(next_state, depth - 1, seen_states | {next_state})
            if found_node is not None:
                return found_node
        return None

    target_found = recursive_dfs(start_state, depth_limit, {start_state})
    if target_found:
        final_path, final_moves = trace_solution_path(parent_map, target_found)
        return build_result_pack(True, final_path, final_moves, nodes_expanded, nodes_generated, max_frontier_size, "Tìm thấy bằng AND-OR Graph Search.")
    return build_result_pack(False, expanded=nodes_expanded, generated=nodes_generated, max_frontier=max_frontier_size, message="AND-OR không tìm thấy trong giới hạn.")