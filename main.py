#!/usr/bin/python

import threading
from Pilights import Pilights
from Snake import Snake, Direction
import curses
from ConsolePlayer import *

if __name__ == '__main__':
    print "Starting test cycle!"

    console_player = ConsolePlayer()
    snake = Snake(11, 11, console_player)
    pilights = Pilights(11, 11, snake)

    def snake_loop():
        while True:
            snake.update()
            snake.sleep()

    snake_thread = threading.Thread(target=snake_loop)
    snake_thread.daemon = True
    snake_thread.start()

    console_player.block()