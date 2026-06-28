from algorithms.core import BoardState, benchmark_timer, generate_adjacent_states, get_heuristic_function
from algorithms.informed_search.astar import astar
from algorithms.adversarial_search.minimax import _evaluate_game_tree_step

@benchmark_timer
def alpha_beta_pruning(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', depth_limit=8, **kwargs):
    h_func = get_heuristic_function(heuristic, goal_state)
    decision, ext_nodes = _evaluate_game_tree_step(start_state, goal_state, h_func, min(depth_limit, 10), 'alphabeta')
    if not decision:
        return build_result_pack(False, expanded=ext_nodes, message='Không có nước đi.')
    search_summary = astar(decision[0], goal_state, heuristic=heuristic, **kwargs)
    
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
        search_summary.status_message = 'Alpha-Beta Pruning chọn nước đầu trong biến thể đối kháng, sau đó A* hoàn tất đường đi.'
    else:
        setattr(search_summary, 'message', 'Alpha-Beta Pruning chọn nước đầu trong biến thể đối kháng, sau đó A* hoàn tất đường đi.')
    return search_summary