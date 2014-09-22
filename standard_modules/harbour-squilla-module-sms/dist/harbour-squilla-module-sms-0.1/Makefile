# -*- coding: us-ascii-unix -*-

name       = harbour-squilla-module-sms
version    = 0.1
DESTDIR    =
PREFIX     = /usr/local
datadir    = $(DESTDIR)$(PREFIX)/share/harbour-squilla-daemon/squilla/modules/$(name)

.PHONY: clean dist install rpm

clean:
	rm -rf dist 
	rm -f rpm/*.rpm
	find module -name  "__pycache__" -exec rm -rf {} \;
	find module -name  "*.pyc" -exec rm -rf {} \;

dist:
	$(MAKE) clean
	mkdir -p dist/$(name)-$(version)
	cp -r `cat MANIFEST` dist/$(name)-$(version)
	tar -C dist -czf dist/$(name)-$(version).tar.gz $(name)-$(version)

install:
	@echo "Installing Python files..."
	mkdir -p $(datadir)/
	cp -r module/* $(datadir)/

rpm:
	mkdir -p $$HOME/rpmbuild/SOURCES
	cp dist/$(name)-$(version).tar.gz $$HOME/rpmbuild/SOURCES
	rpmbuild -ba rpm/$(name).spec
	cp $$HOME/rpmbuild/RPMS/armv7hl/$(name)-$(version)-*.rpm rpm
	#cp $$HOME/rpmbuild/RPMS/noarch/$(name)-$(version)-*.rpm rpm
	cp $$HOME/rpmbuild/SRPMS/$(name)-$(version)-*.rpm rpm
