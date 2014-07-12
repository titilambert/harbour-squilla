# -*- coding: us-ascii-unix -*-

name       = harbour-squilla
version    = 0.1
DESTDIR    =
PREFIX     = /usr/local
datadir    = $(DESTDIR)$(PREFIX)/share/$(name)
desktopdir = $(DESTDIR)$(PREFIX)/share/applications
icondir    = $(DESTDIR)$(PREFIX)/share/icons/hicolor/86x86/apps

.PHONY: clean dist install rpm

clean:
	rm -rf dist 
	rm -rf squilla/__pycache__
	rm -rf squilla/lib/__pycache__
	rm -rf embedded_libs/bs4/__pycache__
	rm -rf embedded_libs/bs4/builder/__pycache__
	rm -rf embedded_libs/mdns/__pycache__
	rm -rf embedded_libs/dbus/__pycache__
	rm -rf embedded_libs/dbus/mainloop/__pycache__
	rm -f rpm/*.rpm

dist:
	$(MAKE) clean
	mkdir -p dist/$(name)-$(version)
	cp -r `cat MANIFEST` dist/$(name)-$(version)
	tar -C dist -czf dist/$(name)-$(version).tar.gz $(name)-$(version)

install:
	@echo "Installing Python files..."
	mkdir -p $(datadir)/squilla/lib
	cp squilla/*.py $(datadir)/squilla
	cp squilla/lib/*.py $(datadir)/squilla/lib
	cp -r embedded_libs $(datadir)/
	@echo "Installing QML files..."
	mkdir -p $(datadir)/qml/icons
	cp qml/Squilla.qml $(datadir)/qml/$(name).qml
	cp -r qml/* $(datadir)/qml
	@echo "Installing desktop file..."
	mkdir -p $(desktopdir)
	cp data/$(name).desktop $(desktopdir)
	@echo "Installing icon..."
	mkdir -p $(icondir)
	cp data/harbour-squilla.png $(icondir)/$(name).png
	cp data/harbour-squilla.png $(datadir)/qml/

rpm:
	mkdir -p $$HOME/rpmbuild/SOURCES
	cp dist/$(name)-$(version).tar.gz $$HOME/rpmbuild/SOURCES
	rpmbuild -ba rpm/$(name).spec
	cp $$HOME/rpmbuild/RPMS/armv7hl/$(name)-$(version)-*.rpm rpm
	#cp $$HOME/rpmbuild/RPMS/noarch/$(name)-$(version)-*.rpm rpm
	cp $$HOME/rpmbuild/SRPMS/$(name)-$(version)-*.rpm rpm
