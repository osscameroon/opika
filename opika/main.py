import time
from os import system
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

max_time = 100


def map_it(elt, x, y):
    SCENE[x][y] = elt


def clean_it(x, y):
    SCENE[x][y] = " "


def map_it_and_clean(elt, x0, y0, x1, y1):
    clean_it(x0, y0)
    map_it(elt, x1, y1)


def map_it_randomly(elt):
    map_it(elt, randint(0, WIDTH - 1), randint(0, HEIGHT - 1))


def generate_env():
    global ENV_GENERATED

    if not ENV_GENERATED:
        for i in range(randint(5, 20)):
            map_it_randomly("🌲")
            map_it_randomly("🌳")

        for i in range(randint(2, 10)):
            map_it_randomly("🪨")

        for i in range(randint(5, 30)):
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

    if WIDTH > pos_x - 1 >= 0:
        map_it_and_clean(ME, pos_x, pos_y, pos_x - 1, pos_y)

        pos_x -= 1


def move_right():
    global SCENE, WIDTH, pos_x, pos_y

    if WIDTH > pos_x + 1 >= 0:
        map_it_and_clean(ME, pos_x, pos_y, pos_x + 1, pos_y)

        pos_x += 1


def move_up():
    global SCENE, HEIGHT, pos_x, pos_y

    if HEIGHT > pos_y - 1 >= 0:
        map_it_and_clean(ME, pos_x, pos_y, pos_x, pos_y - 1)

        pos_y -= 1


def move_down():
    global SCENE, HEIGHT, pos_x, pos_y

    if HEIGHT > pos_y + 1 >= 0:
        map_it_and_clean(ME, pos_x, pos_y, pos_x, pos_y + 1)

        pos_y += 1


def move_pnjs(x, y):
    global SCENE

    while True:
        for j in range(0, HEIGHT - 1):
            for i in range(0, WIDTH - 1):
                if SCENE[i][i] in PNJS:
                    randd = randint(1, 100)
                    if randd % 2 == 0:
                        map_it_and_clean(SCENE[i][j], i, j, i + 1, j)
                    elif randd % 3 == 0 or randd % 5 == 0:
                        map_it_and_clean(SCENE[i][j], i, j, i - 1, j)
                    time.sleep(1)

        time.sleep(0.3)


def refresh_scene():
    global SCENE, max_time

    while True:
        rend_this = ""
        for j in range(0, HEIGHT - 1):
            for i in range(0, WIDTH - 1):
                rend_this += SCENE[i][j] + ' '
            rend_this += '\n'

        print(rend_this)
        print(f'{pos_x}/{pos_y} => score : {SCORE} | {max_time}s')
        print('_' * 100)
        time.sleep(0.033)

        system('clear')


def render(key):
    global KEYS, SCENE, SCORE, max_time

    while True:
        make_ball()

        keyboard.wait(key)

        if key == 'Left':
            move_left()

        if key == 'Right':
            move_right()

        if key == 'Down':
            move_down()

        if key == 'Up':
            move_up()


def timer_decr():
    global max_time

    while max_time > 0:
        time.sleep(1)
        max_time -= 1


if __name__ == "__main__":
    generate_env()

    thread_scene = Thread(target=refresh_scene)
    thread_scene.start()

    thread_pnjs = Thread(target=move_pnjs)
    thread_pnjs.start()

    thread_time = Thread(target=timer_decr)
    thread_time.start()

    threads = [Thread(target=render, kwargs={'key': key}) for key in KEYS]

    for thread in threads:
        thread.start()
