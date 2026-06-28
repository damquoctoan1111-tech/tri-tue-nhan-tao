from algorithms.core import (
    BoardState,
    benchmark_timer,
    check_solvability,
    generate_adjacent_states,
    trace_solution_path,
    build_result_pack,
    MAX_NODE_LIMIT
)

@benchmark_timer
def dfs(start_state: BoardState, goal_state: BoardState, depth_limit=35, **kwargs):
    if not check_solvability(start_state, goal_state):
        return build_result_pack(False, msg="Trạng thái bàn cờ không có lời giải.")
    st = [(start_state, 0)]
    visited_records = {start_state: (None, None)}
    best_depth = {start_state: 0}
    nodes_expanded = 0
    nodes_generated = 1
    max_stack_size = 1
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    while st:
        max_stack_size = max(max_stack_size, len(st))
        curr_node, current_depth = st.pop()
        nodes_expanded += 1
        if curr_node == goal_state:
            final_path, final_moves = trace_solution_path(visited_records, goal_state)
            return build_result_pack(True, final_path, final_moves, nodes_expanded, nodes_generated, max_stack_size, "Tìm thấy lời giải bằng DFS.")
        if nodes_expanded > node_limit:
            return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_stack_size, msg="Vượt giới hạn nút tối đa.")
        if current_depth >= depth_limit:
            continue
        for next_state, action_label, _ in reversed(generate_adjacent_states(curr_node)):
            if next_state not in best_depth or current_depth + 1 < best_depth[next_state]:
                best_depth[next_state] = current_depth + 1
                visited_records[next_state] = (curr_node, action_label)
                nodes_generated += 1
                st.append((next_state, current_depth + 1))
    return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_stack_size, msg="DFS không tìm thấy trong giới hạn độ sâu.")