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
def ids(start_state: BoardState, goal_state: BoardState, depth_limit=35, **kwargs):
    if not check_solvability(start_state, goal_state):
        return build_result_pack(False, msg="Trạng thái bàn cờ không có lời giải.")
    total_expanded = 0
    total_generated = 0
    peak_stack_size = 0
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    for current_limit in range(depth_limit + 1):
        st = [(start_state, 0)]
        visited_records = {start_state: (None, None)}
        path_set = {start_state}
        current_expanded = 0
        current_generated = 1
        while st:
            peak_stack_size = max(peak_stack_size, len(st))
            if total_expanded + current_expanded > node_limit:
                return build_result_pack(False, exp=total_expanded + current_expanded, gen=total_generated + current_generated, max_f=peak_stack_size, msg="Vượt giới hạn nút tối đa.")
            curr_node, current_depth = st.pop()
            current_expanded += 1
            if curr_node == goal_state:
                final_path, final_moves = trace_solution_path(visited_records, goal_state)
                return build_result_pack(True, final_path, final_moves, total_expanded + current_expanded, total_generated + current_generated, peak_stack_size, f"Tìm thấy ở depth limit = {current_limit}.")
            if current_depth >= current_limit:
                continue
            for next_state, action_label, _ in reversed(generate_adjacent_states(curr_node)):
                if next_state in path_set:
                    continue
                path_set.add(next_state)
                visited_records[next_state] = (curr_node, action_label)
                current_generated += 1
                st.append((next_state, current_depth + 1))
        total_expanded += current_expanded
        total_generated += current_generated
    return build_result_pack(False, exp=total_expanded, gen=total_generated, max_f=peak_stack_size, msg="IDS không tìm thấy trong giới hạn.")