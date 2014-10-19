#!/usr/bin/python

import threading
from Pilights import Pilights
from Snake import Snake, Direction
import curses

if __name__ == '__main__':
    print "Starting test cycle!"
    snake = Snake(11, 11)
    pilights = Pilights(11, 11, snake)

    def snake_loop():
        while True:
            snake.update()
            snake.sleep()

    snake_thread = threading.Thread(target=snake_loop)
    snake_thread.daemon = True
    snake_thread.start()

    def main_loop(screen):
        win = curses.newwin(20, 60, 0, 0)
        win.keypad(1)
        curses.noecho()
        curses.cbreak()

        while True:
            c = win.getch()
            if c == curses.KEY_UP:
                snake.change_direction(Direction.up)
            elif c == curses.KEY_DOWN:
                snake.change_direction(Direction.down)
            elif c == curses.KEY_LEFT:
                snake.change_direction(Direction.left)
            elif c == curses.KEY_RIGHT:
                snake.change_direction(Direction.right)
            elif c == 10:
                snake.start()

    curses.wrapper(main_loop)