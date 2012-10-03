#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    lib_sms.py
#
#    This file is part of HeySms
#
#    Copyright (C) 2012 Thibault Cohen
#    Copyright (C) 2012 Stefan Siegl <stesie@brokenpipe.de>
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

# See:
# http://ztbsauer.com/sender.py
# http://borunov.ural.ru/sender.py

from lib import logger
from math import ceil
from random import randint
from copy import copy

GSM_DEFAULT_ALPHABET = [
    u"@",
    u"\u00a3",
    u"$",
    u"\u00a5",
    u"\u00e8",
    u"\u00e9",
    u"\u00f9",
    u"\u00ec",
    u"\u00f2",
    u"\u00c7",
    u"\n",
    u"\u00d8",
    u"\u00f8",
    u"\r",
    u"\u00c5",
    u"\u00e5",

    u"\u0394",
    u"_",
    u"\u03a6",
    u"\u0393",
    u"\u039b",
    u"\u03a9",
    u"\u03a0",
    u"\u03a8",
    u"\u03a3",
    u"\u0398",
    u"\u039e",
    u" ",
    u"\u00c6",
    u"\u00e6",
    u"\u00df",
    u"\u00c9",

    u" ",
    u"!",
    u"\"",
    u"#",
    u"\u00a4",
    u"%",
    u"&",
    u"'",
    u"(",
    u")",
    u"*",
    u"+",
    u",",
    u"-",
    u".",
    u"/",

    u"0",
    u"1",
    u"2",
    u"3",
    u"4",
    u"5",
    u"6",
    u"7",
    u"8",
    u"9",
    u":",
    u";",
    u"<",
    u"=",
    u">",
    u"?",

    u"\u00a1",
    u"A",
    u"B",
    u"C",
    u"D",
    u"E",
    u"F",
    u"G",
    u"H",
    u"I",
    u"J",
    u"K",
    u"L",
    u"M",
    u"N",
    u"O",

    u"P",
    u"Q",
    u"R",
    u"S",
    u"T",
    u"U",
    u"V",
    u"W",
    u"X",
    u"Y",
    u"Z",
    u"\u00c4",
    u"\u00d6",
    u"\u00d1",
    u"\u00dc",
    u"\u00a7",

    u"\u00bf",
    u"a",
    u"b",
    u"c",
    u"d",
    u"e",
    u"f",
    u"g",
    u"h",
    u"i",
    u"j",
    u"k",
    u"l",
    u"m",
    u"n",
    u"o",

    u"p",
    u"q",
    u"r",
    u"s",
    u"t",
    u"u",
    u"v",
    u"w",
    u"x",
    u"y",
    u"z",
    u"\u00e4",
    u"\u00f6",
    u"\u00f1",
    u"\u00fc",
    u"\u00e0"
]


def _decode_default_alphabet(s):
    # ought to be all in the 7 bit GSM character map
    # modem is in 8 bit mode, so it makes 7 bit unpacking itself
    chars = [GSM_DEFAULT_ALPHABET[ord(c)] for c in s]
    u_str = "".join(chars)
    return u_str.encode("utf-8")


def octify(str, shift):
        '''
        Returns a list of octet bytes representing
        each char of the input str.
        '''
        bytes = map(GSM_DEFAULT_ALPHABET.index, str)
        bytes = [b if b != 27 else 32 for b in bytes]

        bitsconsumed = 0
        referencebit = 7
        octets = []

        for i in xrange(shift):
                bytes.insert(0, 0)

        while len(bytes):
                byte = bytes.pop(0)
                byte = byte >> bitsconsumed
                try:
                    nextbyte = bytes[0]
                    bitstocopy = (nextbyte &
                                  (0xff >> referencebit)) << referencebit
                    octet = (byte | bitstocopy)
                except:
                    octet = (byte | 0x00)

                if bitsconsumed != 7:
                    octets.append(octet)
                    bitsconsumed += 1
                    referencebit -= 1
                else:
                    bitsconsumed = 0
                    referencebit = 7

        return octets[shift - shift / 7:]


def semi_octify(str):
        '''
        Expects a string containing two digits.
        Returns an octet -
        first nibble in the octect is the first
        digit and the second nibble represents
        the second digit.
        '''
        try:
            digit_1 = int(str[0])
            digit_2 = int(str[1])
            octet = (digit_2 << 4) | digit_1
        except:
            octet = (1 << 4) | digit_1

        return octet


