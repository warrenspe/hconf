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
try:
    import ConfigParser
    import StringIO
except ImportError:
    import configparser as ConfigParser
import yaml
import sys, itertools, tempfile, os

class INIConfigContext(object):
    """ Defines a context which can be used to create pseudo INI config files for testing purposes. """

    sections = None
    nameDict = {'name': None, 'path': None}

    def __init__(self, d):
        self.d = d
        self.fd = tempfile.NamedTemporaryFile(mode='w+')
        self.__class__.nameDict['path'], self.__class__.nameDict['name'] = os.path.split(self.fd.name)

    def __enter__(self):
        parser = ConfigParser.ConfigParser(self.d.get('DEFAULT', None))
        for sectionName, sectionValues in self.d.items():
            if sectionName != 'DEFAULT':
                parser.add_section(sectionName)
                for configName, configVal in sectionValues.items():
                    parser.set(sectionName, configName, str(configVal))
        parser.write(self.fd)

        self.fd.seek(0)
        return self.fd

    def __exit__(self, *args):
        self.fd.close()


class YAMLConfigContext(object):
    """ Defines a context which can be used to create pseudo YAML files for testing purposes. """

    nameDict = {'name': None, 'path': None}

    def __init__(self, d):
        self.fd = tempfile.NamedTemporaryFile(mode='w+')
        self.__class__.nameDict['path'], self.__class__.nameDict['name'] = os.path.split(self.fd.name)
        self.d = d

    def __enter__(self):
        yaml.dump(self.d, self.fd)
        self.fd.seek(0)
        return self.fd

    def __exit__(self, *args):
        self.fd.close()


class CmdlineConfigContext(object):
    """ Defines a context which can be used to temporarily modify sys.argv. """

    oldArgv = None
    options = None

    def __init__(self, options):
        self.options = options
        self.oldArgv = sys.argv

    def __enter__(self):
        sys.argv = [__file__] + list(itertools.chain(*[('--%s' % o[0].replace('_', '-'), str(o[1])) for o in self.options.items()]))

    def __exit__(self, *args):
        sys.argv = self.oldArgv
