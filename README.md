# hconf
Hierarchical configuration manager for Python 2/3.

hconf allows configurations from multiple sources to be prioritized and amalgamated onto a single object.  Configuration options and parsers must be registered with an hconf.ConfigManager which can then be used to produce the resulting configuration object.

## Installation
hconf can be installed using pip:

`pip install hconf`

Alternatively, hconf can be installed manually by cloning this repo and running the following command in the main directory:

`python setup.py install`

## Example
```
>>> import hconf

>>> configMgr = hconf.ConfigManager()

>>> # Add configuration options
>>> configMgr.addConfig('start-time', required=True, cast=int)
>>> configMgr.addConfig('end-time', cast=int)
>>> configMgr.addConfig('action', required=True, default='list')

>>> # Add parsers; configuration options will be acquired from them in order
>>> configMgr.addParser(hconf.Subparsers.Cmdline("Program -h description")
>>> configMgr.addParser(hconf.Subparsers.YAML(filename="program.cfg", filepath='/etc/program/conf')

>>> # Parse configuration options into an object
>>> config = configMgr.parse()
>>> print vars(config)
{
 'start-time': 1234567890,
 'end-time': None,
 'action': 'list'
}
```

## Usage
### hconf.ConfigManager
Object which controls the registering of configuration options and subparsers.

#### hconf.ConfigManager.\_\_init\_\_
When hconf.ConfigManager objects are instantiated they can optionally be passed a series of dictionaries representing arguments to addConfig calls.  The code below creates two equivalent ConfigManager objects
```
>>> c1 = hconf.ConfigManager()
>>> c1.addConfig('a', required=True, cast=int, default=0)
>>> c1.addConfig('b', required=False, default=1)

>>> c2 = hconf.ConfigManager(
...     {'name': 'a', 'required': True, 'cast': int, 'default': 0},
...     {'name': 'b', 'required': False, 'default': 1}
... )
```

#### hconf.ConfigManager.addConfig
Registers a configuration object with the manager.  Only configuration options registered with the manager will be populated on the resulting configuration obejct returned from ConfigManager.parse.  Any non-registered configuration options received from the registered subparsers will raise an UnknownConfigurationException.
Accepts 5 arguments, with the first being required and the following 4 optional.
* name - The name of the configuration option to accept.  Note that any -'s in the name will be converted to \_'s on the resulting configuration object.  It must also not start with a number and must contain only alphanumeric characters, dashes and underscores.
* required - A boolean indicating whether or not this configuration option is required or not.  If not passed and not required, will be set to None on the resulting configuration object.  If not passed and required, a MissingConfigurationException will be raised.
* cast - A type (or function accepting 1 argument and returning an object) to cast the input as. If any error occurs during casting an InvalidConfigurationException will be raised.
* default - The default value to assign to this configuration option if not passed.  Note that default=None is not valid if required=True, as required=True will force a MissingConfigurationException to be raised if the final value of the configuration option is None.
* description - A human readable description of this configuration parameter.  Will be displayed when the program is run with a -h flag and a Cmdline subparser is registered.
```
>>> c1 = hconf.ConfigManager()
>>> c1.addConfig('a', required=True, cast=int, default=0, description="A parameter")
>>> c1.addConfig('b', required=False, default=1)
```

#### hconf.ConfigManager.registerParser
Registers a subparser to parse configuration options from some source.  A list of the pre-built subparsers can be found below.  The parsers will be run in the order that they are registered with the manager.  If an earlier parser parses out a configuration option and then a later parser parses out the same configuration option, the later parser will overwrite the earlier parsers configuration value.  In this way you can specify a hierarchy of configuration sources.  For example, cmdline >= Config File >= Defaults.
If the parser passed to registerParser is not a subclass of hconf.Subparsers.Subparser a TypeError is raised.
```
>>> confMgr = hconf.ConfigManager()
>>> confMgr.addConfig('a')
>>> confMgr.registerParser(hconf.Subparsers.Dictionary({'a': 1}))
>>> confMgr.registerParser(hconf.Subparsers.Dictionary({'a': 2}))

>>> vars(confMgr.parse())
{'a': 2}
```

#### hconf.ConfigManager.parse
Parses registered configuration options using the registered subparsers into a configuration object.  Accepts no parameters.
Configuration options can be extracted from the returned configuration object either by attribute lookup or dictionary lookup.
```
>>> confMgr = hconf.ConfigManager()
>>> confMgr.addConfig('a')
>>> confMgr.registerParser(hconf.Subparsers.Dictionary({'a': 1}))

>>> config = confMgr.parse()
>>> config['a']
1
>>> config.a
1
```

