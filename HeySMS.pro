# NOTICE:
#
# Application name defined in TARGET has a corresponding QML filename.
# If name defined in TARGET is changed, the following needs to be done
# to match new name:
#   - corresponding QML filename must be changed
#   - desktop icon filename must be changed
#   - desktop filename must be changed
#   - icon definition filename in desktop file must be changed
#   - translation filenames have to be changed

# The name of your application
TARGET = HeySMS

CONFIG += sailfishapp

SOURCES += src/HeySMS.cpp

OTHER_FILES += qml/HeySMS.qml \
    qml/cover/CoverPage.qml \
    rpm/HeySMS.changes.in \
    rpm/HeySMS.spec \
    rpm/HeySMS.yaml \
    translations/*.ts \
    HeySMS.desktop \
    qml/pages/PreferencesPage.qml \
    qml/pages/MainPage.qml \
    friend_list.py

# to disable building translations every time, comment out the
# following CONFIG line
CONFIG += sailfishapp_i18n
TRANSLATIONS += translations/HeySMS-de.ts

