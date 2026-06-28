from collections import deque
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
def bfs(start_state: BoardState, goal_state: BoardState, **kwargs):
    if not check_solvability(start_state, goal_state):
        return build_result_pack(False, msg="Trạng thái bàn cờ không có lời giải.")
        
    if start_state == goal_state:
        return build_result_pack(True, path=[start_state], moves=[], msg="Trạng thái bắt đầu trùng đích.")

    pending_queue = deque([start_state])
    visited_records = {start_state: (None, None)}
    
    nodes_expanded = 0
    nodes_generated = 1
    max_queue_size = 1
    
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)

    while pending_queue:
        max_queue_size = max(max_queue_size, len(pending_queue))
        curr_node = pending_queue.popleft()
        nodes_expanded += 1

        if nodes_expanded > node_limit:
            return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_queue_size, msg="Vượt giới hạn nút tối đa.")

        for next_state, action_label, _ in generate_adjacent_states(curr_node):
            if next_state not in visited_records:
                visited_records[next_state] = (curr_node, action_label)
                nodes_generated += 1

                if next_state == goal_state:
                    final_path, final_moves = trace_solution_path(visited_records, goal_state)
                    return build_result_pack(
                        True, 
                        path=final_path, 
                        moves=final_moves, 
                        exp=nodes_expanded, 
                        gen=nodes_generated, 
                        max_f=max_queue_size, 
                        msg="Tìm kiếm thành công!"
                    )
                
                pending_queue.append(next_state)

    return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_queue_size, msg="Không tìm thấy đường đi.")