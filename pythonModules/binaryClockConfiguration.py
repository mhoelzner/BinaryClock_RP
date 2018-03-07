from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError


class ConfigFile:

    def __init__(self, configPath):

        self.show_seconds = 1
        self.old_show_seconds = self.show_seconds
        self.flag_whipeLEDs = (self.show_seconds != self.old_show_seconds)
        self.rainbow = 1
        self.red = 0
        self.green = 0
        self.blue = 255
        self.background = 0
        self.background_value = 128
        self.sensitive = 1
        self.brightness_general = 255
        self.running = 0
        self.stop = 0
        self.plugin = 1

        self.parser = SafeConfigParser()
        self.configPath = configPath

    # --------------------------------------------------------------------------

    def readConfigFile(self):

        self.parser.read(self.configPath)

        self.show_seconds = self.getConfigItem('binaryclock_general',
                                               'show_seconds',
                                               1)
        self.flag_whipeLEDs = (self.show_seconds != self.old_show_seconds)
        self.old_show_seconds = self.show_seconds
        self.rainbow = self.getConfigItem('binaryclock_color',
                                          'rainbow_color',
                                          1)
        self.red = self.getConfigItem('binaryclock_color',
                                      'r_value',
                                      0)
        self.green = self.getConfigItem('binaryclock_color',
                                        'g_value',
                                        0)
        self.blue = self.getConfigItem('binaryclock_color',
                                       'b_value',
                                       255)
        self.background = self.getConfigItem('binaryclock_background',
                                             'background_color',
                                             0)
        self.background_value = self.getConfigItem('binaryclock_background',
                                                   'background_color_value',
                                                   128)
        self.sensitive = self.getConfigItem('binaryclock_sensitiv',
                                            'brightness_time_sensitiv',
                                            1)
        self.brightness_general = self.getConfigItem('binaryclock_sensitiv',
                                                     'brightness_general',
                                                     255)
        self.running = self.getConfigItem('binaryclock_startstop',
                                          'clock_running',
                                          0)
        self.stop = self.getConfigItem('binaryclock_startstop',
                                       'clock_stop',
                                       0)
        self.plugin = self.getConfigItem('binaryclock_plugins',
                                         'plugin_number',
                                         1)

    # --------------------------------------------------------------------------

    def getConfigItem(self, section, option, default):

        try:
            return self.parser.getint(section, option)
        except (NoOptionError, NoSectionError):
            return default

    # --------------------------------------------------------------------------

    def saveConfigFile(self, plugin_number=0, startstop=0):

        self.parser.read(self.configPath)

        if plugin_number == 0:
            self.parser.set('binaryclock_startstop',
                            'clock_running',
                            str(startstop))
            self.parser.set('binaryclock_startstop', 'clock_stop', '0')
        else:
            self.parser.set('binaryclock_plugins',
                            'plugin_number',
                            str(plugin_number))

        with open(self.configPath, 'w') as cf:
            self.parser.write(cf)
