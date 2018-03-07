# -*- coding: utf-8 -*-

import datetime
import time
import os.path
import inspect
import math
import threading
from shutil import copyfile
from neopixel import Color, Adafruit_NeoPixel, ws
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import pythonModules.binaryClockConfiguration as bcc
import pythonModules.binaryClockHelpers as bch
import pythonModules.binaryClockLEDFunctions as bcl
import pythonModules.plugin_showTimeAsText as p_TimeAsText
import pythonModules.plugin_showMatrixEffect as p_MatrixEffect
import pythonModules.plugin_showSplashScreen as p_SplashScreen
import pythonModules.plugin_showRainbowAllLEDs as p_RainbowAllLEDs
import pythonModules.plugin_showFire as p_Fire
import RPi.GPIO as GPIO

"""
Created on Mon Sep 18 08:18:43 2017

@author: Hoelzner.M
"""

"""

    Coordinates Layout

        c/x  c/x  c/x  c/x  c/x  c/x

 r/y     00   10   20   30   40   50
 r/y     01   11   21   31   41   51
 r/y     02   12   22   32   42   52
 r/y     03   13   23   33   43   53

         xy   xy   xy   xy   xy   xy
         cr   cr   cr   cr   cr   cr


    LED Layout

          0   1   2   3   4   5  ->--
                                    |
   --<-  11  10   9   8   7   6  -<--
   |
   -->-  12  13  14  15  16  17  ->--
                                    |
         23  22  21  20  19  18  -<--

"""

'''-----------------------------------------------------------------------------
B I N A R Y   C L O C K ----------------------------------------------------'''


