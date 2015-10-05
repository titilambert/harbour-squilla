#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools


# Better to use exec to load the VERSION from alignak/bin/__init__
# so to not have to import the alignak package:
VERSION = "unknown"
ver_file = os.path.join('squilla', 'version.py')
with open(ver_file) as fh:
    exec(fh.read())

os.environ['PBR_VERSION'] = VERSION


setuptools.setup(
    setup_requires=['pbr'],
    version=VERSION,
    packages=['squilla', 'squilla.modules'],
    namespace_packages=['squilla', 'squilla.modules'],
    pbr=True,
)
