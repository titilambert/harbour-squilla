#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
#    lib/presence_browser.py
#
#    This file is part of Squilla
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


import socket
import sqlite3

from mdns.zeroconf import *
import mdns

from squilla.lib.logger import logger


# wlan0 needs
# devel-su
# iwpriv wlan0 setMCBCFilter 3
zeroconf = Zeroconf(("0.0.0.0", ))
zeroconf = Zeroconf(("192.168.13.15", ))

contacts_db_uri  = "file:/home/nemo/.local/share/system//privileged/Contacts/qtcontacts-sqlite/contacts.db?mode=ro"

contacts_by_numbers = {}
sqlite_opening_error = False

def search_contact_by_number(number):
    global sqlite_opening_error
    global contacts_by_numbers
    # return if we can't open contact database
    if sqlite_opening_error == True:
            return number.strip("+")

    logger.debug("Looking for contact name for number : %s" % number)
    if contacts_by_numbers == {}:
        logger.debug("Fetch contacts database")
        # queries
        contacts_query = "SELECT contactId, displayLabel FROM contacts"
        numbers_query = "SELECT phoneNumber, contactId FROM PhoneNumbers"
        # connection
        try:
            contacts_con = sqlite3.connect(contacts_db_uri, uri=True)
        except Exception as e:
            sqlite_opening_error = True
            logger.debug("Fetch contacts database error: %s" % e)
            return number.strip("+")
        contacts_cur = contacts_con.cursor()
        # get numbers
        contacts_cur.execute(numbers_query)
        raw_numbers = dict(contacts_cur.fetchall())
        # get contact names
        contacts_cur.execute(contacts_query)
        raw_contacts = dict(contacts_cur.fetchall())
        # close connection
        contacts_con.close()

        for num, contact_id in raw_numbers.items():
            if not contact_id in raw_contacts:
                continue
            contacts_by_numbers[num] =  raw_contacts[contact_id]

    contact_name = contacts_by_numbers.get(number, number)
    if contact_name != number:
        logger.debug("Contact name found: %s" % contact_name)
        return contact_name
    else:
        logger.debug("Contact name not found: %s" % contact_name)
        return number.strip("+")
