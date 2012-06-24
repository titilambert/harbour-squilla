#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# HeySms
 
import sys
reload(sys).setdefaultencoding("UTF-8")
 
try:
    from sdist_maemo import sdist_maemo as _sdist_maemo
except:
    _sdist_maemo = None
    print 'sdist_maemo command not available'
 
from distutils.core import setup

import heysms.heysms
 
#Remove pyc and pyo file
import glob
import os
for fpath in glob.glob('*/*.py[c|o]'):
    os.remove(fpath)

for fpath in glob.glob('*/*/*.py[c|o]'):
    os.remove(fpath)
 
changes = ' Fix manage profile option'
 
setup(name='heysms',
      version='1.3.2',
      license='GNU GPLv2',
      description="HeySms forwards sms to your Bonjour account.",
      long_description="HeySms forwards sms to your Bonjour account. You can also answer by Bonjour.",
      author='Thibault Cohen',
      author_email='titilambert@gmail.com',
      maintainer=u'Thibault Cohen',
      maintainer_email='titilambert@gmail.com',
#      requires=('libavahi-compat-libdnssd1', 'python2.5-qt4-network',
#                'python2.5-qt4-sql', 'python2.5', 'python-osso'),
      url='https://github.com/titilambert/HeySms',
      packages= ['heysms', 'heysms.lib', 'heysms.lib.avahi'],
      package_data = {'heysms': ['images/*.png']},
      data_files=[('/usr/share/applications/hildon/', ['heysms.desktop']),
                  ('/usr/share/pixmaps', ['images/heysms.png', 'images/heysms_64.png', 'images/heysms_32.png']),
                  ('/usr/share/icons/hicolor/128x128/apps', ['images/heysms.png']),
                  ('/usr/share/icons/hicolor/64x64/apps', ['images/heysms_64.png']),
                  ('/usr/share/icons/hicolor/32x32/apps', ['images/heysms_32.png']),
                  ('/usr/share/icons/hicolor/32x32/apps', ['images/favorite.png']),
                  ('/usr/share/icons/hicolor/32x32/apps', ['images/non-favorite.png']),
                ],
      scripts=['scripts/heysms'],
      classifiers=[
        "Development Status :: 1 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: Other",
        "Operating System :: Other OS",
        "Intended Audience :: End Users/Desktop",],
      cmdclass={'sdist_maemo': _sdist_maemo},
      options = { 'sdist_maemo':{
        'debian_package':'heysms',
        'buildversion': '1',
        'depends': "python2.5, python-osso, libavahi-compat-libdnssd1, python2.5-qt4-network, python2.5-qt4-sql, avahi-daemon",
        'conflicts': '',
        'Maemo_Bugtracker': 'https://github.com/titilambert/HeySms',
        'Maemo_Display_Name': 'HeySms',
        'Maemo_Icon_26': 'heysms.png',
        'Maemo_Upgrade_Description': '%s' % changes,
        'section': 'user/network',
        'changelog': changes,
        'architecture': 'any',
        'postinst': """""",
        'prere': """""",
        'copyright': 'gpl'},
        'bdist_rpm': {
            'requires': "python2.5, python-osso, libavahi-compat-libdnssd1,python2.5-qt4-network, python2.5-qt4-sql, avahi-daemon",
            'conflicts': '',
            'icon': 'images/heysms.png',
            'group': 'Network',}
        }
     )
