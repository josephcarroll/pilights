import curses
from Snake import Direction


class ConsolePlayer:
    def __init__(self):
        self.last_key = curses.KEY_RIGHT

    def block(self):
        curses.wrapper(self.main_loop)

    def take_turn(self, game):
        if self.last_key == curses.KEY_UP:
            game.change_direction(Direction.up)
        elif self.last_key == curses.KEY_DOWN:
            game.change_direction(Direction.down)
        elif self.last_key == curses.KEY_LEFT:
            game.change_direction(Direction.left)
        elif self.last_key == curses.KEY_RIGHT:
            game.change_direction(Direction.right)
        elif self.last_key == 10:
            game.start()

    def main_loop(self, screen):
        win = curses.newwin(20, 60, 0, 0)
        win.keypad(1)
        curses.noecho()
        curses.cbreak()

        while True:
            c = win.getch()
            self.last_key = c