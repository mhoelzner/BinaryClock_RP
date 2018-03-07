import math
import colorsys
from neopixel import Color


class Helpers:

    def __init__(self, config):
        self.configuration = config

    # --------------------------------------------------------------------------

    def bitsOfNumber(self, n):
        # Converts any Numbers in its binary Counterparts
        # 59 = 32 + 16 + 8 + 2 + 1
        a = []
        if n > 0:
            while True:
                bit = math.pow(2, math.floor(math.log(n, 2)))
                a.append(bit)
                n -= a[-1]
                if n == 0:
                    break
        return a

    # --------------------------------------------------------------------------

    def check_if_between(self, value, low, high):

        if value < low:
            value = low
        if value > high:
            value = high

        return value

    # --------------------------------------------------------------------------

    def hsl_to_rgb(self, h, s, v):

        # check h s l values
        h = self.check_if_between(h, 0.0, 1.0)
        s = self.check_if_between(s, 0.0, 1.0)
        v = self.check_if_between(v, 0.0, 1.0)

        rgb = colorsys.hsv_to_rgb(h, s, v)

        r = int(rgb[0] * 255)
        g = int(rgb[1] * 255)
        b = int(rgb[2] * 255)

        # print("R: " + str(r) + " G: " + str(g) + " B: " + str(b))

        return Color(r, g, b)

    # --------------------------------------------------------------------------

    def getRainbowColor(self, rainbow, hue, sat=1.0, val=1.0):

        # setup fore- and background color
        if rainbow == 1:
            return self.hsl_to_rgb(hue, sat, val)
        else:
            return Color(self.configuration.red,
                         self.configuration.green,
                         self.configuration.blue)
