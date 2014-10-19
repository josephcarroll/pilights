from collections import namedtuple
from enum import Enum
from random import randint
import time
from colorsys import *

Position = namedtuple('Position', ['x', 'y'])


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4


class State(Enum):
    playing = 1
    game_over = 2


class Snake:
    direction_opposites = {
        Direction.up: Direction.down,
        Direction.down: Direction.up,
        Direction.left: Direction.right,
        Direction.right: Direction.left
    }

    def __init__(self, width, height, player):
        self.width = width
        self.height = height
        self.player = player

        self.state = State.playing
        self.eaten = 0
        self.level = 0
        self.level_up = False
        self.snake = [Position((self.width / 2) - 1, self.height / 2), Position(self.width / 2, self.height / 2)]
        self.direction = Direction.right
        self.new_direction = Direction.right
        self.food = Position(self.width / 2 + 3, self.height / 2)
        self.food_hue = 0.0

    def start(self):
        if self.state != State.playing:
            self.__init__(self.width, self.height, self.player)

    def render(self, pilights):
        if self.level_up:
            pilights.fill([0, 0, 100])
        else:
            pilights.clear()

        # Food
        food_colour = tuple(int(i * 255) for i in hsv_to_rgb(self.food_hue, 1, 1))
        self.food_hue += 0.005
        pilights.set(self.food.x, self.food.y, food_colour)

        # Snake body
        body_colour = pilights.green if self.state == State.playing else pilights.red
        brightness = 0.4
        actual_colour = tuple(int(i * brightness) for i in body_colour)
        for position in self.snake:
            pilights.set(position.x, position.y, actual_colour)

        # Snake head
        head_colour = tuple(int(i * brightness) for i in pilights.purple)
        pilights.set(self.snake[-1].x, self.snake[-1].y, head_colour)

    def change_direction(self, new_direction):
        self.new_direction = new_direction

    def random_position(self):
        return Position(randint(0, self.width - 1), randint(0, self.height - 1))

    def sleep(self):
        sleep_factor = self.level * 0.03
        time.sleep(max(0.07, 0.2 - sleep_factor))

    def update(self):
        if self.state == State.game_over:
            return

        self.player.take_turn(self)

        # If we level up in the previous update, we reset here!
        self.level_up = False

        if self.new_direction != self.direction_opposites[self.direction]:
            self.direction = self.new_direction

        x_change = 0
        y_change = 0

        if self.direction == Direction.up:
            y_change = -1
        elif self.direction == Direction.down:
            y_change = 1
        elif self.direction == Direction.left:
            x_change = -1
        elif self.direction == Direction.right:
            x_change = 1

        head_position = self.snake[-1]
        new_position = Position(head_position.x + x_change, head_position.y + y_change)

        if new_position.x < 0 or new_position.y < 0 or new_position.x >= self.width or new_position.y >= self.height:
            self.state = State.game_over
            return

        if new_position in self.snake[:-1]:  # Note that we exclude the tail from this check as it will disappear!
            self.state = State.game_over
            self.snake.append(new_position)  # So the player can see where the head is when dead
            return

        self.snake.append(new_position)
        if new_position == self.food:
            new_food = self.random_position()
            while new_food in self.snake:
                new_food = self.random_position()
            self.food = new_food
            self.eaten += 1
            if self.eaten % 10 == 0:
                self.level += 1
                self.level_up = True

        else:
            self.snake.pop(0)