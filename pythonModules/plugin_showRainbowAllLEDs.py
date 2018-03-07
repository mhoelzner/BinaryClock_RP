from neopixel import Color
import time


class ShowRainbowAllLEDs():

    def __init__(self, strip, config):

        self.strip = strip
        self.configuration = config

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def showRainbowAllLEDs(self):
        """Draw rainbow that fades across all pixels at once."""
        while True:

            if self.configuration.plugin == 1:
                return

            for j in range(256):

                if self.configuration.plugin == 1:
                    return

                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((i+j) & 255))
                self.strip.show()
                time.sleep(0.02)
