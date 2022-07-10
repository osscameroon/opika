.DEFAULT_GOAL=help

CONFIG_FILE=./.env
VENVPATH=venv
PYTHON=$(VENVPATH)/bin/python3

venv: $(VENVPATH)/bin/activate
$(VENVPATH)/bin/activate: requirements.txt
	test -d $(VENVPATH) || virtualenv -p python3 $(VENVPATH); \
	. $(VENVPATH)/bin/activate; \
	pip install -U pip; \
	pip install -r requirements.txt; \
	touch $(VENVPATH)/bin/activate;

$(CONFIG_FILE):
	echo "> Adding config file..."
	cp .env.example $(CONFIG_FILE)

##install-deps: setup your dev environment
install-deps: venv $(CONFIG_FILE)

install-dev-deps: install-deps $(CONFIG_FILE)
	$(PYTHON) -m pip install -r requirements-dev.txt

##run: run the api locally
run: install-deps
	sudo $(PYTHON) -m opika.main

lint: venv
	$(PYTHON) -m black opika
	$(PYTHON) -m isort opika
	$(PYTHON) -m flake8 opika --show-source --statistics

##test: test your code
test: install-deps lint
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENVPATH)

##help: show help
help : Makefile
	@sed -n 's/^##//p' $<

.PHONY : help venv install-deps test lint
