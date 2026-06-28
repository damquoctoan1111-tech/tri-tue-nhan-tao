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

@benchmark_timer
def local_beam_search(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', beam_width=5, **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    beams = [(start_state, [start_state], [])] + [(generate_random_state(start_state, random.randint(5, 40)), [], []) for _ in range(max(0, beam_width - 1))]
    nodes_expanded = 0
    nodes_generated = len(beams)
    max_frontier_size = len(beams)
    seen_states = {start_state}
    node_limit = kwargs.get('max_nodes', MAX_NODE_LIMIT)
    while nodes_expanded < node_limit:
        candidates = []
        for current_state, current_path, action_history in beams:
            if current_state == goal_state:
                return build_result_pack(True, current_path or [current_state], action_history, nodes_expanded, nodes_generated, max_frontier_size, "Tìm thấy bằng Local Beam Search.")
            nodes_expanded += 1
            for next_state, action_label, _ in generate_adjacent_states(current_state):
                if next_state in seen_states:
                    continue
                seen_states.add(next_state)
                nodes_generated += 1
                candidates.append((h_func(next_state), next_state, (current_path or [current_state]) + [next_state], action_history + [action_label]))
        if not candidates:
            break
        candidates.sort(key=lambda x: x[0])
        beams = [(state, path, moves) for _, state, path, moves in candidates[:beam_width]]
        max_frontier_size = max(max_frontier_size, len(candidates))
    if beams:
        best_beam = min(beams, key=lambda x: h_func(x[0]))
        return build_result_pack(False, best_beam[1], best_beam[2], nodes_expanded, nodes_generated, max_frontier_size, "Không tìm thấy; trả về beam tốt nhất.")
    return build_result_pack(False, exp=nodes_expanded, gen=nodes_generated, max_f=max_frontier_size, msg="Không tìm thấy.")