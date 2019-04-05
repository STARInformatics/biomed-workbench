install:
	ls venv || virtualenv -p python3.6 venv
	venv/bin/pip3 install -r requirements.txt

run:
	venv/bin/python3 -m server

download:
	mkdir -p server/data
	wget http://purl.obolibrary.org/obo/mondo.json -O server/data/
	# wget https://data.monarchinitiative.org/ttl/hgnc.ttl -O server/data/
	# wget https://www.ebi.ac.uk/biomodels/model/download/MODEL1707111726.2?filename=MODEL1707111726.xml -O server/data/
	# wget https://www.ebi.ac.uk/biomodels/model/download/BIOMD0000000724.5?filename=Theinmozhi_2018.xml -O server/data/Theinmozhi_2018.xml
