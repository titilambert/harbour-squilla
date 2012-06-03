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
    chars = [ GSM_DEFAULT_ALPHABET[ord(c)] for c in s ]
    u_str = "".join(chars)
    return u_str.encode("utf-8")

def octify(str):
        '''     
        Returns a list of octet bytes representing
        each char of the input str.               
        '''
        try:
            bytes = map(GSM_DEFAULT_ALPHABET.index, str)
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
                        bitstocopy = (nextbyte & (0xff >> referencebit)) << referencebit
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
                        doctect.append( bcurr )
                        bnext = (i & (0xff << (8 - referencebit)) ) >> 8 - referencebit
                        referencebit += 1
                else:
                        doctect.append( bcurr )
                        bnext = (i & (0xff << (8 - referencebit)) ) >> 8 - referencebit
                        doctect.append( bnext )
                        bnext = 0x00
                        referencebit = 1

        return _decode_default_alphabet(''.join([chr(i) for i in doctect])).decode('utf-8')

def createPDUmessage(number, msg):
        '''                       
        Returns a list of bytes to represent a valid PDU message
        '''
        #prepare for accentd
        msg = msg.decode('utf-8')
        
        numlength = len(number)
        if (numlength % 2) == 0:
                rangelength = numlength
        else:
                number = number + 'F'
                rangelength = len(number)

        octifiednumber = [ semi_octify(number[i:i+2]) for i in range(0,rangelength,2) ]
        octifiedmsg = octify(msg)
        HEADER = 1
        FIRSTOCTETOFSMSDELIVERMSG = 10
        ADDR_TYPE = 129 #unknown format                                                
        number_length = len(number)
        msg_length = len(msg)
        pdu_message = [HEADER, FIRSTOCTETOFSMSDELIVERMSG, number_length, ADDR_TYPE]
        pdu_message.extend(octifiednumber)
        pdu_message.append(0)
        pdu_message.append(0)
        pdu_message.append(msg_length)
        pdu_message.extend(octifiedmsg)
        return pdu_message


