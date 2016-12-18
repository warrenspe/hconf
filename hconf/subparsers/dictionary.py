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

# Project imports
from ._subparser import Subparser

class Dictionary(Subparser):
    """
    Subparser for parsing Python-passed configuration options.
    """

    def __init__(self, dictionary):
        """
        Initializes a dictionary parser.

        Inputs: dictionary - A dictionary containing key: value pairs of configName: configValue of config options to
                             add to the configuration object.
        """

        self.dictionary = dictionary

    def parse(self, *args):
        """
        Return our initialized dictionary arguments.
        """

        if isinstance(self.dictionary, dict):
            return self.dictionary

        raise self.subparserException("Argument passed to Dictionary SubParser is not a dict: %s" % type(self.dictionary))
