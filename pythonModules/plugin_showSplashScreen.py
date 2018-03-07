import time
import binaryClockLEDFunctions as bcl
from neopixel import Color


class ShowSplashScreen():

    def __init__(self, strip, c_width, c_height):
        self.strip = strip
        self.clock_width = c_width
        self.clock_height = c_height
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)

    def showSplashScreen(self):

        '''

               0   1   2   3   4   5  ->--
                                       |
        --<-  11  10   9   8   7   6  -<--
        |
        -->-  12  13  14  15  16  17  ->--
                                       |
              23  22  21  20  19  18  -<--

        '''

        # Erase previous content
        self.stripFunctions.wipeLEDs()

        splashItemsOtherColor = [23, 22, 13, 10,
                                 21, 20, 15, 8,
                                 19, 18, 17, 6]

        splashItems = [23, 12, 11, 0,
                       1, 10, 13, 22,
                       21, 14, 9, 2,
                       3, 8, 15, 20,
                       19, 16, 7, 4,
                       5, 6, 17, 18]

        splashColor1 = Color(0, 0, 255)
        splashColor2 = Color(255, 255, 0)
        splashColor3 = Color(0, 0, 0)

        for i in range(len(splashItems)):
            if splashItems[i] in splashItemsOtherColor:
                self.stripFunctions.setColorBy1DCoordinate(splashItems[i],
                                                           splashColor1)
            else:
                self.stripFunctions.setColorBy1DCoordinate(splashItems[i],
                                                           splashColor2)
            self.strip.show()
            time.sleep(0.1)
        for i in range(len(splashItems)):
            self.stripFunctions.setColorBy1DCoordinate(splashItems[i],
                                                       splashColor3)
            self.strip.show()
            time.sleep(0.1)
