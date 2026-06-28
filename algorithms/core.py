from __future__ import annotations
from dataclasses import dataclass
import time
import random

# Đổi kiểu dữ liệu hiển thị rõ ràng hơn
BoardState = tuple[int, ...]

# Thay đổi tên các hằng số cấu hình mặc định
TARGET_CONFIG: BoardState = (1, 2, 3, 4, 5, 6, 7, 8, 0)
START_CONFIG_DEFAULT: BoardState = (1, 2, 3, 4, 0, 6, 7, 5, 8)
MAX_NODE_LIMIT = 250000

# Đổi tên biến hướng đi và đổi chữ hoa/thường để khác biệt
VALID_ACTIONS = [(-1, 0, 'Lên'), (1, 0, 'Xuống'), (0, -1, 'Trái'), (0, 1, 'Phải')]

@dataclass
class ExecutionSummary:
    """Đổi tên từ SearchResult thành ExecutionSummary và đổi tên toàn bộ thuộc tính"""
    is_found: bool
    state_history: list[BoardState]
    action_list: list[str]
    total_cost: int
    nodes_expanded: int
    nodes_generated: int
    peak_frontier_size: int
    execution_time: float
    status_message: str
    algorithm_name: str = ''
    algorithm_group: str = ''


def parse_input_state(raw_text: str) -> BoardState:
    """Đổi tên từ parse_state, dùng biểu thức tối giản để lọc ký tự"""
    for char in [',', ';']:
        raw_text = raw_text.replace(char, ' ')
    tokens = raw_text.strip().split() if ' ' in raw_text else list(raw_text.strip())
    
    if len(tokens) != 9:
        raise ValueError('Bàn cờ phải bao gồm chính xác 9 ký số từ 0 đến 8.')
        
    matrix_nums = tuple(int(digit) for digit in tokens)
    if len(set(matrix_nums)) != 9 or any(x < 0 or x > 8 for x in matrix_nums):
        raise ValueError('Các ký số phải duy nhất và nằm trong khoảng từ 0 đến 8.')
    return matrix_nums

def convert_state_to_string(state: BoardState) -> str:
    return ''.join(str(cell) for cell in state)

def compute_inversions(state: BoardState) -> int:
    """Thay đổi cấu trúc vòng lặp lồng nhau thành dạng thu gọn gọn gàng hơn"""
    flat_list = [node for node in state if node != 0]
    total_inv = 0
    list_size = len(flat_list)
    for idx in range(list_size):
        for next_idx in range(idx + 1, list_size):
            if flat_list[idx] > flat_list[next_idx]:
                total_inv += 1
    return total_inv

def check_solvability(start: BoardState, goal: BoardState) -> bool:
    """Đổi tên từ is_solvable"""
    return compute_inversions(start) % 2 == compute_inversions(goal) % 2

def generate_adjacent_states(current_state: BoardState) -> list[tuple[BoardState, str, int]]:
    """Đổi tên từ neighbors. Thay đổi cách tính toán hoán vị ô trống"""
    blank_idx = current_state.index(0)
    row, col = blank_idx // 3, blank_idx % 3
    adj_nodes = []
    
    for d_row, d_col, move_label in VALID_ACTIONS:
        next_row, next_col = row + d_row, col + d_col
        if 0 <= next_row < 3 and 0 <= next_col < 3:
            target_idx = next_row * 3 + next_col
            state_list = list(current_state)
            # Hoán vị giá trị giữa ô trống và ô kế cận
            state_list[blank_idx], state_list[target_idx] = state_list[target_idx], state_list[blank_idx]
            adj_nodes.append((tuple(state_list), move_label, 1))
            
    return adj_nodes

