from algorithms.core import BoardState, benchmark_timer, generate_adjacent_states
from algorithms.informed_search.astar import astar

@benchmark_timer
def belief_no_observation(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    belief_set = {start_state}
    for adjacent, _, _ in generate_adjacent_states(start_state):
        belief_set.add(adjacent)
    search_summary = astar(start_state, goal_state, heuristic=heuristic, **kwargs)
    if hasattr(search_summary, 'status_message'):
        search_summary.status_message = 'Belief State Search (No observation): dùng tập belief quanh start, giải theo trạng thái đại diện.'
    else:
        setattr(search_summary, 'message', 'Belief State Search (No observation): dùng tập belief quanh start, giải theo trạng thái đại diện.')
    return search_summary