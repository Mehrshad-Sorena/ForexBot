
VENVDIR 	= .venv
PYTHON 		= .venv/bin/python
PIP 		= .venv/bin/pip
RUNNER 		= main.py


TESTDIR 		= tests
NOSETEST 		= .venv/bin/nosetests
NOSETEST_OPTS 		= -v
NOSETEST_TIMER_OPTS 	= --with-timer
NOSETEST_COVER_OPTS 	= --with-coverage --cover-html
CPROFILE_RESULT_PATH 	= result_profiling.txt


.PHONY: help init run unittest debug clean


help:
	@echo "Commands:"
	@echo ""
	@echo " 	- help 				show this help"
	@echo " 	- init 				install dependences"
	@echo " 	- run 				run project"
	@echo " 	- unittest 			run unit tests"
	@echo " 	- debug 			run project on debug mode"
	@echo " 	- clean 			clean cache"

update:
	$(PYTHON) -m pip install --upgrade pip

venv:
	test -d $(VENVDIR) || virtualenv -p python3 $(VENVDIR)

init: venv update
	$(PIP) install -Ur requirements.txt

run:
	$(PYTHON) $(RUNNER)

unittest:
	$(NOSETEST) $(NOSETEST_OPTS) $(NOSETEST_TIMER-OPTS) $(TESTDIR)

debug:
	$(PYTHON) -m pdb $(RUNNER)

clean_pyc:
	find . -name "*.pyc" | xargs -I {} rm -rfv "{}"

clean_pycache:
	find . -name "__pycache__" -type d | xargs -I {} rm -rfv "{}"

clean: clean_pyc clean_pycache
