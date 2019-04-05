VENV?=venv

venv:
	python -m venv ${VENV}

install:
	${VENV}/bin/pip3 install -r requirements.txt

run:
	${VENV}/bin/python3 -m server

parameters:
	@echo "Virtual Environment specified in subfolder '${VENV}'"