EXES=multimode.py multimode_helper.py
THESTUFF=$(EXES) multimode.grc Makefile

install: multimode.py
	-mkdir -p $(HOME)/bin
	cp $(EXES) $(HOME)/bin
	@echo Please make sure your PYTHONPATH includes $(HOME)/bin
	@echo And also that PATH includes $(HOME)/bin
	@echo this will allow multimode to work correctly

multimode.py: multimode.grc
	grcc -d . multimode.grc

tarball:
	tar czvf multimode-$(VERSION).tar.gz $(THESTUFF)
