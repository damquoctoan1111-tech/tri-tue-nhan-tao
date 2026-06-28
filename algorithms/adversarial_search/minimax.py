from algorithms.core import BoardState, benchmark_timer, generate_adjacent_states, get_heuristic_function
from algorithms.informed_search.astar import astar

def _evaluate_game_tree_step(start_n, target_n, h_eval, depth_n, search_mode='minimax'):
    expanded_counter = 0
    def compute_minimax_value(state, current_depth, is_max_turn, alpha=-10**9, beta=10**9):
        nonlocal expanded_counter
        expanded_counter += 1
        if state == target_n or current_depth == 0:
            return -h_eval(state)
        options = generate_adjacent_states(state)
        if search_mode == 'expectimax' and not is_max_turn:
            return sum(compute_minimax_value(n, current_depth - 1, True, alpha, beta) for n, _, _ in options) / len(options)
        if is_max_turn:
            max_val = -10**9
            for n, _, _ in options:
                max_val = max(max_val, compute_minimax_value(n, current_depth - 1, False, alpha, beta))
                alpha = max(alpha, max_val)
                if search_mode == 'alphabeta' and alpha >= beta:
                    break
            return max_val
        min_val = 10**9
        for n, _, _ in options:
            min_val = min(min_val, compute_minimax_value(n, current_depth - 1, True, alpha, beta))
            beta = min(beta, min_val)
            if search_mode == 'alphabeta' and alpha >= beta:
                break
        return min_val
    best_decision = None
    best_score = -10**9
    for adjacent, action, _ in generate_adjacent_states(start_n):
        score = compute_minimax_value(adjacent, max(0, depth_n - 1), False)
        if score > best_score:
            best_score = score
            best_decision = (adjacent, action)
    return best_decision, expanded_counter

@benchmark_timer
def minimax(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', depth_limit=8, **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    decision, ext_nodes = _evaluate_game_tree_step(start_state, goal_state, h_func, min(depth_limit, 10), 'minimax')
    if not decision:
        return build_result_pack(False, expanded=ext_nodes, message='Không có nước đi.')
    search_summary = astar(decision[0], goal_state, heuristic=heuristic, **kwargs)
    
    is_found = getattr(search_summary, 'is_found', getattr(search_summary, 'found', False))
    state_history = getattr(search_summary, 'state_history', getattr(search_summary, 'path', []))
    action_list = getattr(search_summary, 'action_list', getattr(search_summary, 'moves', []))
    
    if state_history:
        final_states = [start_state] + list(state_history)
        final_actions = [decision[1]] + list(action_list)
        if hasattr(search_summary, 'state_history'): search_summary.state_history = final_states
        if hasattr(search_summary, 'path'): search_summary.path = final_states
        if hasattr(search_summary, 'action_list'): search_summary.action_list = final_actions
        if hasattr(search_summary, 'moves'): search_summary.moves = final_actions
        if hasattr(search_summary, 'total_cost'): search_summary.total_cost = len(final_actions)
        if hasattr(search_summary, 'cost'): search_summary.cost = len(final_actions)
        
    if hasattr(search_summary, 'nodes_expanded'): search_summary.nodes_expanded += ext_nodes
    if hasattr(search_summary, 'expanded'): search_summary.expanded += ext_nodes
    
    if hasattr(search_summary, 'status_message'):
        search_summary.status_message = 'Minimax chọn nước đầu trong biến thể đối kháng, sau đó A* hoàn tất đường đi.'
    else:
        setattr(search_summary, 'message', 'Minimax chọn nước đầu trong biến thể đối kháng, sau đó A* hoàn tất đường đi.')
    return search_summary