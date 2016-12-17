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
import os
import abc

class SubparserException(Exception):
    """
    Exception class thrown when a subparser encounters an unrecoverable error.
    """

class Subparser(object):
    """
    Base class for subparsers which can be instantiated and registered with a ConfigManager.
    """

    __metaclass__ = abc.ABCMeta
    subparserException = SubparserException

    @abc.abstractmethod
    def parse(self, configManager, config):
        """
        Function which must accept a _Config instance of configuration options parsed thus far, and return a dictionary
        containing new configuration options to add to the _Config object.

        Inputs: configManager - Our parent ConfigManager instance which is constructing the Config object.
                config        - The _Config object containing configuration options populated thus far.

        Outputs: A dictionary of new configuration options to add to the Config object.
        """

        raise NotImplementedError()

class ConfigFileSubparser(Subparser):
    """
    Base class for subparsers which require an input file to parse.
    """

    def __init__(self, filepath=None, filename=None, filepathConfig=None, filenameConfig=None):
        """
        Initializes this configuration file parser.
        Note: At least one set of either filepath & filename, or filepathConfig & filenameConfig must be passed.
              If both are passed, both will be checked, though only the first will be parsed.  The order that they will
              be checked is filenameConfig/filepathConfig first, then filepath/filename second.

        Inputs: filepath       - Either a list containing the path directories to where the configuration file is
                                 stored or a string of the complete path to the directory where the configuration file
                                 to be parsed can be found.
                filename       - The name of the configuration file to be parsed.
                filepathConfig - The name of the configuration option to retrieve the configuration file path from.
                filenameConfig - The name of the configuration option to retrieve the the configuration filename from.
        """

        self.filepath = filepath
        self.filename = filename
        self.filepathConfig = filepathConfig
        self.filenameConfig = filenameConfig

        # Ensure either filepath/filename or filepathConfig/filenameConfig was passed.
        if (filepath is None or filename is None) and (filepathConfig is None or filenameConfig is None):
            raise self.subparserException("A file configuration parser must be either explicitely initialized using " +
                                          "filepath and filename keyword arguments, or filepathConfig and " +
                                          "filenameConfig keyword arguments")

    def _getConfigFile(self, config):
        """
        Retrieves a file descriptor to a configuration file to process.

        Inputs: config - The _Config object which is being populated.

        Outputs: An open file descriptor to the configuration file to parse in read mode if successful, else None.
        """

        joinPath = lambda p: (os.path.join(p) if isinstance(p, (tuple, list)) else p)

        if self.filepathConfig is not None and self.filenameConfig is not None:
            if hasattr(config, self.filepathConfig) and hasattr(config, self.filenameConfig):
                path = joinPath(getattr(config, self.filepathConfig))
                name = getattr(config, self.filenameConfig)

                if os.path.isfile(os.path.join(path, name)):
                    return open(os.path.join(path, name), 'r')

        if self.filepath is not None and self.filename is not None:
            path = joinPath(self.filepath)
            name = self.filename

            if os.path.isfile(os.path.join(path, name)):
                return open(os.path.join(path, name), 'r')
