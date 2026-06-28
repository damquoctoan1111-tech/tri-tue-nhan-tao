from algorithms.core import BoardState, benchmark_timer, check_solvability, build_result_pack
from algorithms.informed_search.astar import astar

@benchmark_timer
def ac3_search(start_state: BoardState, goal_state: BoardState, heuristic='Manhattan', **kwargs):
    if not check_solvability(start_state, goal_state):
        return build_result_pack(False, message='AC-3 phát hiện trạng thái không giải được.')
    search_summary = astar(start_state, goal_state, heuristic=heuristic, **kwargs)
    if hasattr(search_summary, 'status_message'):
        search_summary.status_message = 'AC-3 Search: kiểm tra nhất quán/tính giải được rồi chạy A*.'
    else:
        setattr(search_summary, 'message', 'AC-3 Search: kiểm tra nhất quán/tính giải được rồi chạy A*.')
    return search_summary