from neopixel import Color
import time
from random import randint
import colorsys
import binaryClockLEDFunctions as bcl


class ShowFire():

    def __init__(self, strip, c_width, c_height, config):
        self.strip = strip
        self.clock_width = c_width
        self.clock_height = c_height
        self.configuration = config
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)

        self.valueMask = [[255, 192, 128, 128, 192, 255],
                          [160, 80, 32, 32, 80, 160],
                          [96, 32, 0, 0, 32, 96],
                          [32, 0, 0, 0, 0, 32]]

        # hueMask[3][5] 3 => zeilen (height) 5 => spalten (width)
        self.hueMask = [[0, 0, 1, 1, 0, 0],
                        [1, 2, 4, 4, 2, 1],
                        [1, 3, 5, 5, 3, 1],
                        [1, 4, 7, 7, 4, 1]]

        self.matrixValue = [[0 for x in range(self.clock_width)]
                            for y in range(self.clock_height)]
        self.line = [0 for x in range(self.clock_width)]
        self.pcnt = 0

    def generateLine(self):
        for x in range(self.clock_width):
            self.line[x] = randint(64, 255)

    def shiftUp(self):
        # for y in range(self.clock_height-1, -1, -1):
        for y in range(self.clock_height - 1):
            for x in range(self.clock_width):
                self.matrixValue[y][x] = self.matrixValue[y+1][x]
        for x in range(self.clock_width):
            self.matrixValue[self.clock_height-1][x] = self.line[x]

    def drawFrame(self):

        # for y in range(self.clock_height-1, -1, -1):
        for y in range(self.clock_height - 1):
            for x in range(self.clock_width):
                nextv = (
                         (
                          (
                           (100.0 - self.pcnt)
                           * self.matrixValue[y][x]
                           + self.pcnt
                           * self.matrixValue[y+1][x]
                          ) / 100.0
                         ) - self.valueMask[y][x]
                        )
                rgb = colorsys.hsv_to_rgb(self.hueMask[y][x] / 255.0,
                                          1.0,
                                          max(0, nextv / 255.0))
                r = int(rgb[0] * 255)
                g = int(rgb[1] * 255)
                b = int(rgb[2] * 255)
                self.stripFunctions.setColorBy2DCoordinates(x,
                                                            y,
                                                            Color(r, g, b))

        for x in range(self.clock_width):

            nextv = (
                     (
                      (
                       (100.0-self.pcnt)
                       * self.matrixValue[self.clock_height-1][x]
                       + self.pcnt
                       * self.line[x]
                      ) / 100.0
                     ) / 255
                    )

            rgb = colorsys.hsv_to_rgb(self.hueMask[0][x] / 255.0,
                                      1.0,
                                      nextv)
            r = int(rgb[0] * 255)
            g = int(rgb[1] * 255)
            b = int(rgb[2] * 255)

            self.stripFunctions.setColorBy2DCoordinates(x,
                                                        self.clock_height - 1,
                                                        Color(r, g, b))

    def showFire(self):

        self.generateLine()

        while True:

            if self.configuration.plugin == 1:
                return

            if self.pcnt >= 100:
                self.shiftUp()
                self.generateLine()
                self.pcnt = 0

            self.drawFrame()
            self.strip.show()
            time.sleep(0.1)
            self.pcnt += 30
