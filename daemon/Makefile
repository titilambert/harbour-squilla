# -*- coding: us-ascii-unix -*-

name       = harbour-squilla-daemon
version    = 0.3
DESTDIR    =
PREFIX     = /usr/local
datadir    = $(DESTDIR)$(PREFIX)/share/$(name)
desktopdir = $(DESTDIR)$(PREFIX)/share/applications
icondir    = $(DESTDIR)$(PREFIX)/share/icons/hicolor/86x86/apps

.PHONY: clean dist install rpm

clean:
	rm -rf dist 
	rm -rf squilla/__pycache__
	rm -rf squilla/*.pyc
	rm -rf squilla/libs/__pycache__
	rm -rf squilla/libs/*.pyc
	rm -f rpm/*.rpm
	find embedded_libs -name  "__pycache__" -exec rm -rf {} \;
	find embedded_libs -name  "*.pyc" -exec rm -rf {} \;

dist:
	$(MAKE) clean
	mkdir -p dist/$(name)-$(version)
	cp -r `cat MANIFEST` dist/$(name)-$(version)
	rm -rf dist/$(name)-$(version)/modules
	tar -C dist -czf dist/$(name)-$(version).tar.gz $(name)-$(version)

install:
	@echo "Installing Python files..."
	mkdir -p $(datadir)/squilla/
	mkdir -p $(datadir)/embedded_libs
	cp -r squilla/* $(datadir)/squilla/
	rm -rf $(datadir)/squilla/modules
	cp -r embedded_libs/* $(datadir)/embedded_libs/
	cp -r run_squilla_daemon.py $(datadir)/

rpm:
	mkdir -p $$HOME/rpmbuild/SOURCES
	cp dist/$(name)-$(version).tar.gz $$HOME/rpmbuild/SOURCES
	rpmbuild -ba rpm/$(name).spec
	cp $$HOME/rpmbuild/RPMS/armv7hl/$(name)-$(version)-*.rpm rpm
	#cp $$HOME/rpmbuild/RPMS/noarch/$(name)-$(version)-*.rpm rpm
	cp $$HOME/rpmbuild/SRPMS/$(name)-$(version)-*.rpm rpm
