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

import setuptools

VERSION = "0.0.1"
NAME = "hconf"

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="A hierarchical configuration manager for parsing configurations from multiple sources.",
    author="Warren Spencer",
    author_email="warrenspencer27@gmail.com",
    url="https://github.com/warrenspe/%s" % NAME,
    download_url="https://github.com/warrenspe/%s/tarball/%s" % (NAME, VERSION),
    keywords=['configuration', 'config', 'hierarchical', 'cascade'],
    classifiers=[],
    packages=[NAME] + ["%s.%s" % (NAME, pkg) for pkg in setuptools.find_packages(NAME)],
    license="https://www.gnu.org/licenses/gpl-3.0.html",
    platforms=["Linux", "Windows"],

    install_requires=[
        'PyYAML',
    ]
)
