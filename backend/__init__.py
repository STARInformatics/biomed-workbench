import gevent.monkey; gevent.monkey.patch_all()

from flask import Flask, render_template, jsonify, request, Response, send_file
from flask_cors import CORS, cross_origin
import os
import json
import requests
import tempfile

# import libsbgn and important SBGN types
import libsbgnpy.libsbgn as libsbgn
from libsbgnpy import libsbgn, utils, render

from .mondo import search
import backend.workflow as workflow
from .neo4j import get_ncats_data

path = os.path.dirname(os.path.abspath(__name__))
app = Flask(__name__)

def get(d:dict, *keys, default=None):
    try:
        for key in keys:
            d = d[key]
        return d
    except:
        return default

# Set the hostname
BKW_BASE_URL = os.getenv('BKW_BASE_URL', "http://localhost:5000")
BKW_API_PATH = os.getenv('BKW_API_PATH', "")
SERVICE_URL = BKW_BASE_URL + BKW_API_PATH

@app.route("/")
def index():
    endpoints = [
        '/api/disease/diabetes mellitus',
        '/api/workflow/mod0/MONDO:0005148',
        '/api/workflow/mod1a/MONDO:0005148',
        '/api/workflow/mod1e/MONDO:0005148',
        '/api/workflow/mod1b1/MONDO:0005148',
        '/api/gene-to-pathway/HGNC:406',
        '/api/data/HGNC:406',
        '/api/pathway-to-sbgn/R-HSA-389661',
        '/api/pathway-to-png/R-HSA-389661',
        '/api/get-ncats-data/MONDO:0005148'
    ]
    return 'API workflow example:<br>' + '<br>'.join('<a href="{}">{}{}</a>'.format(e, SERVICE_URL, e) for e in endpoints)

@app.route('/api/data/<string:id>')
@cross_origin()
def get_data(id):
    return jsonify(get_statements(id))

@app.route('/api/get-ncats-data/<string:id>')
@cross_origin()
def get_ncats_data_endpoint(id):
    return jsonify(get_ncats_data(id))

@app.route('/api/disease/<string:keywords>')
@cross_origin()
def disease(keywords):
    size = request.args.get('size')

    diseases = search(keywords)

    if size is not None:
        size = int(size)
        diseases = diseases[:size]

    data = json.dumps(diseases)
    response = Response(data, status=200, mimetype='application/json')
    return response
    # return jsonify(search(keywords))

@app.route('/api/workflow/mod0/<string:mondo_id>')
@cross_origin()
def mod0(mondo_id):
    return jsonify(workflow.mod0_disease_lookup(mondo_id))

@app.route('/api/workflow/mod1a/<string:mondo_id>')
@cross_origin()
def mod1a(mondo_id):
    data = workflow.mod0_disease_lookup(mondo_id)
    return jsonify(workflow.mod1a_functional_similarity(data))

@app.route('/api/workflow/mod1e/<string:mondo_id>')
@cross_origin()
def mod1e(mondo_id):
    data = workflow.mod0_disease_lookup(mondo_id)
    return jsonify(workflow.mod1e_gene_interactions(data))

@app.route('/api/workflow/mod1b1/<string:mondo_id>')
@cross_origin()
def mod1b1(mondo_id):
    data = workflow.mod0_disease_lookup(mondo_id)
    return jsonify(workflow.mod1b1_phenotype_similarity(data))

# @app.route('/api/disease-to-gene/<string:mondo_id>')
# @cross_origin()
# def gene_lookup(mondo_id):
#     size = request.args.get('size')
#
#     input_object, disease_associated_genes, input_curie_set = diseaseLookUp(mondo_id)
#     df = disease_associated_genes
#
#     records = []
#
#     for d in df.to_dict(orient='record'):
#         records.append({
#             'disease_id' : d['input_id'],
#             'gene_id' : d['hit_id'],
#             'gene_symbol' : d['hit_symbol'],
#             'relation' : d['relation']
#         })
#
#     if size is not None:
#         size = int(size)
#         records = records[:size]
#
#     return jsonify(records)

known_pathways = set()
known_pathways.update(filename.replace('.sbgn', '') for filename in os.listdir(os.path.join('backend', 'data', 'sbgn')))
known_pathways.update(filename.replace('.png', '') for filename in os.listdir(os.path.join('backend', 'data', 'diagrams')))

@app.route('/api/gene-to-pathway/<string:gene_id>')
@cross_origin()
def pathway_lookup(gene_id):
    response = requests.post(
        'https://reactome.org/AnalysisService/identifiers/projection/?page=1',
        data=gene_id.strip(),
        headers={'Content-Type' : 'text/plain'},
    )

    d = response.json()

    records = []
    for pathway in d['pathways']:
        pathway_id = get(pathway, 'stId')
        if pathway_id not in known_pathways:
            continue
        records.append({
            'pathway_id' : pathway_id,
            'species' : get(pathway, 'species', 'name'),
            'name' : get(pathway, 'name')
        })
    return jsonify(records)

@app.route('/api/pathway-to-sbgn/<string:pathway_id>')
@cross_origin()
def get_xml(pathway_id):
    filename = os.path.join('backend', 'data', 'sbgn', pathway_id) + '.sbgn'
    with open(filename, mode='r') as f:
        response = Response(f.read(), status=200, mimetype='application/xml')
        return response

@app.route('/api/pathway-to-png/<string:pathway_id>')
@cross_origin()
def get_png(pathway_id):
    filename = os.path.join('data', 'diagrams', pathway_id) + '.png'
    return send_file(filename, mimetype='image/png')

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('error/404.html'), 404

if __name__ == "__main__":
    app.run()
