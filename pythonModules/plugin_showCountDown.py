import time
import binaryClockLEDFunctions as bcl
from neopixel import Color
import fontdemo


class ShowCountDown():

    def __init__(self, strip, c_width, c_height, basepath):
        self.strip = strip
        self.clock_width = c_width
        self.clock_height = c_height
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)
        self.basepath = basepath

    def showCountDown(self):

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

        colors = [Color(255,0,0),
                  Color(255,96,0),
                  Color(255,255,0),
                  Color(128,255,0),
                  Color(0,255,0),
                  Color(0,255,128),
                  Color(0,255,255),
                  Color(0,178,255),
                  Color(0,0,255),
                  Color(128,0,255),
                  Color(255,0,255)]

        for i in range(10):

            if i == 0:
                # 10
                self.stripFunctions.setColorBy1DCoordinate(11,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(23,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(1,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(10,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(13,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(22,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])

                self.stripFunctions.setColorBy1DCoordinate(4,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(8,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(15,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(19,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(17,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(6,colors[i])

            elif i == 1:
                # 9
                self.stripFunctions.setColorBy1DCoordinate(9,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(14,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(15,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(4,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(7,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(16,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(19,colors[i])

            elif i == 2:
                # 8
                self.stripFunctions.setColorBy1DCoordinate(1,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(10,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(13,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(2,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(14,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(8,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(20,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(7,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(16,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(19,colors[i])

            elif i == 3:
                # 7
                self.stripFunctions.setColorBy1DCoordinate(2,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(15,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(4,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(7,colors[i])

            elif i == 4:
                # 6
                self.stripFunctions.setColorBy1DCoordinate(9,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(14,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(2,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(15,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(20,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(6,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(16,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(19,colors[i])

            elif i == 5:
                # 5
                self.stripFunctions.setColorBy1DCoordinate(2,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(9,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(20,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(4,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(16,colors[i])

            elif i == 6:
                # 4
                self.stripFunctions.setColorBy1DCoordinate(9,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(14,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(15,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(4,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(7,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(16,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(19,colors[i])

            elif i == 7:
                # 3
                self.stripFunctions.setColorBy1DCoordinate(2,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(8,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(20,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(7,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(16,colors[i])

            elif i == 8:
                # 2
                self.stripFunctions.setColorBy1DCoordinate(2,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(14,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(3,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(20,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(7,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(19,colors[i])

            elif i == 9:
                # 1
                self.stripFunctions.setColorBy1DCoordinate(11,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(23,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(1,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(10,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(13,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(22,colors[i])
                self.stripFunctions.setColorBy1DCoordinate(21,colors[i])

            self.strip.show()
            time.sleep(1)
            self.stripFunctions.wipeLEDs()

        text = 'Frohes Neues'
        fg_color = colors[10]
        bg_color = Color(0,0,0)
        fps = 5
        count = 1

        # set font
        font = os.path.join(self.basePath, 'other', 'tiny.ttf')

        # setup fontdemo
        fnt = fontdemo.Font(font, self.clock_width)
        txt_width, txt_height, txt_max_descent = fnt.text_dimensions(text)
        txt_as_pixel = fnt.render_text(text)

        # Display text count times
        for i in range(count):

            # Erase previous content
            self.stripFunctions.wipeLEDs(bg_color)

            # Shift text from left to right to show all.
            for cur_offset in range(txt_width - self.clock_width + 1):
                for y in range(txt_height):
                    for x in range(self.clock_width):
                        if txt_as_pixel.pixels[y * txt_width + x + cur_offset]:
                            u_color = fg_color
                        else:
                            u_color = bg_color
                        self.stripFunctions.setColorBy2DCoordinates(x,
                                                                    y,
                                                                    u_color)
                self.strip.show()
                time.sleep(1.0/fps)














