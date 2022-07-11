import os
import time
from random import randint
from threading import Thread

import keyboard

KEYS = ["Down", "Up", "Left", "Right"]

WIDTH = 70
HEIGHT = 50
ME = "🐼"
pos_x, pos_y = randint(0, WIDTH - 5), randint(0, HEIGHT - 5)

SCENE = [[" " for y in range(HEIGHT)] for x in range(WIDTH)]
SCENE[pos_x][pos_y] = ME

SCORE = 0

BALL = "🥚"
ball_x, ball_y = randint(0, WIDTH - 5), randint(0, HEIGHT - 5)

ENV_GENERATED = False

PNJS = ["🐄", "🐑", "🦆", "🐓", "🐃", "🐂", "🦏", "🐎", "🐖", "🦍", "🐆"]
TREES = ["🌲", "🌳"]

SHOULD_REND = True


def is_in_the_with(x):
    return WIDTH > x >= 0


def is_in_the_height(y):
    return HEIGHT > y >= 0


def map_it(elt, x, y):
    global SHOULD_REND

    if is_in_the_height(y) and is_in_the_with(x):
        SCENE[x][y] = elt
        SHOULD_REND = True


def clean_it(x, y):
    global SHOULD_REND

    if is_in_the_height(y) and is_in_the_with(x):
        SCENE[x][y] = " "
        SHOULD_REND = True


def map_it_and_clean(elt, x0, y0, x1, y1):
    clean_it(x0, y0)
    map_it(elt, x1, y1)


def map_it_randomly(elt):
    map_it(elt, randint(0, WIDTH - 1), randint(0, HEIGHT - 1))


def generate_trees():
    global ENV_GENERATED, TREES

    for tree in TREES:
        # we can build some forest here
        x, y = randint(0, WIDTH - 1), randint(0, HEIGHT - 1)

        map_it(tree, x, y)
        map_it(tree, x + randint(1, 3), y)
        map_it(tree, x, y + randint(1, 3))

        map_it(tree, abs(x - randint(1, 3)), y)
        map_it(tree, x, abs(y - randint(1, 3)))


def generate_env():
    global ENV_GENERATED

    if not ENV_GENERATED:
        for i in range(randint(1, 20)):
            generate_trees()

        for i in range(randint(2, 10)):
            map_it_randomly("🪨")

        for i in range(randint(5, 50)):
            map_it_randomly(PNJS[randint(0, len(PNJS) - 1)])

        ENV_GENERATED = True


def make_ball():
    global ball_x, ball_y, BALL, SCORE

    if ball_x == pos_x and ball_y == pos_y:
        SCORE += 1
        ball_x, ball_y = randint(0, WIDTH - 5), randint(0, HEIGHT - 5)

    map_it(BALL, ball_x, ball_y)


def move_left():
    global SCENE, WIDTH, pos_x, pos_y

    if is_in_the_with(pos_x - 1):
        map_it_and_clean(ME, pos_x, pos_y, pos_x - 1, pos_y)
        pos_x -= 1


def move_right():
    global SCENE, WIDTH, pos_x, pos_y

    if is_in_the_with(pos_x + 1):
        map_it_and_clean(ME, pos_x, pos_y, pos_x + 1, pos_y)
        pos_x += 1


def move_up():
    global SCENE, HEIGHT, pos_x, pos_y

    if is_in_the_height(pos_y - 1):
        map_it_and_clean(ME, pos_x, pos_y, pos_x, pos_y - 1)
        pos_y -= 1


def move_down():
    global SCENE, HEIGHT, pos_x, pos_y

    if is_in_the_height(pos_y + 1):
        map_it_and_clean(ME, pos_x, pos_y, pos_x, pos_y + 1)
        pos_y += 1


def clearConsole():
    # We need to clean the screen when there is a change on it
    command = "clear"
    # If Machine is running on Windows, use cls
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


# def move_pnjs():
#     global SCENE

#     while True:
#         for j in range(0, HEIGHT - 1):
#             for i in range(0, WIDTH - 1):
#                 if SCENE[i][i] in PNJS:
#                     randd = randint(1, 100)
#                     if randd % 2 == 0:
#                         map_it_and_clean(SCENE[i][j], i, j, i + 1, j)
#                     elif randd % 3 == 0 or randd % 5 == 0:
#                         map_it_and_clean(SCENE[i][j], i, j, i - 1, j)
#                     time.sleep(1)

#         time.sleep(0.5)


def refresh_scene():
    global SCENE, SHOULD_REND

    while True:
        if SHOULD_REND:
            clearConsole()

            rend_this = ""
            for j in range(0, HEIGHT - 1):
                for i in range(0, WIDTH - 1):
                    rend_this += SCENE[i][j] + " "
                rend_this += "\n"

            rend_this += f"{pos_x}/{pos_y} => score : {SCORE}\n"
            rend_this += "_" * 100

            print(rend_this)
            SHOULD_REND = False

        time.sleep(0.05)


def render(key):
    global KEYS, SCENE, SCORE

    while True:
        make_ball()

        keyboard.wait(key)

        if key == "Left":
            move_left()

        if key == "Right":
            move_right()

        if key == "Down":
            move_down()

        if key == "Up":
            move_up()


if __name__ == "__main__":
    generate_env()

    thread_scene = Thread(target=refresh_scene)
    thread_scene.start()

    # thread_pnj = Thread(target=move_pnjs)
    # thread_pnj.start()

    threads = [Thread(target=render, kwargs={"key": key}) for key in KEYS]

    for thread in threads:
        thread.start()
