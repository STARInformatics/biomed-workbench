VENV?=venv

venv:
	virtualenv -p python3.6 ${VENV}

install:
	ls ${VENV} || virtualenv -p python3.6 ${VENV}
	${VENV}/bin/pip3 install -r requirements.txt

run:
	venv/bin/python3 -m backend

download:
	mkdir -p backend/data/diagrams
	mkdir -p backend/data/sbgn
	wget http://purl.obolibrary.org/obo/mondo.json -O backend/data/mondo.json
	wget https://reactome.org/download/current/diagrams.png.tgz -O backend/data/diagrams.png.tgz
	tar -xvzf backend/data/diagrams.png.tgz --directory backend/data/diagrams
	wget https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz -O backend/data/homo_sapiens.sbgn.tar.gz
	tar -xvzf backend/data/homo_sapiens.sbgn.tar.gz --directory backend/data/sbgn

run:
	${VENV}/bin/python3 -m backend

project_settings:
	@echo "Python Virtual Environment specified to be located in the subdirectory '${VENV}'"
