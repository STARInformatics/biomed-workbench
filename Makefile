VENV?=venv

venv:
	virtualenv -p python3.6 ${VENV}

install:
	${VENV}/bin/pip3 install -r requirements.txt

run:
	${VENV}/bin/python3 -m server

echo:
	@echo "Virtual Environment specified in subfolder '${VENV}'"