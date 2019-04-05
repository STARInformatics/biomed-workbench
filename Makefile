VENV?=venv

venv:
	python3 -m venv ${VENV}

install:
	${VENV}/bin/pip3 install -r requirements.txt

run:
	${VENV}/bin/python3 -m server

project_settings:
	@echo "Python Virtual Environment specified to be located in the subdirectory '${VENV}'"