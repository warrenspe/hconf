"""
    Copyright (C) 2016 Warren Spencer warrenspencer27@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author: Warren Spencer
    Email:  warrenspencer27@gmail.com
"""

# Standard imports
try: # Python2/3
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

# Project imports
from ._subparser import ConfigFileSubparser

class INI(ConfigFileSubparser):
    """
    Subparser for parsing .ini configuration files.
    """

    def __init__(self, sections=None, **kwargs):
        """
        Initializes an ini configuration file parser.

        Inputs: sections - A list of sections names which should be parsed.  If not set all sections will be parsed.
                kwargs   - Keyword arguments to be supplied to ConfigFileSubparser.__init__
        """

        super(self.__class__, self).__init__(**kwargs)
        self.sections = sections

    def parse(self, configManager, config):
        """
        Parse configuration options out of an .ini configuration file.

        Inputs: configManager - Our parent ConfigManager instance which is constructing the Config object.
                config        - The _Config object containing configuration options populated thus far.

        Outputs: A dictionary of new configuration options to add to the Config object.
        """

        parser = ConfigParser.RawConfigParser()
        configOptions = dict()
        configFile = self._getConfigFile(config)

        if configFile:
            parser.readfp(configFile)

            for section in parser.sections():
                if self.sections is None or section in self.sections:
                    configOptions.update(parser.items(section))

        return configOptions
