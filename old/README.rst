=======================
Presentation of Squilla
=======================

**This is the port of HeySMS on Sailfish OS**

I made a small application to send and receive sms on your computer without a specific software.
You just have to use your instant messaging client ... Which have to be compatible with Bonjour protocol.

I made this application because my girlfriend send me a lot of SMS when I'm working ...
Now I can answer her without taking my Jolla ... 

Feature list
============
* Send SMS from your computer (using your bonjour client) - DONE
* Receive SMS on your computer (using your bonjour client) - DONE
* Silent your phone when Squilla starts - DONE
* Use Smssend to send SMS. Usefull if you can't send Sms wih standard method. (You need to install smssend package) - DELETED (useless on Sailfish OS)
* Connect your phone to your computer using the USB cable - DONE
* Connect your phone to your computer using Wifi - NOT STARTED (root rights seem needed ...)
* Bonjour Bot to control your phone (called 'Controller') - NOT STARTED
* Controller will notify you if someone call you (Usefull, if your Jolla is in silent mode) - NOT STARTED
* Set contact as favorite... This contact will appears in your active contact list at starting... - DONE
* All your messages/answers are stored in your conversation history... - NOT STARTED

Controller fonctions (NOT IMPLEMENTED)
--------------------
* help : Show help
* show : Show current active contact list
* search : Search a contact in your address book in order to add a contact in your Bonjour contact list
* add : Add contact to active contact list
* del : Remove contact from active contact list
* echo : Just reply your message ...
* If you have any idea ???

Mini manual
==========

1. Launch Squilla on your Jolla
2. Launch your instant messaging client on your computer and activate your Bonjour account.
3. In Squilla select yourself (your Bonjour name) in the Bonjour contact list.
4. If you are not in the Bonjour contact list, click on reload button ...
5. Add contact in your active contact list (Menu -> "Add friend")
6. You will see your friend in the active contact list
7. Your friend will appears in your Bonjour client on your computer
8. Write message to your friend (in fact, it send SMS...)
9. .... Wait answer ....
10. Receive SMS ...
11. The message appears on your computer !
12. Answer ...

Of course, only the selected bonjour contact can send/receive SMS from/to your phone... 
Also, all your answers will be store in the Jolla history. You will not lost your messages ! (NOT YET)

Tested with
===========
* Jolla and Pidgin (on Linux)
* Jolla and Gajim (on Linux)
* Please talk about you 

Limitations
===========
* If you use Wifi, your Jolla and your computer must be on the same network (subnet)
* Sailfish OS

Updates
=======
* 0.1-1: First alpha release

Roadmap 
=======
* Improve USB network activation stability
* Add Wifi connectivity
* Add the Controller
* Translations
* A really logo ?
* .... ???
* Call forwarding using PulseAudio forwarding ??? ( maybe in version 15 )

Usefull links
=============
* You can download `HERE`__
* Source code : `HERE`__
* You can submit ideas and bugs `HERE`__
* Thanks to benny1967 : `Post on HeySMS`__
* Thakns to Stefan Siegl : `An other post on HeySMS`__

__ https://openrepos.net/content/titilambert/squilla
__ https://github.com/titilambert/harbour-squilla
__ https://github.com/titilambert/harbour-squilla/issues
__ http://translate.google.com/translate?hl=en&sl=de&u=http://oskar.twoday.net/stories/97052244/&prev=/search%3Fq%3D%2522heysms%2522%26start%3D10%26hl%3Den%26safe%3Doff%26client%3Dopera%26hs%3DyqG%26sa%3DN%26channel%3Dsuggest%26biw%3D1698%26bih%3D1092%26prmd%3Dimvns&sa=X&ei=9eVEUNE2zfToAf3NgfgE&ved=0CC0Q7gEwAjgK
__ http://stesie.github.io/2012/10/heysms/
