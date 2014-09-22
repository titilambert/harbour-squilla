#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    __init__.py
#
#    This file is part of Squilla
#
#    Copyright (C) 2014 Thibault Cohen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#


__version__ = "0.2"
    
import sys
import os
import grp

embedded_libs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  '../embedded_libs/')
sys.path.append(embedded_libs_path)

#from squilla.application import Application
from squilla.libs.logger import logger


def main():
    """Initialize application."""
    global app
    try:
        os.setgid(grp.getgrnam("privileged").gr_gid)
    except Exception as e:
        logger.debug("Can't set privileged group: %s" % str(e))
    app = Application(interval=3)
    app.start()


def shutdown():
    global app
    app.stop()
