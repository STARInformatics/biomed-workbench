VENV?=venv
PYTHON3=/usr/bin/python3.7

venv:
	${PYTHON3} -m venv ${VENV}

install:
	${VENV}/bin/pip3 install -r requirements.txt

run:
	${VENV}/bin/python3 -m server

project_settings:
	@echo "Python3 binary to be used is '${PYTHON3}'"
	@echo "Python Virtual Environment specified to be located in the subdirectory '${VENV}'"