### hconf.Exceptions
The hconf.Exceptions module contains exceptions which may be thrown by ConfigManager objects.

#### hconf.Exceptions.InvalidConfigurationException
Thrown by ConfigManager.addConfig when a configuration option with an invalid name is registered.

Thrown by ConfigManager.parse when a configuration option is registered with a cast, and the cast raises an exception.

#### hconf.Exceptions.MissingConfigurationException
Thrown by ConfigManager.parse when a configuration option registered with required=True would be returned with the resulting config object with a value of None.

#### hconf.Exceptions.UnknownConfigurationException
Thrown by ConfigManager.parse when an unregistered configuration option is parsed by a subparser.

#### hconf.Exceptions.SubparserException
Thrown by various subparsers on initialization/parsing when an error occurs.

### hconf.Subparsers
Module which contains subparsers which can be registered to a ConfigManager using ConfigManager.registerParser.  You can define your own subparsers by overriding hconf.subparser.Subparser or hconf.subparser.ConfigFileSubparser.

#### hconf.Subparsers.Cmdline
Parses configuration options from the command line.  Also creates help output when the program is run with a -h flag.

##### hconf.Subparsers.Cmdline.\_\_init\_\_
Command line parsers can accept an optional description argument, which will be used as the description for the program in the help output if it is run with a -h flag.

##### hconf.Subparsers.Cmdline.getArgumentParser
Command line parsers can optionally either be subclassed or have this function overridden to modify the argparse.ArgumentParser used to accept command-line arguments.  This function should accept two parameters, the first being the ConfigManager object the subparser is registered to, and the second being the Config object which has been constructed thus far.  It should return a single argument, being the argparse.ArgumentParser that the subparser should use to parse arguments from the command line.

Note that any arguments registered with underscores will have them converted to dashes when accepting commandline arguments.
For example, a configuration registered with the name `start_time` will be accepted from the command line as `--start-time`.
```
cmdlineSubparser = hconf.Subparsers.Cmdline("Program Description")
```

#### hconf.Subparsers.Dictionary
Subparser which accepts a python dictionary as an input and returns it.  Can be used to accept configuration options from external sources, like another process or from a socket.
```
dictionarySubparser = hconf.Subparsers.Dictionary(someDictionary)
```

#### hconf.Subparsers.INI
Subparser which parses configuration options from an .ini configuration file.  Arguments:
* sections - (Optional) A list of names of sections to parse.  Note that DEFAULT is not a valid section name as that section is always parsed.  If not passed all sections will be parsed.
* hconf.Subparsers.ConfigFileSubparser keyword arguments.  See below.
```
iniSubparser = hconf.Subparsers.INI(sections=['client'], filename='prog.cnf', filepath='/etc/prog/conf')
```

#### hconf.Subparsers.JSON
Subparser which accepts a JSON string (which when parsed must result in a dictionary) and returns the resulting dictionary.  Can be used to accept configuration options from external sources, like another process or from a socket.
```
jsonSubparser = hconf.Subparsers.JSON(someJSONString)
```

#### hconf.Subparsers.YAML
Subparser which parses configuration options from a .yaml/.yml configuration file. Arguments:
* hconf.Subparsers.ConfigFileSubparser keyword arguments.  See below.
```
yamlSubparser = hconf.Subparsers.YAML(filenameConfig='config-name', filepathConfig='config-path')
```

#### hconf.Subparsers.Subparser
Base class for subparsers.  Defines a single function, parse, which must be overridden.

#### hconf.Subparsers.ConfigFileSubparser
Convenience base class for subparsers which require the input of a configuration file to parse. Requires one of two pairs of keyword arguments to be passed to \_\_init\_\_:

* filepath: Either a list/tuple of the path tokens or a complete string to the directory which the configuration file resides in.
* filename: A string containing the name and extension of the configuration file to parse.

or

* filepathConfig: The name of a configuration option, the value of which will be acquired from the Config object and used as the path to the directory containing the configuration file to parse.
* filenameConfig: The name of a configuration option, the value of which will be acquired from the Config object and used as the name of the configuration file to parse.

Notes:
* If both filepath/filename and filepathConfig/filenameConfig are passed, filepath/filename will be used UNLESS the configuration options filepathConfig/filenameConfig are not None on the Config object.  In other words, filepath/filename acts as the default if filepathConfig/filenameConfig aren't passed.
* If filepathConfig/filenameConfig are used, the names they refer to must be registered as configuration objects in the ConfigManager as well.  Example:
```
iniSubparser = hconf.Subparsers.INI(filepathConfig='ini_conf_path', filenameConfig='ini_conf_name')
confMgr.addConfig('ini_conf_path')
conf<gr.addConfig('ini_conf_name')
```
