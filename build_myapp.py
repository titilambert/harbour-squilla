#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    build_myapp.py
#
#    This file is part of HeySms
#
#    Copyright (C) 2012 Thibault Cohen
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


import py2deb
import os


if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass
    print

    p = py2deb.Py2deb("heysms")
    p.description = ("HeySms forwards sms to your Bonjour account. You can "
                    "also answer by Bonjour.")
    p.author = "Thibault Cohen"
    p.mail = "titilambert@gmail.com"
    p.depends = ("python2.5, python-osso, libavahi-compat-libdnssd1, "
                "python2.5-qt4-network, python2.5-qt4-sql")
    p.section = "user/utilities"
    p.icon = "images/heysms.png"
    p.arch = "all"
    p.urgency = "low"
    p.distribution = "fremantle-1.3"
    p.repository = "extras-devel"
    p.xsbc_bugtracker = "https://github.com/titilambert/HeySms"
    version = "1.0"
    build = "1"
    changeloginformation = "First release"
    dir_name = "src"
    for root, dirs, files in os.walk(dir_name):
        real_dir = root[len(dir_name):]
        fake_file = []
        for f in files:
            fake_file.append(root + os.sep + f + "|" + f)
        if len(fake_file) > 0:
            p[real_dir] = fake_file
    print p
    r = p.generate(version, build, changelog=changeloginformation, tar=True,
                   dsc=True, changes=True, build=False, src=True)
