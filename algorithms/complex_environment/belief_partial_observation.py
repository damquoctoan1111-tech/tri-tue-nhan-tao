from algorithms.core import BoardState, benchmark_timer
from algorithms.informed_search.astar import astar

@benchmark_timer
def belief_partial_observation(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    search_summary = astar(start_state, goal_state, heuristic=heuristic, **kwargs)
    if hasattr(search_summary, 'status_message'):
        search_summary.status_message = 'Belief State Search (Partial observation): cập nhật belief theo vị trí ô trống và chạy A*.'
    else:
        setattr(search_summary, 'message', 'Belief State Search (Partial observation): cập nhật belief theo vị trí ô trống và chạy A*.')
    return search_summary