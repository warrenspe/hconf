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
from .Subparsers._subparser import SubparserException

__all__ = [
    'UnknownConfigurationException',
    'InvalidConfigurationException',
    'MissingConfigurationException',
    'SubparserException',
]

class UnknownConfigurationException(Exception):
    """
    Raised when an unknown configuration option is parsed from a ConfigManager object.
    """

class InvalidConfigurationException(Exception):
    """
    Raised when the configuration value for a given configuration option is invalid.
    """

class MissingConfigurationException(Exception):
    """
    Raised when a required configuration option is not passed.
    """
