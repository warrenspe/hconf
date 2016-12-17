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
import json

# Project imports
import hconf
import tests

class JSONSubparserTests(tests.HConfTestCase):

    def setUp(self):
        self.configManager = hconf.ConfigManager()

    def testParsingJSONArguments(self):
        inputDict = {'a': 1}
        jsonSubparser = hconf.subparsers.JSON(json.dumps(inputDict))
        self.configManager.registerParser(jsonSubparser)
        self.configManager.addConfig('a')
        self.configManager.addConfig('b', required=True)
        self.configManager.addConfig('c', cast=int)
        self.configManager.addConfig('d', default=2)
        self.configManager.addConfig('e', required=True, cast=int)
        self.configManager.addConfig('f_g', required=True, default=2)
        self.configManager.addConfig('g-g', cast=int, default=2)

        self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        inputDict['b'] = 2
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        inputDict['c'] = 3
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        inputDict['d'] = 4
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        inputDict['e'] = 5
        inputDict['f_g'] = 6
        inputDict['g-g'] = 2
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertEqual(vars(self.configManager.parse()),
                         {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f_g': 6, 'g_g': 2})

        inputDict['g-g'] = 1
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertEqual(vars(self.configManager.parse()),
                         {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f_g': 6, 'g_g': 1})

        del inputDict['g-g']
        del inputDict['f_g']
        del inputDict['d']
        del inputDict['c']
        del inputDict['a']
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertEqual(vars(self.configManager.parse()),
                         {'a': None, 'b': 2, 'c': None, 'd': 2, 'e': 5, 'f_g': 2, 'g_g': 2})

        inputDict['a'] = [1, 2, 3]
        jsonSubparser.jsonString = json.dumps(inputDict)
        self.assertEqual(vars(self.configManager.parse()),
                         {'a': [1, 2, 3], 'b': 2, 'c': None, 'd': 2, 'e': 5, 'f_g': 2, 'g_g': 2})
