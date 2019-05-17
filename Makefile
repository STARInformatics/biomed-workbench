VENV?=venv
PYTHON3_PATH?=${VENV}/bin/python3
PIP3_PATH?=${VENV}/bin/pip3

install:
	#
	# Configure Python Flask back end
	#
	${PIP3_PATH} install -r requirements.txt
	#
	# Configure node.js web application
	#
	cd frontend; cp template.env .env; npm install; npm audit fix

data:
	mkdir -p backend/data/diagrams
	mkdir -p backend/data/sbgn
	# download data
	cd backend/data ; \
	    wget https://github.com/monarch-initiative/mondo/releases/download/current/mondo.json ; \
	    curl -O https://reactome.org/download/current/diagrams.png.tgz ; \
	    tar -xvzf diagrams.png.tgz --directory diagrams ; \
	    curl -O https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz ; \
	    tar -xvzf homo_sapiens.sbgn.tar.gz --directory sbgn
	# Preprocess data
	python scripts/build_id_mapping_csv.py -o backend/data/id_mapping.csv
	python scripts/fix_sbgn.py

.PHONY: web venv

service:
	nohup ${PYTHON3_PATH} -m backend >logs/service_`date`.log 2>&1 &

web:
	cd frontend; nohup npm start >../logs/web_`date`.log 2>&1 &

project_settings:
	@echo "Python Virtual Environment (VENV) specified to be located in the subdirectory '${VENV}'"
	@echo "Path to python3 ('PYTHON3_PATH') is specified to be located at path '${PYTHON3_PATH}'"
	@echo "Path to pip3 ('PIP3_PATH') is specified to be located at path '${PIP3_PATH}'"
	@echo "Override the these environment variables as needed, according to your site installation particulars"

start:
	make start-backend
	make start-workflow
	make start-frontend

start-backend:
	./venv/bin/gunicorn \
		-b 0.0.0.0:5000 \
		--preload \
		--access-logfile - \
		--error-logfile - \
		--timeout 300 \
		-w 5 \
		backend:app

start-workflow:
	./venv/bin/gunicorn \
		-b 0.0.0.0:8080 \
		--preload \
		--access-logfile - \
		--error-logfile - \
		--timeout 300 \
		-w 5 \
		workflow:app

start-frontend:
	cd frontend && npm start

download-swagger:
	wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.5/swagger-codegen-cli-2.4.5.jar -O swagger-codegen-cli.jar
