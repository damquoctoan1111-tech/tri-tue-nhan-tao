import random

SIZE = 5

floor = [[random.randint(0, 1) for i in range(SIZE)] for j in range(SIZE)]


def show_floor():

    for line in floor:

        print(line)

    print()


def available_direction(r, c):

    path = []

    if r + 1 < SIZE:
        path.append("DOWN")

    if r - 1 >= 0:
        path.append("UP")

    if c + 1 < SIZE:
        path.append("RIGHT")

    if c - 1 >= 0:
        path.append("LEFT")

    return path


def vacuum_robot():

    row = 0
    col = 0

    for turn in range(20):

        print(f"Robot đang đứng tại ({row},{col})")

        if floor[row][col] == 1:

            print("Phát hiện bụi -> ĐANG HÚT")

            floor[row][col] = 0

        else:

            print("Khu vực sạch")

        show_floor()

        choice_list = available_direction(row, col)

        picked = random.choice(choice_list)

        print("Robot di chuyển:", picked)

        print("====================")

        if picked == "DOWN":

            row += 1

        elif picked == "UP":

            row -= 1

        elif picked == "RIGHT":

            col += 1

        elif picked == "LEFT":

            col -= 1


print("TRẠNG THÁI KHỞI TẠO")

show_floor()

vacuum_robot()