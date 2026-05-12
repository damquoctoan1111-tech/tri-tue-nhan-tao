import random

N = 5

matrix = [[random.randint(0, 1) for j in range(N)] for i in range(N)]
checked = [[False] * N for i in range(N)]


def show():
    for hang in matrix:
        print(hang)
    print()


def directions(r, c):

    way = []

    if r + 1 < N:
        way.append("DOWN")

    if r - 1 >= 0:
        way.append("UP")

    if c + 1 < N:
        way.append("RIGHT")

    if c - 1 >= 0:
        way.append("LEFT")

    return way


def next_pos(r, c, step):

    if step == "DOWN":
        return r + 1, c

    if step == "UP":
        return r - 1, c

    if step == "RIGHT":
        return r, c + 1

    if step == "LEFT":
        return r, c - 1


def vacuum_agent():

    row = 0
    col = 0

    for i in range(35):

        print(f"Agent đang ở ô ({row},{col})")

        checked[row][col] = True

        if matrix[row][col] == 1:

            print("Phát hiện bụi -> DỌN")

            matrix[row][col] = 0

        else:

            print("Ô này sạch")

        show()

        done = True

        for x in matrix:

            if 1 in x:
                done = False

        if done:

            print("TOÀN BỘ PHÒNG ĐÃ SẠCH")

            break

        move_list = directions(row, col)

        flag = False

        for m in move_list:

            nr, nc = next_pos(row, col, m)

            if checked[nr][nc] != True:

                row, col = nr, nc

                flag = True

                break

        if flag == False:

            random_move = random.choice(move_list)

            row, col = next_pos(row, col, random_move)

        print("=======================")


print("TRẠNG THÁI LÚC ĐẦU")

show()

vacuum_agent()