class BinaryClock:

    '''
    The class, which makes the binary clock run...
    '''

    def __init__(self):

        GPIO.setmode(GPIO.BOARD)

        # absolute path to current file old: os.getcwd()
        self.basePath = os.path.dirname(
            os.path.abspath(
                inspect.getfile(
                    inspect.currentframe()
                )
            )
        )
        # Number of columns in clock
        self.clock_width = 6
        # Number of rows in clock
        self.clock_height = 4

        self.curr_fg_color = Color(0, 0, 0)
        self.curr_bg_color = Color(0, 0, 0)
        self.flag_clockIndent = False

        # Number of LED pixels.
        LED_COUNT = self.clock_width * self.clock_height
        # GPIO pin connected to the pixels (18 uses PWM!).
        LED_PIN = 18
        # LED signal frequency in hertz (usually 800khz)
        LED_FREQ_HZ = 800000
        # DMA channel to use for generating signal (try 5)
        LED_DMA = 5
        # Set to 0 for darkest and 255 for brightest
        LED_BRIGHTNESS = 128
        # True to invert the signal (when using NPN transistor level shift)
        LED_INVERT = False
        # set to '1' for GPIOs 13, 19, 41, 45 or 53
        LED_CHANNEL = 0
        # Strip type and colour ordering
        LED_STRIP = ws.WS2811_STRIP_GRB

        # path to configuration file
        cfgFilePath = os.path.join(self.basePath, 'config', 'clockConfig.cfg')
        if not os.path.exists(cfgFilePath):
            cfgFilePathDefault = os.path.join(self.basePath,
                                              'config',
                                              'clockConfig_default.cfg')
            copyfile(cfgFilePathDefault, cfgFilePath)

        # configuration setup
        self.configuration = bcc.ConfigFile(cfgFilePath)
        self.configuration.readConfigFile()

        self.helpers = bch.Helpers(self.configuration)

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT,
                                       LED_PIN,
                                       LED_FREQ_HZ,
                                       LED_DMA,
                                       LED_INVERT,
                                       LED_BRIGHTNESS,
                                       LED_CHANNEL,
                                       LED_STRIP)

        # Intialize the library (must be called once before other functions).
        self.strip.begin()

        # LED Functions
        self.stripFunctions = bcl.LEDFunctions(self.strip,
                                               self.clock_width,
                                               self.clock_height)

        # Plugins
        self.plugin2 = p_TimeAsText.ShowTimeAsText(self.strip,
                                                   self.clock_width,
                                                   self.clock_height,
                                                   self.basePath)

        self.plugin3 = p_MatrixEffect.ShowMatrixEffect(self.strip,
                                                       self.clock_width,
                                                       self.clock_height,
                                                       self.configuration)

        self.plugin4 = p_SplashScreen.ShowSplashScreen(self.strip,
                                                       self.clock_width,
                                                       self.clock_height)

        self.plugin5 = p_RainbowAllLEDs.ShowRainbowAllLEDs(self.strip,
                                                           self.configuration)

        self.plugin6 = p_Fire.ShowFire(self.strip,
                                       self.clock_width,
                                       self.clock_height,
                                       self.configuration)

        # initialize the observer event
        watchedDir = os.path.join(self.basePath, 'config')
        self.event_handler = PatternMatchingEventHandler(
            patterns=["*.cfg"],
            ignore_patterns=[],
            ignore_directories=True)
        self.event_handler.on_any_event = self.on_any_event
        self.observer = Observer()
        self.observer.schedule(self.event_handler, watchedDir, recursive=False)
        self.observer.start()

        # ldr gpio pin number
        self.pin_to_circuit = 7
        self.brightness = self.configuration.brightness_general
        self.arr_ldrValues = []

    '''-------------------------------------------------------------------------
    # O T H E R   F U N C T I O N S ----------------------------------------'''

    def rc_time(self):

        while True:

            if self.configuration.running == self.configuration.stop == 1:
                break

            if self.configuration.sensitive == 1:

                GPIO.setup(self.pin_to_circuit, GPIO.OUT)
                GPIO.output(self.pin_to_circuit, GPIO.LOW)

                time.sleep(0.1)

                GPIO.setup(self.pin_to_circuit, GPIO.IN)

                c = 0
                while (GPIO.input(self.pin_to_circuit) == GPIO.LOW):
                    c += 1
                    if c >= 20000:
                        break

                self.arr_ldrValues.append(c)
                # print "c: " + str(c)

                if len(self.arr_ldrValues) == 10:
                    ldrValue = (sum(self.arr_ldrValues) - max(self.arr_ldrValues) -
                                min(self.arr_ldrValues)) / (len(self.arr_ldrValues) - 2)
                    del self.arr_ldrValues[:]

                    self.brightness = int(math.floor(
                        (238 / (1 + math.exp(0.000475 * (2.25 * ldrValue - 10000)))) + 19))
                    print str(self.brightness)

            else:

                self.brightness = self.configuration.brightness_general
                print str(self.brightness)
                time.sleep(0.5)

    # --------------------------------------------------------------------------

    def on_any_event(self, event):
        self.configuration.readConfigFile()
        if self.configuration.flag_whipeLEDs:
            self.stripFunctions.wipeLEDs()

    # --------------------------------------------------------------------------

    def upInTheSky(self):

        backgroundNoSeconds = [1, 2, 3, 4,
                               7, 8, 9, 10,
                               13, 14, 15, 16,
                               19, 20, 21, 22]

        arr = []
        # get current xy coordinates of lit LEDs
        for i in range(self.strip.numPixels()):
            if self.strip.getPixelColor(i) == self.curr_fg_color:
                arr.append(i)

        for j in range(4):
            for i, p in enumerate(arr):
                x, y = self.stripFunctions.get2DCoordinateFrom1D(p)
                self.stripFunctions.setColorBy2DCoordinates(x,
                                                            y - j,
                                                            self.curr_fg_color)
            self.strip.show()
            time.sleep(0.2)
            if self.configuration.show_seconds == 1:
                for i in range(self.strip.numPixels()):
                    self.stripFunctions.setColorBy1DCoordinate(
                        i,
                        self.curr_bg_color,
                        flag_forClock=self.flag_clockIndent)
            else:
                for i in range(len(backgroundNoSeconds)):
                    self.stripFunctions.setColorBy1DCoordinate(
                        backgroundNoSeconds[i],
                        self.curr_bg_color,
                        flag_forClock=self.flag_clockIndent)

        self.strip.show()
        time.sleep(1)

    '''-------------------------------------------------------------------------
    # B I N A R Y   C L O C K   F U N C T I O N S --------------------------'''

    def runClockBinary(self):

        while True:

            # get current time from system
            now = datetime.datetime.now()

            # get current minute and second Value for color within hour
            currTimeValue = now.second + (now.minute * 60)

            # 3600 iterations per hour over Rainbow colors
            for j in range(currTimeValue, 3600):

                if self.configuration.running == self.configuration.stop == 1:

                    # closing animtion
                    self.upInTheSky()
                    self.stripFunctions.wipeLEDs(Color(0, 0, 0))
                    self.configuration.saveConfigFile()
                    return

                # check if plugin should run
                if self.configuration.plugin != 1:
                    return

                # every hue devided into 3600 steps
                h = j / 3600.0

                self.binaryTime(h)

                # sleep for 1 second
                time.sleep(1)

    # --------------------------------------------------------------------------

    def binaryTime(self, hue):

        # foreground color
        colorForeground = self.helpers.getRainbowColor(
            self.configuration.rainbow,
            hue)

        self.curr_fg_color = colorForeground

        backgroundNoSeconds = [1, 2, 3, 4,
                               7, 8, 9, 10,
                               13, 14, 15, 16,
                               19, 20, 21, 22]

        # set background color
        if self.configuration.background == 1:
            colorBackground = Color(self.configuration.background_value,
                                    self.configuration.background_value,
                                    self.configuration.background_value)
        else:
            colorBackground = Color(0, 0, 0)

        self.curr_bg_color = colorBackground

        # show / hide seconds
        if self.configuration.show_seconds == 1:
            for i in range(self.strip.numPixels()):
                self.stripFunctions.setColorBy1DCoordinate(
                    i,
                    colorBackground,
                    flag_forClock=self.flag_clockIndent)
        else:
            for i in range(len(backgroundNoSeconds)):
                self.stripFunctions.setColorBy1DCoordinate(
                    backgroundNoSeconds[i],
                    colorBackground,
                    flag_forClock=self.flag_clockIndent)

        # get current Time
        curTime = datetime.datetime.now()

        # separate date elements
        year = curTime.year
        month = curTime.month
        day = curTime.day

        # separate time elements
        hour = curTime.hour
        minute = curTime.minute
        second = curTime.second

        # new year countdown
        if day == 31 and month == 12 and hour == 23 and minute == 59 and second = 50:
            open(os.path.join(self.basePath, 'other', 'customText.txt'), 'w').close()
            with open(os.path.join(self.basePath, 'other', 'customText.txt'), "a") as myfile:
                myfile.write("10 9 8 7 6 5 4 3 2 1 0 Frohes Neues Jahr " + str(year + 1))
            self.plugin2.showTimeAsText(fg_color=self.curr_fg_color,
                                        bg_color=self.curr_bg_color,
                                        fps=10)
        # ldr log file
        if hour == 0 and minute == 0 and second == 0:
            open(os.path.join(self.basePath, 'config', 'ldrValues.log'), 'w').close()

        if second == 0:
            with open(os.path.join(self.basePath, 'config', 'ldrValues.log'), "a") as myfile:
                myfile.write(str(hour) + ":" + str(minute) +
                             "  -  " + str(self.brightness) + "\n")

        print(str(hour) + ":" + str(minute) + ":" + str(second))

        # column values for hour, minues and seconds
        # if seconds should not be shown, hour and minute columns += 1
        y_posH = 0 if self.configuration.show_seconds == 1 else 1
        y_posM = 2 if self.configuration.show_seconds == 1 else 3
        y_posS = 4

        # hour
        self.columnValuesWithPixel(hour, y_posH, colorForeground)
        # minute
        self.columnValuesWithPixel(minute, y_posM, colorForeground)
        # second
        if self.configuration.show_seconds == 1:
            self.columnValuesWithPixel(second, y_posS, colorForeground)

        self.strip.setBrightness(self.brightness)

        self.strip.show()

    # --------------------------------------------------------------------------

    def columnValuesWithPixel(self, hms_value, time_part, color):

        leftColValues = math.floor(hms_value / 10)
        lst_binaryValuesLeftColumn = self.helpers.bitsOfNumber(leftColValues)

        self.binaryValueParse(lst_binaryValuesLeftColumn, time_part, 0, color)

        rightColValues = hms_value - (leftColValues * 10)
        lst_binaryValuesRightColumn = self.helpers.bitsOfNumber(rightColValues)

        self.binaryValueParse(lst_binaryValuesRightColumn, time_part, 1, color)

    # --------------------------------------------------------------------------

    def binaryValueParse(self, lst, time_part, lor, color):

        # time_part = 0(1) -> hour   2(3) -> minute   4 -> second
        # lor       = 0 -> left   1 -> right

        dic_binary = {1: 3, 2: 2, 4: 1, 8: 0}

        x = time_part + lor

        for i in range(len(lst)):
            y = dic_binary.get(lst[i])
            self.stripFunctions.setColorBy2DCoordinates(
                x,
                y,
                color,
                flag_forClock=self.flag_clockIndent)

    '''-------------------------------------------------------------------------
    # P L U G I N S --------------------------------------------------------'''

    def runPlugin(self):

        if self.configuration.plugin == 2:
            self.plugin2.showTimeAsText(fg_color=self.curr_fg_color,
                                        bg_color=self.curr_bg_color,
                                        fps=5)
        elif self.configuration.plugin == 3:
            self.plugin3.showMatrixEffect()
        elif self.configuration.plugin == 4:
            self.plugin4.showSplashScreen()
        elif self.configuration.plugin == 5:
            self.plugin5.showRainbowAllLEDs()
        elif self.configuration.plugin == 6:
            self.plugin6.showFire()

        self.stripFunctions.wipeLEDs()

        # reset plugin_number to 1 -> binaryClock
        # after finishing running plugin
        self.configuration.plugin = 1
        self.configuration.saveConfigFile(plugin_number=1)

    # --------------------------------------------------------------------------

    '''-------------------------------------------------------------------------
    # M A I N   F U N C T I O N S ------------------------------------------'''

    def main(self):

        # update config file to say clock is running
        self.configuration.saveConfigFile(startstop=1)

        # Startsequence show for 5 seconds
        self.plugin4.showSplashScreen()

        try:

            while True:

                # check if clock should be stopped
                if self.configuration.running == self.configuration.stop == 1:
                    # closing animtion
                    self.stripFunctions.wipeLEDs(Color(0, 0, 0))
                    self.configuration.saveConfigFile()
                    return

                # check which plugin to run
                # 1 = Time in binary format
                if self.configuration.plugin == 1:
                    self.runClockBinary()
                else:
                    self.runPlugin()

        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    # --------------------------------------------------------------------------


if __name__ == '__main__':

    binaryClock = BinaryClock()
    t1 = threading.Thread(target=binaryClock.rc_time)
    t1.daemon = True
    t1.start()
    binaryClock.main()
