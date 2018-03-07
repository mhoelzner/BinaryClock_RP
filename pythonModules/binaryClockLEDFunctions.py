
'''-----------------------------------------------------------------------------
# S T R I P   F U N C T I O N S --------------------------------------------'''

from neopixel import Color


class LEDFunctions:

    def __init__(self, strip, c_width, c_height):
        self.strip = strip
        self.clock_width = c_width
        self.clock_height = c_height

    # --------------------------------------------------------------------------

    def wipeLEDs(self, color=Color(0, 0, 0)):
        for i in range(self.strip.numPixels()):
            self.setColorBy1DCoordinate(i, color)
        self.strip.show()

    # --------------------------------------------------------------------------

    def setColorBy1DCoordinate(self, pos, color, flag_forClock=False):

        if flag_forClock:
            if pos in (0, 2, 4, 11):
                color = Color(0, 0, 0)

        self.strip.setPixelColor(pos, color)

    # --------------------------------------------------------------------------

    def setColorBy2DCoordinates(self, x, y, color, flag_forClock=False):

        pos = self.get1DCoordinateFrom2D(x, y)

        if flag_forClock:
            if pos in (0, 2, 4, 11):
                color = Color(0, 0, 0)
                print('1D: ' + str(flag_forClock) + ' pos: ' + str(pos))

        self.setColorBy1DCoordinate(pos, color)

    # --------------------------------------------------------------------------

    def get1DCoordinateFrom2D(self, x, y):

        # check if even or odd row
        if y % 2 == 0:
            pos = x + (self.clock_width * y)
        else:
            pos = ((self.clock_width - 1) - x) + (self.clock_width * y)

        return pos

    # --------------------------------------------------------------------------

    def get2DCoordinateFrom1D(self, pos):

        y = (abs((pos % self.clock_width) - pos) / self.clock_width)
        if y % 2 == 0:
            x = pos % self.clock_width
        else:
            x = (self.clock_width - 1) - (pos % self.clock_width)

        return x, y
