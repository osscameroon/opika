import keyboard
from os import system
from threading import Thread
import time
from random import randint


KEYS = ['Down', 'Up', 'Left', 'Right']

WIDTH = 50
HEIGHT = 30
ME = '🐼'

SCENE = [[' ' for y in range(HEIGHT)] for x in range(WIDTH)]

pos_x, pos_y = 10, 20

ball_x, ball_y = randint(0, WIDTH - 5), randint(0, HEIGHT - 5)
BALL = '🥚'

SCENE[pos_x][pos_y] = ME
SCORE = 0

ENV_GENERATED = False

max_time = 100


def map_it(elt, x, y):
    SCENE[x][y] = elt


def clean_it(x, y):
    SCENE[x][y] = ' '


def generate_env():
    global ENV_GENERATED

    if not ENV_GENERATED:
        for i in range(randint(1, 10)):
            map_it('🌲', randint(0, WIDTH - 5), randint(0, HEIGHT - 5))
            map_it('🌳', randint(0, WIDTH - 5), randint(0, HEIGHT - 5))
            map_it('🪨', randint(0, WIDTH - 5), randint(0, HEIGHT - 5))
            map_it('🐑', randint(0, WIDTH - 5), randint(0, HEIGHT - 5))

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
        clean_it(pos_x, pos_y)
        map_it(ME, pos_x - 1, pos_y)

        pos_x -= 1


def move_right():
    global SCENE, WIDTH, pos_x, pos_y

    if WIDTH > pos_x + 1 >= 0:
        clean_it(pos_x, pos_y)
        map_it(ME, pos_x + 1, pos_y)

        pos_x += 1


def move_up():
    global SCENE, HEIGHT, pos_x, pos_y

    if HEIGHT > pos_y - 1 >= 0:
        clean_it(pos_x, pos_y)
        map_it(ME, pos_x, pos_y - 1)

        pos_y -= 1


def move_down():
    global SCENE, HEIGHT, pos_x, pos_y

    if HEIGHT > pos_y + 1 >= 0:
        clean_it(pos_x, pos_y)
        map_it(ME, pos_x, pos_y + 1)

        pos_y += 1


def render(key):
    global KEYS, SCENE, SCORE, max_time

    while True:
        generate_env()

        for j in range(0, HEIGHT - 1):
            for i in range(0, WIDTH - 1):
                print(SCENE[i][j], end=' ')
            print('\n')

        make_ball()

        print(f"{pos_x}/{pos_y} => score : {SCORE} | {max_time}")
        print("______________________________________________")

        keyboard.wait(key)

        if key == 'Left':
            move_left()

        if key == 'Right':
            move_right()

        if key == 'Down':
            move_down()

        if key == 'Up':
            move_up()

        system('clear')


def timer_decr():
    global max_time

    while max_time > 0:
        time.sleep(1)
        max_time -= 1


thread_time = Thread(target=timer_decr)
thread_time.start()

threads = [Thread(target=render, kwargs={'key': key}) for key in KEYS]

for thread in threads:
    thread.start()