def deoctify(arr):
        referencebit = 1
        doctect = []
        bnext = 0x00

        for i in arr:

                bcurr = ((i & (0xff >> referencebit)) << referencebit) >> 1
                bcurr = bcurr | bnext

                if referencebit != 7:
                        doctect.append(bcurr)
                        bnext = (i & (0xff <<
                                      (8 - referencebit))) >> 8 - referencebit
                        referencebit += 1
                else:
                        doctect.append(bcurr)
                        bnext = (i & (0xff <<
                                      (8 - referencebit))) >> 8 - referencebit
                        doctect.append(bnext)
                        bnext = 0x00
                        referencebit = 1

        doctect = ''.join([chr(i) for i in doctect])
        return _decode_default_alphabet(doctect).decode('utf-8')

def deoctify_int(arr):
    
    doctect = [h * 256 + l for h, l in zip(arr[::2], arr[1::2])]

    doctect = ''.join([unichr(i) for i in doctect])
    return doctect


def createPDUmessage(number, msg):
    '''
    Returns a list of bytes to represent a valid PDU message
    '''

    # Convert to Python Unicode string (prepare for accentd)
    msg = msg.decode('utf-8')

    # Unknown type, works with 514 xxx xxxx, 1 514 xxx xxxx
    #ADDR_TYPE = 0x80
    # Local works with 1 514 xxx xxxx
    #ADDR_TYPE = 0xA8
    # ???????, works with 514 xxx xxxx, 1 514 xxx xxxx
    ADDR_TYPE = 0x81
    if number.startswith("+"):
        ADDR_TYPE = 0x91
        number = number[1:]

    numlength = len(number)
    if (numlength % 2):
            number = number + 'F'

    octifiednumber = [semi_octify(number[i:i + 2])
                      for i in range(0, len(number), 2)]

    PDU_TYPE = 0x11 
    MR = 0

    # Test whether message can be represented in GSM-7 alphabet
    try:
        map(GSM_DEFAULT_ALPHABET.index, msg)
        DCS = 0     # yes it can
        need_chunking = len(msg) > 160
        chunksize = 153

    except ValueError:
        # Message cannot be represented using GSM alphabet, use UCS-2
        DCS = 8
        need_chunking = len(msg) > 70
        chunksize = 67

    if need_chunking:
        logger.debug("Message too long for one SMS")
        PDU_TYPE |= 0x40
        chunks = int(ceil(1.0 * len(msg) / chunksize))
        ref = randint(0, 255)
    else:
        chunks = 1

    pdu_template = [PDU_TYPE, MR, numlength, ADDR_TYPE]
    pdu_template.extend(octifiednumber)

    pdu_template.append(0) #PID
    pdu_template.append(DCS) #DCS

    pdu_template.append(167) #VP 24 hours

    pdus = []

    for chunk in xrange(chunks):
        pdu_message = copy(pdu_template)

        if PDU_TYPE & 0x40:
            part = msg[chunk * chunksize : (chunk + 1) * chunksize]

            if DCS & 0x08:
                # UCS-2 encoding, hence UDL in octets
                pdu_message.append(6 + 2 * len(part))
            else:
                # GSM-7 encoding, UDL in septets
                pdu_message.append(7 + len(part))

            # concatenated SMS header
            pdu_message.append(5)   # UDH length
            pdu_message.append(0)   # concat sms, 8-bit ref
            pdu_message.append(3)   # concat sms header length
            pdu_message.append(ref)
            pdu_message.append(chunks)
            pdu_message.append(1 + chunk)
        else:
            part = msg

            if DCS & 0x08:
                # UCS-2 encoding, hence UDL in octets (2 bytes per char)
                pdu_message.append(2 * len(part))
            else:
                # GSM-7 encoding, UDL in septets
                pdu_message.append(len(part))


        if DCS & 0x08:  # UCS-2 encoding
            for i in xrange (len(msg)) :
                digit = ord(msg[i])
                pdu_message.append(digit >> 8)
                pdu_message.append(digit & 0xFF)

        else:  # GSM-7 encoding
            pdu_message.extend(octify(part, 7 if PDU_TYPE & 0x40 else 0))

        pdus.append(pdu_message)

    return pdus
