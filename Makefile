install:
	virtualenv -p python3.6 venv
	venv/bin/pip3 install -r requirements.txt

run:
	venv/bin/python3 -m server
