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
import re

# Project imports
from .Exceptions import *
from .Subparsers._subparser import Subparser

__all__ = [
    'ConfigManager',
]

class _Config(object):
    """
    Config object which will be populated and returned as the config object holding all the configuration options.
    """

    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        raise KeyError(str(name))

class ConfigManager(object):
    """
    Config manager which can have a sequence of subparsers assigned to it in order to delegate configuration parsing.
    Expected configuration options are set on the object explicitely.
    """

    configNameRE = re.compile("^[a-zA-Z][\w\-_]*$")

    def __init__(self, *args):
        """
        Initializes a ConfigManager.

        Inputs: args - ConfigManagers can be optionally initialized with a sequence of dictionaries representing
                       configuration options to add to the ConfigManager.
        """

        self.configs = dict()
        self.parsers = list()
        self._config = None

        for arg in args:
            self.addConfig(**arg)

    def registerParser(self, parser):
        """
        Registers a parser to parse configuration inputs.
        """

        if not isinstance(parser, Subparser):
            raise TypeError("%s is not an instance of a subparser." % parser)

        self.parsers.append(parser)

    def addConfig(self, name, default=None, cast=None, required=False, description=None):
        """
        Adds the given configuration option to the ConfigManager.

        Inputs: name        - The configuration name to accept.
                required    - A boolean indicating whether or not the configuration option is required or not.
                cast        - A type (or function accepting 1 argument and returning an object) to cast the input as.
                              If any error occurs during casting an InvalidConfigurationException will be raised.
                default     - The default value to assign to this configuration option.  Note that None is not a valid
                              default if required=True.
                description - A human readable description of this configuration parameter.  Will be displayed when the
                              program is run with a -h flag.
        """

        # Validate the name
        if not self.configNameRE.match(name):
            raise InvalidConfigurationException("Invalid configuration name: %s" % name)

        self.configs[self._sanitizeName(name)] = {
            'default': default,
            'cast': cast,
            'required': required,
            'description': description
        }

    def parse(self):
        """
        Executes the registered parsers to parse input configurations.
        """

        self._config = _Config()

        self._setDefaults()

        for parser in self.parsers:
            for key, value in parser.parse(self, self._config).items():
                key = self._sanitizeName(key)
                if key not in self.configs:
                    raise UnknownConfigurationException(key)
                if value is not None:
                    self._setConfig(key, value)

        self._ensureRequired()
        self._cast()

        return self._config

    def _setDefaults(self):
        """
        Sets all the expected configuration options on the config object as either the requested default value, or None.
        """

        for configName, configDict in self.configs.items():
            self._setConfig(configName, configDict['default'])

    def _ensureRequired(self):
        """
        Ensures that all configuration options marked as being required have been passed (ie are non-None).
        Raises a MissingConfigurationException if a required configuration option was not passed.
        """

        for configName, configDict in self.configs.items():
            if configDict['required']:
                if getattr(self._config, configName) is None:
                    raise MissingConfigurationException(configName)

    def _cast(self):
        """
        Iterates through our parsed configuration options and cast any options with marked cast types.
        """

        for configName, configDict in self.configs.items():
            if configDict['cast'] is not None:
                configValue = getattr(self._config, configName)
                if configValue is not None:
                    try:
                        self._setConfig(configName, configDict['cast'](configValue))

                    except:
                        raise InvalidConfigurationException("%s: %r" % (configName, configValue))

    def _setConfig(self, name, value):
        """
        Sets the configuration option on the current configuration object being populated.

        Inputs: name  - The name of the configuration option to set.
                value - The value of the configuration option to set.
        """

        setattr(self._config, name, value)

    def _sanitizeName(self, name):
        """
        Sanitizes a configuration name so that it can be set onto the Config object safely (ex: replacing -'s with _'s).

        Inputs: name - The string containing the name to sanitize.

        Outputs: A string containing the sanitized string.
        """

        return name.replace('-', '_')
