import time
import binaryClockLEDFunctions as bcl
from neopixel import Color
import random


class ShowMatrixEffect():

    def __init__(self, strip, c_width, c_height, config):
        self.strip = strip
        self.clock_width = c_width
        self.clock_height = c_height
        self.configuration = config
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)

    def showMatrixEffect(self):

        # Colors from black to green (and a bit gray-ish)
        colors = []
        for i in range(0, 8):
            colors.append(Color(0, int(255.0 / 10 * i), 0))
        colors.append(Color(50, 204, 30))
        colors.append(Color(50, 230, 30))
        colors.append(Color(80, 255, 60))

        threadhold = 0.8

        rain = [20 for _ in range(0, 6)]
        while True:

            if self.configuration.plugin == 1:
                return

            # Erase previous content
            self.stripFunctions.wipeLEDs()

            for x, y in enumerate(rain):
                if (y == 20):
                    # reset y coordinate randomly
                    if (random.random() > threadhold):
                        rain[x] = 0
                else:
                    # simple alpha blending using our predefined colors
                    y0 = max(y - 10, 0)
                    y1 = min(9, y)
                    ci = y0 - (y - 10)
                    for yi, yn in enumerate(range(y0, y1 + 1)):
                        color = colors[ci + yi]
                        self.stripFunctions.setColorBy2DCoordinates(x,
                                                                    yn,
                                                                    color)
                    # advance y coordinate
                    rain[x] = y + 1

            self.strip.show()
            time.sleep(0.1)
