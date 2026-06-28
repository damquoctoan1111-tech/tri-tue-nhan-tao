import heapq
from algorithms.core import (
    BoardState,
    benchmark_timer,
    check_solvability,
    generate_adjacent_states,
    trace_solution_path,
    build_result_pack,
    get_heuristic_function,
    MAX_NODE_LIMIT
)

@benchmark_timer
def astar(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    if not check_solvability(start_state, goal_state):
        return build_result_pack(False, msg="Trạng thái bàn cờ không có lời giải.")
    h_func = get_heuristic_function(heuristic, goal_state)
    pq = [(h_func(start_state), 0, 0, start_state)]
    visited_records = {start_state: (None, None)}
    best_g_costs = {start_state: 0}
    closed_set = set()
    nodes_generated = 1
    nodes_expanded = 0
    max_queue_size = 1
    push_counter = 0
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    while pq:
        max_queue_size = max(max_queue_size, len(pq))
        current_f, current_g, _, curr_node = heapq.heappop(pq)
        if curr_node in closed_set:
            continue
        closed_set.add(curr_node)
        nodes_expanded += 1
        if curr_node == goal_state:
            final_path, final_moves = trace_solution_path(visited_records, goal_state)
            return build_result_pack(True, final_path, final_moves, nodes_expanded, nodes_generated, max_queue_size, "Tìm thấy lời giải tối ưu bằng A*.")
        if nodes_expanded > node_limit:
            return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_queue_size, msg="Vượt giới hạn nút tối đa.")
        for next_state, action_label, edge_cost in generate_adjacent_states(curr_node):
            next_g = current_g + edge_cost
            if next_state not in best_g_costs or next_g < best_g_costs[next_state]:
                best_g_costs[next_state] = next_g
                visited_records[next_state] = (curr_node, action_label)
                push_counter += 1
                nodes_generated += 1
                next_f = next_g + h_func(next_state)
                heapq.heappush(pq, (next_f, next_g, push_counter, next_state))
    return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_queue_size, msg="Không tìm thấy lời giải.")