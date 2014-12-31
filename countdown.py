#!/usr/bin/python

import time
import sys
from datetime import datetime
from colorsys import *

from dateutil.parser import parse

from Pilights import Pilights


class CountdownRender:
    def __init__(self, current, target):
        self.current = current
        self.target = target
        self.hue = 0
        self.pixel_count = pilights.width * pilights.height

    def render(self, pilights):
        now = datetime.now()
        initial_distance = (self.target - self.current).total_seconds()
        current_distance = (self.target - now).total_seconds()

        percent = (initial_distance - current_distance) / initial_distance
        capped_percent = min(percent, 1.0)
        light_count = int(capped_percent * self.pixel_count)

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
    target = parse(sys.argv[1])
    current = datetime.now()
    print "Counting down from {} to {}".format(current, target)
    renderer = CountdownRender(current, target)

    pilights = Pilights(11, 11, renderer)

    while True:
        time.sleep(1)