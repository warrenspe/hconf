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

# Standard import
import json

# Project imports
from ._subparser import Subparser

class JSON(Subparser):
    """
    Subparser for parsing JSON strings.
    """

    def __init__(self, jsonString):
        """
        Initializes a JSON string parser.

        Inputs: jsonString - The JSON string to parse.
        """

        self.jsonString = jsonString

    def parse(self, configManager, config):
        """
        Parse configuration options out of a YAML configuration file.

        Inputs: configManager - Our parent ConfigManager instance which is constructing the Config object.
                config        - The _Config object containing configuration options populated thus far.

        Outputs: A dictionary of new configuration options to add to the Config object.
        """

        jsonConfigs = json.loads(self.jsonString)
        if isinstance(jsonConfigs, dict):
            return jsonConfigs

        raise self.subparserException("JSON string parsed did not result in a dictionary, but instead a %s"
                                      % type(jsonConfigs))
