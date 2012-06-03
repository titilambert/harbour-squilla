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
    p=py2deb.Py2deb("heysms") #This is the package name and MUST be in lowercase! (using e.g. "mClock" fails miserably...)
    p.description="HeySms forwards sms to your Bonjour account. You can also answer by Bonjour."
    p.author="Thibault Cohen"
    p.mail="titilambert@gmail.com"
    p.depends = "python2.5, python-osso, libavahi-compat-libdnssd1, python2.5-qt4-network, python2.5-qt4-sql"
    p.section="user/utilities"
    p.icon = "images/heysms.png"
    p.arch="all"                #should be all for python, any for all arch
    p.urgency="low"             #not used in maemo onl for deb os
    p.distribution="fremantle-1.3"
    p.repository="extras-devel"
    p.xsbc_bugtracker="https://github.com/titilambert/HeySms"
    #  p.postinstall="""#!/bin/sh
    #  chmod +x /usr/bin/mclock.py""" #Set here your post install script
    #  p.postremove="""#!/bin/sh
    #  chmod +x /usr/bin/mclock.py""" #Set here your post remove script
    #  p.preinstall="""#!/bin/sh
    #  chmod +x /usr/bin/mclock.py""" #Set here your pre install script
    #  p.preremove="""#!/bin/sh
    #  chmod +x /usr/bin/mclock.py""" #Set here your pre remove script
    version = "1.0"           #Version of your software, e.g. "1.2.0" or "0.8.2"
    build = "1"                 #Build number, e.g. "1" for the first build of this version of your software. Increment for later re-builds of the same version of your software.
                             #Text with changelog information to be displayed in the package "Details" tab of the Maemo Application Manager
    changeloginformation = "First release" 
    dir_name = "src"            #Name of the subfolder containing your package source files (e.g. usr\share\icons\hicolor\scalable\myappicon.svg, usr\lib\myapp\somelib.py). We suggest to leave it named src in all projects and will refer to that in the wiki article on maemo.org
    #Thanks to DareTheHair from talk.maemo.org for this snippet that recursively builds the file list 
    for root, dirs, files in os.walk(dir_name):
     real_dir = root[len(dir_name):]
     fake_file = []
     for f in files:
         fake_file.append(root + os.sep + f + "|" + f)
     if len(fake_file) > 0:
         p[real_dir] = fake_file
    print p
    r = p.generate(version,build,changelog=changeloginformation,tar=True,dsc=True,changes=True,build=False,src=True)
