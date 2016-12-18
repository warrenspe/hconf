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
import argparse

# Project imports
from ._subparser import Subparser

class Cmdline(Subparser):
    """
    Subparser for parsing cmdline inputs.
    """

    def __init__(self, description=None):
        """
        Initializes a cmdline parser.

        Inputs: description - A description to print if a user runs this program with a -h flag.
        """

        self.description = description

    def getArgumentParser(self, configManager, config):
        """
        May be overidden to provide custom functionality.
        Constructs an argparse.ArgumentParser used to parse configuration options from the command line.

        Inputs: configManager - Our parent ConfigManager instance which is constructing the Config object.
                config        - The _Config object containing configuration options populated thus far.

        Outputs: An argparse.ArgumentParser object intialized to parse command line configuration options.
        """

        argParser = argparse.ArgumentParser(self.description)
        for configName, configDict in configManager.configs.items():
            cmdName = configName.replace("_", "-")
            argParser.add_argument(
                '--%s' % cmdName,
                default=None,
                help=configDict['description']
            )

        return argParser

    def parse(self, configManager, config):
        """
        Parses commandline arguments, given a series of configuration options.

        Inputs: configManager - Our parent ConfigManager instance which is constructing the Config object.
                config        - The _Config object containing configuration options populated thus far.

        Outputs: A dictionary of new configuration options to add to the Config object.
        """

        argParser = self.getArgumentParser(configManager, config)
        return vars(argParser.parse_args())
