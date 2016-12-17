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

class INISubparserTests(tests.HConfTestCase):

    def setUp(self):
        self.configManager = hconf.ConfigManager()

    def testParsingINIArguments(self):
        iniParser = hconf.subparsers.INI(filepathConfig='path', filenameConfig='name')
        self.configManager.registerParser(hconf.subparsers.Dictionary(utils.INIConfigContext.nameDict))
        self.configManager.registerParser(iniParser)
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
        with utils.INIConfigContext({'DEFAULT': {'a': 1}, 'a': {'b': 2}}) as fd:
            self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        with utils.INIConfigContext({'DEFAULT': {'a': 1, 'b': 2}, 'a': {'e': 3}}) as fd:
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': '1', 'b': '2', 'c': None, 'd': 2, 'e': 3, 'f_g': 2, 'g_g': 2,
                              'name': utils.INIConfigContext.nameDict['name'],
                              'path': utils.INIConfigContext.nameDict['path']})

        # Test parsing only certain sections out of an ini file
        with utils.INIConfigContext({'DEFAULT': {'e': 3, 'b': 2}, 'a': {'a': 1}, 'b': {'g_g': 5, 'f-g': 4}}) as fd:
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': '1', 'b': '2', 'c': None, 'd': 2, 'e': 3, 'f_g': '4', 'g_g': 5,
                              'name': utils.INIConfigContext.nameDict['name'],
                              'path': utils.INIConfigContext.nameDict['path']})
            iniParser.sections = ['a', 'b']
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': '1', 'b': '2', 'c': None, 'd': 2, 'e': 3, 'f_g': '4', 'g_g': 5,
                              'name': utils.INIConfigContext.nameDict['name'],
                              'path': utils.INIConfigContext.nameDict['path']})
            iniParser.sections = ['b']
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': None, 'b': '2', 'c': None, 'd': 2, 'e': 3, 'f_g': '4', 'g_g': 5,
                              'name': utils.INIConfigContext.nameDict['name'],
                              'path': utils.INIConfigContext.nameDict['path']})

        with utils.INIConfigContext({'DEFAULT': {'e': 3, 'b': 2}, 'a': {'a': 1}, 'b': {'g_g': 5, 'f-g': 4}}) as fd:
            configManager2 = hconf.ConfigManager()
            configManager2.configs = self.configManager.configs
            configManager2.registerParser(hconf.subparsers.INI(
                filepath=utils.INIConfigContext.nameDict['path'],
                filename=utils.INIConfigContext.nameDict['name']
            ))
            
            self.assertEqual(vars(configManager2.parse()),
                             {'a': '1', 'b': '2', 'c': None, 'd': 2, 'e': 3, 'f_g': '4', 'g_g': 5, 'name': None, 'path': None})
