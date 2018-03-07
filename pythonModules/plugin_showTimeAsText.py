import fontdemo
import datetime
import time
import os.path
import binaryClockLEDFunctions as bcl


class ShowTimeAsText():

    def __init__(self,
                 strip,
                 c_width,
                 c_height,
                 basePath):
        self.strip = strip
        self.clock_width = c_width
        self.clock_height = c_height
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)
        self.basePath = basePath

    def showTimeAsText(self, fg_color, bg_color, fps=10, count=1):

        # get current time from system
        curTime = datetime.datetime.now()

        # separate time elements
        hour = curTime.hour
        minute = curTime.minute

        # set the displaying text
        # default is time with hours and minutes
        # if customText file exists then display the text within the file
        text = '   ' \
               + format(hour, '02d') \
               + ':' \
               + format(minute, '02d') \
               + '   '

        # customText file readout if exists
        pathToTextFile = os.path.join(self.basePath, 'other', 'customText.txt')
        if os.path.exists(pathToTextFile):
            with open(pathToTextFile, 'r') as f:
                text = '   ' + f.read() + '   '
            os.remove(pathToTextFile)

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
