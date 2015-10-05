WD = $(shell pwd)

TMPVIRTENV=$(WD)/tmpvirtualenv

dev:
	@mkdir -p $(TMPVIRTENV)
	@pip3 install -t $(TMPVIRTENV) virtualenv
	@python3 $(TMPVIRTENV)/virtualenv.py $(WD)/env
	@env/bin/pip3 install virtualenv
	@env/bin/pip3 install -r requirements.txt
	@env/bin/pip3 install -r requirements-dev.txt
	@rm -rf $(TMPVIRTENV)
	@echo
	@echo
	@echo
	@echo source env/bin/activate
	@echo
	@echo

dev_clean:
	rm -rf $(WD)/env
	rm -rf $(WD)/tmpvirtualenv


dev_run:
	@env/bin/python3 server.py
