#!/usr/bin/python

import time
import sys
from datetime import datetime, timedelta
from colorsys import *

from dateutil.parser import parse

from Pilights import Pilights


class CountdownRender:
    def __init__(self, current, target):
        self.current = current
        self.target = target
        self.hue = 0

        self.numbers = {
            0:  self.read("numbers/zero"),
            1:  self.read("numbers/one"),
            2:  self.read("numbers/two"),
            3:  self.read("numbers/three"),
            4:  self.read("numbers/four"),
            5:  self.read("numbers/five"),
            6:  self.read("numbers/six"),
            7:  self.read("numbers/seven"),
            8:  self.read("numbers/eight"),
            9:  self.read("numbers/nine"),
            10: self.read("numbers/ten")
        }

    def read(self, name):
        file = open(name)
        lines = file.readlines()
        result = [[0 for x in range(11)] for x in range(11)]
        for i in range(0, 11):
            for j in range(0, 11):
                result[i][j] = lines[j][i]
        return result

    def render(self, pilights):
        pixel_count = pilights.width * pilights.height
        now = datetime.now()
        initial_distance = (self.target - self.current).total_seconds()
        current_distance = (self.target - now).total_seconds()
        current_distance_seconds = max(int(round(current_distance)), 0)

        percent = (initial_distance - current_distance) / initial_distance
        capped_percent = min(percent, 1.0)
        light_count = int(capped_percent * pixel_count)

        if current_distance_seconds <= 10:
            number = self.numbers.get(current_distance_seconds)
            for i in range(0, 11):
                for j in range(0, 11):
                    if number[i][j] == "x":
                        pilights.set(i, j, Pilights.white)
                    else:
                        pilights.set(i, j, Pilights.black)
        else:
            colour = tuple(int(i * 255) for i in hsv_to_rgb(self.hue, 1, 0.5))
            self.hue += 0.005
            count = 0
            for i in range(0, 11):
                for j in range(0, 11):
                    if count < light_count:
                        pilights.set(i, j, colour)
                    else:
                        pilights.set(i, j, Pilights.black)
                    count += 1

if __name__ == '__main__':
    current = datetime.now()
    target = parse(sys.argv[1])
    print "Counting down from {} to {}".format(current, target)
    renderer = CountdownRender(current, target)

    pilights = Pilights(11, 11, renderer)

    while True:
        time.sleep(1)