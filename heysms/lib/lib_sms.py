#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    lib_sms.py
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

# See:
# http://ztbsauer.com/sender.py
# http://borunov.ural.ru/sender.py

from lib import logger

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


def octify(str):
        '''
        Returns a list of octet bytes representing
        each char of the input str.
        '''
        try:
            bytes = map(GSM_DEFAULT_ALPHABET.index, str)
            bytes = [b if b != 27 else 32 for b in bytes]
        except ValueError, e:
            bytes = map(ord, str)

        bitsconsumed = 0
        referencebit = 7
        octets = []

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
                    octets.append(byte | bitstocopy)
                    bitsconsumed += 1
                    referencebit -= 1
                else:
                    bitsconsumed = 0
                    referencebit = 7

        return octets


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
    #prepare for accentd
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

    number_length = len(number)
    if (numlength % 2) == 0:
            rangelength = numlength
    else:
            number = number + 'F'
            rangelength = len(number)

    octifiednumber = [semi_octify(number[i:i + 2])
                      for i in range(0, rangelength, 2)]

    msg_length = len(msg)*2
    PDU_TYPE = 0x11 
    MR = 0

    pdu_message = [PDU_TYPE, MR, number_length, ADDR_TYPE]
    pdu_message.extend(octifiednumber)

    pdu_message.append(0) #PID
    pdu_message.append(8) #DCS

    pdu_message.append(167) #VP 24 hours

    pdu_message.append(msg_length)

    for i in xrange (len(msg)) :
        digit = ord(msg[i])
        h_digit = digit >> 8
        l_digit = digit & 0xFF
        pdu_message.append(h_digit)
        pdu_message.append(l_digit)

    logger.debug("Sent pdu: %s" % pdu_message)

    return pdu_message
