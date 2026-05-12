import random
import time

TARGET = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]


class PuzzleAgent:

    def __init__(self):

        self.board = None
        self.choice = None

    def save_state(self, data):

        self.board = data

        return self.board

    def locate_zero(self, board):

        for r in range(3):

            for c in range(3):

                if board[r][c] == 0:

                    return r, c

    def is_goal(self, board):

        return board == TARGET

    def available_moves(self, board):

        r, c = self.locate_zero(board)

        result = []

        if r != 0:
            result.append("GO_UP")

        if r != 2:
            result.append("GO_DOWN")

        if c != 0:
            result.append("GO_LEFT")

        if c != 2:
            result.append("GO_RIGHT")

        return result

    def choose_action(self, board):

        move_set = self.available_moves(board)

        selected = random.choice(move_set)

        return selected

    def swap(self, board, step):

        r, c = self.locate_zero(board)

        copied = [line[:] for line in board]

        if step == "GO_UP":

            copied[r][c], copied[r - 1][c] = (
                copied[r - 1][c],
                copied[r][c]
            )

        elif step == "GO_DOWN":

            copied[r][c], copied[r + 1][c] = (
                copied[r + 1][c],
                copied[r][c]
            )

        elif step == "GO_LEFT":

            copied[r][c], copied[r][c - 1] = (
                copied[r][c - 1],
                copied[r][c]
            )

        elif step == "GO_RIGHT":

            copied[r][c], copied[r][c + 1] = (
                copied[r][c + 1],
                copied[r][c]
            )

        return copied

    def run(self, percept):

        current = self.save_state(percept)

        action = self.choose_action(current)

        self.choice = action

        return action


def display(board):

    for item in board:

        print(item)

    print()


start = [
    [1, 2, 3],
    [0, 4, 6],
    [7, 5, 8]
]


robot = PuzzleAgent()

state_now = start

count = 0

print("========= BEGIN =========\n")

while True:

    print("LẦN:", count)

    print("Bàn hiện tại:")

    display(state_now)

    if robot.is_goal(state_now):

        print("HOÀN THÀNH TRẠNG THÁI ĐÍCH")

        break

    act = robot.run(state_now)

    print("Agent chọn:", act)

    state_now = robot.swap(state_now, act)

    count += 1

    time.sleep(1)

    if count >= 30:

        print("KẾT THÚC SAU 30 LẦN")

        break

print("\n========= FINISH =========")