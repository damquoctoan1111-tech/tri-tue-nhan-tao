import random
from algorithms.core import (
    BoardState,
    benchmark_timer,
    generate_adjacent_states,
    generate_random_state,
    build_result_pack,
    get_heuristic_function,
    MAX_NODE_LIMIT
)

def _execute_inner_hc(start_node, target_node, h_evaluation, limit_n):
    curr = start_node
    path_trace = [curr]
    move_trace = []
    exp_c = 0
    gen_c = 1
    while exp_c < limit_n:
        if curr == target_node:
            return True, path_trace, move_trace, exp_c, gen_c
        exp_c += 1
        options = [(h_evaluation(n), n, mv) for n, mv, _ in generate_adjacent_states(curr)]
        gen_c += len(options)
        best_val = min(x[0] for x in options)
        if best_val >= h_evaluation(curr):
            return False, path_trace, move_trace, exp_c, gen_c
        candidates = [x for x in options if x[0] == best_val]
        _, nxt, mv = random.choice(candidates)
        curr = nxt
        path_trace.append(curr)
        move_trace.append(mv)
    return False, path_trace, move_trace, exp_c, gen_c

@benchmark_timer
def random_restart_hill_climbing(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', restarts=20, **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    total_expanded = 0
    total_generated = 0
    best_path = []
    best_moves = []
    best_h_score = 10**9
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    seeds = [start_state] + [generate_random_state(start_state, random.randint(10, 60)) for _ in range(max(0, restarts - 1))]
    for seed in seeds:
        allocated_nodes = max(1, (node_limit - total_expanded) // max(1, len(seeds)))
        success, p_trace, m_trace, e_cnt, g_cnt = _execute_inner_hc(seed, goal_state, h_func, allocated_nodes)
        total_expanded += e_cnt
        total_generated += g_cnt
        if p_trace and h_func(p_trace[-1]) < best_h_score:
            best_h_score = h_func(p_trace[-1])
            best_path = p_trace
            best_moves = m_trace
        if success:
            return build_result_pack(True, p_trace, m_trace, total_expanded, total_generated, 1, "Tìm thấy bằng Random Restart Hill Climbing.")
        if total_expanded >= node_limit:
            break
    return build_result_pack(False, best_path, best_moves, total_expanded, total_generated, 1, "Không tìm thấy sau các lần restart; trả về đường đi tốt nhất.")