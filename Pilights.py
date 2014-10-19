import time
from LedStrip_WS2801 import LedStrip_WS2801
import threading


class Pilights:
    black = [0, 0, 0]
    white = [255, 255, 255]
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    yellow = [255, 255, 0]
    purple = [255, 0, 255]

    def __init__(self, width, height, render_target):
        self.width = width
        self.height = height
        self.changed = True

        self.ledStrip = LedStrip_WS2801(width * height)
        self.mix_speed = 40
        self.current_grid = [[self.black] * width for x in xrange(height)]
        self.wanted_grid = [[self.black] * width for x in xrange(height)]

        pi_thread = threading.Thread(target=self.render_loop)
        pi_thread.daemon = True
        pi_thread.start()

        test_patten = TestPattern()
        self.render_target = test_patten
        test_patten.test()  # Blocks whilst it changes colours
        self.render_target = render_target

    def mix_color(self, from_colour, to_colour):
        r = self.mix_int(from_colour[0], to_colour[0])
        g = self.mix_int(from_colour[1], to_colour[1])
        b = self.mix_int(from_colour[2], to_colour[2])
        return [r, g, b]

    def mix_int(self, from_int, to_int):
        capped_mix_speed = min(self.mix_speed, abs(from_int - to_int))
        if from_int > to_int:
            return from_int - capped_mix_speed
        else:
            return from_int + capped_mix_speed

    def render_loop(self):
        while True:
            self.render_target.render(self)

            if self.changed:
                for i in range(0, self.width):
                    for j in range(0, self.height):
                        wanted_pixel = self.wanted_grid[i][j]
                        current_pixel = self.current_grid[i][j]
                        self.current_grid[i][j] = self.mix_color(current_pixel, wanted_pixel)

                counter = 0
                for i in range(0, self.width):
                    for j in range(0, self.height):
                        modded_j = (self.height - 1 - j) if (i % 2 == 1) else j
                        self.ledStrip.setPixel(counter, self.current_grid[modded_j][i])
                        counter += 1
                self.ledStrip.update()
            time.sleep(0.01)
            self.changed = False

    def set(self, i, j, colour):
        self.changed = True
        self.wanted_grid[j][i] = colour

    def fill(self, colour):
        self.changed = True
        for i in range(0, self.width):
            for j in range(0, self.height):
                self.wanted_grid[j][i] = colour

    def clear(self):
        self.fill(self.black)


class TestPattern:
    def __init__(self):
        self.colour = [0, 0, 0]

    def test(self):
        def fill_and_sleep(colour, sleep_time=0.3):
            self.colour = colour
            time.sleep(sleep_time)

        fill_and_sleep([255, 0, 0])
        fill_and_sleep([0, 255, 0])
        fill_and_sleep([0, 0, 255])
        fill_and_sleep([255, 255, 255])
        fill_and_sleep([0, 0, 0], 1)

    def render(self, pilights):
        pilights.fill(self.colour)