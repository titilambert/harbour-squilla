======================
Presentation of HeySms
======================

I made a small application to send and receive sms on your computer without a specific software.
You just have to use your instant messaging client ... Which have to be compatible with Bonjour protocol.

I made this application because my girlfriend send me a lot of sms when I'm working ...
Now I can answer her without taking my N900 ... 

Feature list
============
* Send SMS from your computer (using your bonjour client)
* Receive SMS on your computer (using your bonjour client)
* Silent your phone when HeySms starts
* Use Smssend to send SMS. Usefull if you can't send Sms wih standard method. (You need to install smssend package)
* Connect your phone to your computer using the USB cable
* Bonjour Bot to control your phone (called 'Controller')
* Controller will notify you if someone call you (Usefull, if your N900 is in silent mode)
* Set contact as favorite... This contact will appears in your active contact list at starting ...
* All your messages/answers are stored in your conversation history... 

Controller fonctions
--------------------
* help : Show help
* show : Show current active contact list
* search : Search a contact in your address book in order to add a contact in your Bonjour contact list
* add : Add contact to active contact list
* del : Remove contact from active contact list
* echo : Just reply your message ...
* If you have any idea ... I can do it !!!

Mini manual
==========
1 - Launch your instant messaging client on your computer and activate your Bonjour account.

2 - Launch HeySms on your N900

3 - In HeySms select yourself (your Bonjour name) in the Bonjour contact list.

4 - If you are not in the Bonjour contact list, click on reload button ...

5 - Add contact in your active contact list (Menu -> "Add friend")

6 - You will see your friend in the active contact list

7 - Your friend will appears in your Bonjour client on your computer

8 - Write message to your friend (in fact, it send SMS...)

9 - .... Wait answer ....

10 - Receive SMS ...

11 - The message appears on your computer !

12 - Answer ...

Of course, only the selected bonjour contact can send/receive SMS from/to your phone... 

Also, all your answers will be store in the N900 history. You will not lost your messages ! 

Tested with
===========
* N900 and Pidgin (on Linux)
* N900 and Empathy (on Linux)
* N900 and Kopete (on Linux)
* N900 and Gajim (on Linux)
* Please talk about you 

Limitations
===========
* If you use Wifi, your N900 and your computer must be on the same network (subnet)
* N900 only (If I get N950 or N9, I port it !)

Updates
=======
* 1.6.4-1 : Fix call notifier
* 1.6.3-1 : Fix search contact (Thanks to darodi)
* 1.6.2-1 : Fix Controller stability
* 1.6.1-1 : Fix stability
* 1.6.0-1 : Add controller. You can now control your N900 using Bonjour
* 1.5.1-1 : Cleaning code
* 1.5.0-1 : Add option to use USB PC connection
* 1.4.5-1 : Fix minor bugs

Roadmap 
=======
* Clean bonjour client code (use XMPPPY ???)
* Improve USB network activation stability
* Port to N9/N950
* Silent phone using the Controller
* Add preference to don't show Yellow Popups
* Translations
* .... ???
* Call forwarding using jingle library ???  ( maybe in version 42 )

Usefull links
=============
* You can download `HERE`__
* Source code : `HERE`__
* You can submit ideas and bugs `HERE`__
* Thanks to benny1967 : `Post on HeySms`__

__ http://maemo.org/downloads/product/Maemo5/heysms/
__ https://github.com/titilambert/HeySms/
__ https://github.com/titilambert/HeySms/issues
__ http://translate.google.com/translate?hl=en&sl=de&u=http://oskar.twoday.net/stories/97052244/&prev=/search%3Fq%3D%2522heysms%2522%26start%3D10%26hl%3Den%26safe%3Doff%26client%3Dopera%26hs%3DyqG%26sa%3DN%26channel%3Dsuggest%26biw%3D1698%26bih%3D1092%26prmd%3Dimvns&sa=X&ei=9eVEUNE2zfToAf3NgfgE&ved=0CC0Q7gEwAjgK
