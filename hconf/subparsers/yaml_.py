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
import yaml

# Project imports
from ._subparser import ConfigFileSubparser

class YAML(ConfigFileSubparser):
    """
    Subparser for parsing .yaml & .yml configuration files.
    """

    def parse(self, configManager, config):
        """
        Parse configuration options out of a YAML configuration file.

        Inputs: configManager - Our parent ConfigManager instance which is constructing the Config object.
                config        - The _Config object containing configuration options populated thus far.

        Outputs: A dictionary of new configuration options to add to the Config object.
        """

        configFile = self._getConfigFile(config)

        if not configFile:
            return dict()

        yamlConfigs = yaml.load(configFile)
        if isinstance(yamlConfigs, dict):
            return yamlConfigs

        raise self.subparserException("YAML config parsed did not result in a dictionary, but instead a: %s"
                                      % type(yamlConfigs))
