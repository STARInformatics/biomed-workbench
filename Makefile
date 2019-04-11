VENV?=venv
BKW_BASE_URL?=http://localhost:5000
BKW_API_PATH?=

venv:
	virtualenv -p python3.6 ${VENV}

install:
	#
	# Configure Python Flask back end
	#
	ls ${VENV} || virtualenv -p python3.6 ${VENV}
	${VENV}/bin/pip3 install -r requirements.txt
	#
	# Configure node.js web application
	#
	cd frontend; npm install

data:
	mkdir -p backend/data/diagrams
	mkdir -p backend/data/sbgn
	wget http://purl.obolibrary.org/obo/mondo.json -O backend/data/mondo.json
	wget https://reactome.org/download/current/diagrams.png.tgz -O backend/data/diagrams.png.tgz
	tar -xvzf backend/data/diagrams.png.tgz --directory backend/data/diagrams
	wget https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz -O backend/data/homo_sapiens.sbgn.tar.gz
	tar -xvzf backend/data/homo_sapiens.sbgn.tar.gz --directory backend/data/sbgn

.PHONY: web

service:
	nohup ${VENV}/bin/python3 -m backend >logs/service_`date`.log 2>&1 &

web:
	cd frontend; \
      nohup \
      BKW_BASE_URL=${BKW_BASE_URL} \
      BKW_API_PATH=${BKW_API_PATH} \
      npm start >../logs/web_`date`.log 2>&1 &

project_settings:
	@echo "Python Virtual Environment specified to be located in the subdirectory '${VENV}'"
