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
import argparse

# Project imports
import hconf
import tests
import utils

class CmdlineSubparserTests(tests.HConfTestCase):

    def setUp(self):
        self.configManager = hconf.ConfigManager()

    def testParsingCmdlineArguments(self):
        self.configManager.registerParser(hconf.Subparsers.Cmdline())
        self.configManager.addConfig('a')
        self.configManager.addConfig('b', required=True)
        self.configManager.addConfig('c', cast=int)
        self.configManager.addConfig('d', default=2)
        self.configManager.addConfig('e', required=True, cast=int)
        self.configManager.addConfig('f_g', required=True, default=2)
        self.configManager.addConfig('g-g', cast=int, default=2)

        with utils.CmdlineConfigContext({'a': 1}):
            self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        with utils.CmdlineConfigContext({'a': 1, 'b': 2}):
            self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        with utils.CmdlineConfigContext({'a': 1, 'b': 2, 'c': 3}):
            self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        with utils.CmdlineConfigContext({'a': 1, 'b': 2, 'c': 3, 'd': 4}):
            self.assertRaises(hconf.Exceptions.MissingConfigurationException, self.configManager.parse)

        with utils.CmdlineConfigContext({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f_g': 6}):
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': '1', 'b': '2', 'c': 3, 'd': '4', 'e': 5, 'f_g': '6', 'g_g': 2})

        with utils.CmdlineConfigContext({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f_g': 6, 'g-g': 1}):
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': '1', 'b': '2', 'c': 3, 'd': '4', 'e': 5, 'f_g': '6', 'g_g': 1})

        with utils.CmdlineConfigContext({'b': 1, 'e': 5}):
            self.assertEqual(vars(self.configManager.parse()),
                             {'a': None, 'b': '1', 'c': None, 'd': 2, 'e': 5, 'f_g': 2, 'g_g': 2})

    def testOverridingGetArgumentParser(self):
        argParser = argparse.ArgumentParser("unit test")
        argParser.add_argument("--a", default=1)
        argParser.add_argument("--b", default=2)

        self.configManager.addConfig('a')
        self.configManager.addConfig('b')

        cmdlineParser = hconf.Subparsers.Cmdline()
        cmdlineParser.getArgumentParser = lambda *_: argParser

        self.configManager.registerParser(cmdlineParser)

        self.assertEqual(vars(self.configManager.parse()), {'a': 1, 'b': 2})

        argParser.add_argument("--c", default=2)

        self.assertRaises(hconf.Exceptions.UnknownConfigurationException, self.configManager.parse)
