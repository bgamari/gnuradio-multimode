install:
	-mkdir -p $(HOME)/bin
	cp multimode.py multimode_helper.py $(HOME)/bin
	@echo Please make sure your PYTHONPATH includes $(HOME)/bin
	@echo And also that PATH includes $(HOME)/bin
	@echo this will allow multimode to work correctly
	
	
