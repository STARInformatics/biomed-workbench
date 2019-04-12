VENV?=venv
PYTHON3_PATH?=${VENV}/bin/python3
PIP3_PATH?=${VENV}/bin/pip3

# Externalized to README manual action by user.
#VIRTUALENV_PATH?=${VENV}/bin/virtualenv
#
#venv:
#	ls ${VENV} || ${VIRTUALENV_PATH} -p python3.6 ${VENV}
#	source ${VENV}/bin/activate

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
	wget http://purl.obolibrary.org/obo/mondo.json -O backend/data/mondo.json
	wget https://reactome.org/download/current/diagrams.png.tgz -O backend/data/diagrams.png.tgz
	tar -xvzf backend/data/diagrams.png.tgz --directory backend/data/diagrams
	wget https://reactome.org/download/current/homo_sapiens.sbgn.tar.gz -O backend/data/homo_sapiens.sbgn.tar.gz
	tar -xvzf backend/data/homo_sapiens.sbgn.tar.gz --directory backend/data/sbgn

.PHONY: web venv

service:
	nohup ${PYTHON3_PATH} -m backend >logs/service_`date`.log 2>&1 &

web:
	cd frontend; nohup npm start >../logs/web_`date`.log 2>&1 &

project_settings:
	@echo "Python Virtual Environment (VENV) specified to be located in the subdirectory '${VENV}'"
	@echo "Path to python3 ('PYTHON3_PATH') is specified to be located at path '${PYTHON3_PATH}'"
	@echo "Path to pip3 ('PIP3_PATH') is specified to be located at path '${PIP3_PATH}'"
	#@echo "Path to virtualenv ('VIRTUALENV_PATH') is specified to be located at path '${VIRTUALENV_PATH}'"
	@echo "Override the these environment variables as needed, according to your site installation particulars"