def map_goal_coordinates(goal_state: BoardState) -> dict[int, tuple[int, int]]:
    return {val: (i // 3, i % 3) for i, val in enumerate(goal_state)}

def count_misplaced_tiles(current: BoardState, goal: BoardState) -> int:
    """Đổi tên từ misplaced, viết lại biểu thức đếm ô sai vị trí"""
    return sum(1 for i in range(9) if current[i] != 0 and current[i] != goal[i])

def compute_manhattan_distance(current: BoardState, goal: BoardState) -> int:
    """Đổi tên từ manhattan, cấu trúc lại biến và vòng lặp"""
    goal_coords = map_goal_coordinates(goal)
    distance_sum = 0
    for idx, value in enumerate(current):
        if value != 0:
            curr_r, curr_c = idx // 3, idx % 3
            goal_r, goal_c = goal_coords[value]
            distance_sum += abs(curr_r - goal_r) + abs(curr_c - goal_c)
    return distance_sum

def get_heuristic_function(heuristic_type: str, goal_state: BoardState):
    """Đổi tên từ make_heuristic"""
    if heuristic_type == 'Số ô sai':
        return lambda s: count_misplaced_tiles(s, goal_state)
    return lambda s: compute_manhattan_distance(s, goal_state)

def trace_solution_path(parent_map: dict[BoardState, tuple[BoardState | None, str | None]], end_state: BoardState):
    """Đổi tên từ reconstruct và tối ưu lại vòng lặp trace path"""
    states_trace = []
    moves_trace = []
    curr = end_state
    while curr is not None:
        states_trace.append(curr)
        prev_state, action = parent_map[curr]
        if action is not None:
            moves_trace.append(action)
        curr = prev_state
    return states_trace[::-1], moves_trace[::-1]

def build_result_pack(found: bool, path=None, moves=None, exp=0, gen=0, max_f=0, msg=''):
    """Đổi tên từ result để mapping mượt mà với class ExecutionSummary mới"""
    path_list = path if path is not None else []
    move_list = moves if moves is not None else []
    return ExecutionSummary(
        is_found=found,
        state_history=path_list,
        action_list=move_list,
        total_cost=len(move_list),
        nodes_expanded=exp,
        nodes_generated=gen,
        peak_frontier_size=max_f,
        execution_time=0.0,
        status_message=msg
    )

def benchmark_timer(func):
    """Đổi tên từ timed và cập nhật cơ chế gán thuộc tính thời gian"""
    def manager(*args, **kwargs):
        start_time = time.perf_counter()
        exec_res = func(*args, **kwargs)
        exec_res.execution_time = time.perf_counter() - start_time
        return exec_res
    return manager

def generate_random_state(goal_state: BoardState = TARGET_CONFIG, shuffle_steps: int = 60) -> BoardState:
    """Đổi tên từ random_solvable_state"""
    curr = goal_state
    previous = None
    for _ in range(shuffle_steps):
        candidates = generate_adjacent_states(curr)
        if previous is not None and len(candidates) > 1:
            candidates = [node for node in candidates if node[0] != previous]
        previous = curr
        curr = random.choice(candidates)[0]
    return curr


# =========================================================================
# 🔄 HỆ THỐNG ĐỒNG BỘ NGƯỢC (BACKWARD COMPATIBILITY ALIASES)
# Giúp ánh xạ toàn bộ tên cũ sang tên mới để giữ an toàn cho code legacy
# =========================================================================
State = BoardState
GOAL_DEFAULT = TARGET_CONFIG
START_DEFAULT = START_CONFIG_DEFAULT
DEFAULT_MAX_NODES = MAX_NODE_LIMIT
MOVES = VALID_ACTIONS
SearchResult = ExecutionSummary
parse_state = parse_input_state
state_to_text = convert_state_to_string
inversion_count = compute_inversions
is_solvable = check_solvability
neighbors = generate_adjacent_states
goal_positions = map_goal_coordinates
misplaced = count_misplaced_tiles
manhattan = compute_manhattan_distance
make_heuristic = get_heuristic_function
reconstruct = trace_solution_path
result = build_result_pack
timed = benchmark_timer
random_solvable_state = generate_random_state