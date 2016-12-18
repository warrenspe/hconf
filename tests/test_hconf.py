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

class HConfTests(tests.HConfTestCase):

    def setUp(self):
        self.configManager = hconf.ConfigManager()

    def testInitRegistering(self):
        self.assertEqual(len(hconf.ConfigManager({'name': 'a'}, {'name': 'b'}).configs), 2)

    def testRegisteringConfigOptions(self):
        self.configManager.addConfig('test', required=False)
        self.configManager.addConfig('test', required=True)
        self.assertTrue(self.configManager.configs['test']['required'])

    def testRegisteringParsers(self):
        self.configManager.registerParser(hconf.Subparsers.Cmdline())
        self.assertRaises(TypeError, self.configManager.registerParser, hconf.Subparsers.Cmdline)

        self.assertEqual(len(self.configManager.parsers), 1)

    def testOverridingConfigurations(self):
        self.configManager.registerParser(hconf.Subparsers.Dictionary({'a': 0}))
        self.configManager.registerParser(hconf.Subparsers.Cmdline())
        self.configManager.addConfig('a', cast=int)

        self.assertEqual(self.configManager.parse()['a'], 0)

        with utils.CmdlineConfigContext({'a': 1}):
            self.assertEqual(self.configManager.parse()['a'], 1)

        self.assertEqual(self.configManager.parse()['a'], 0)

    def testParsingUnknownConfigurations(self):
        self.configManager.registerParser(hconf.Subparsers.Dictionary({'a': 0}))
        self.assertRaises(hconf.Exceptions.UnknownConfigurationException, self.configManager.parse)

    def testDefaultConfigurations(self):
        self.configManager.registerParser(hconf.Subparsers.Dictionary({}))
        self.configManager.addConfig('a', default=1)
        self.assertEqual(self.configManager.parse()['a'], 1)

    def testCastingConfigurations(self):
        self.configManager.registerParser(hconf.Subparsers.Dictionary({'a': (1, 2, 3)}))
        self.configManager.addConfig('a', cast=list)
        self.assertIsInstance(self.configManager.parse()['a'], list)
        self.configManager.addConfig('b', cast=int)
        self.configManager.registerParser(hconf.Subparsers.Dictionary({'b': 'c'}))
        self.assertRaises(hconf.Exceptions.InvalidConfigurationException, self.configManager.parse)

    def testRequiredCongfigurations(self):
        self.configManager.registerParser(hconf.Subparsers.Dictionary({}))
        self.configManager.addConfig('a', required=True)
        self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        self.configManager.registerParser(hconf.Subparsers.Dictionary({'a': 1}))
        self.assertEqual(self.configManager.parse()['a'], 1)

        self.configManager.addConfig('b', required=True, default=1)
        self.assertEqual(self.configManager.parse()['b'], 1)

        self.configManager.addConfig('b', required=True, default=None)
        self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)
