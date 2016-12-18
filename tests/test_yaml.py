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
import hconf
import tests
import utils

class YAMLSubparserTests(tests.HConfTestCase):

    def setUp(self):
        self.configManager = hconf.ConfigManager()

    def testParsingYAMLArguments(self):
        yamlParser = hconf.Subparsers.YAML(filepathConfig='path', filenameConfig='name')
        self.configManager.registerParser(hconf.Subparsers.Dictionary(utils.YAMLConfigContext.nameDict))
        self.configManager.registerParser(yamlParser)
        self.configManager.addConfig('name')
        self.configManager.addConfig('path')
        self.configManager.addConfig('a')
        self.configManager.addConfig('b', required=True)
        self.configManager.addConfig('c', cast=int)
        self.configManager.addConfig('d', default=2)
        self.configManager.addConfig('e', required=True, cast=int)
        self.configManager.addConfig('f_g', required=True, default=2)
        self.configManager.addConfig('g-g', cast=int, default=2)

        # Test parsing a complete ini file & default
        with utils.YAMLConfigContext({'a': 1, 'b': 2}) as fd:
            self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        with utils.YAMLConfigContext({'a': 1, 'b': 2, 'e': 3, 'f-g': 1, 'g_g': 1}) as fd:
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': 1, 'b': 2, 'c': None, 'd': 2, 'e': 3, 'f_g': 1, 'g_g': 1,
                              'name': utils.YAMLConfigContext.nameDict['name'],
                              'path': utils.YAMLConfigContext.nameDict['path']})

        with utils.YAMLConfigContext({'a': 1, 'b': 2, 'e': 3, 'f-g': 1, 'g_g': 1}) as fd:
            configManager2 = hconf.ConfigManager()
            configManager2.configs = self.configManager.configs
            configManager2.registerParser(hconf.Subparsers.YAML(
                filepath=utils.YAMLConfigContext.nameDict['path'],
                filename=utils.YAMLConfigContext.nameDict['name']
            ))
            
            self.assertEqual(vars(configManager2.parse()),
                             {'a': 1, 'b': 2, 'c': None, 'd': 2, 'e': 3, 'f_g': 1, 'g_g': 1, 'name': None, 'path': None})
