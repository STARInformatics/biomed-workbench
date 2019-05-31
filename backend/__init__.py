import gevent.monkey; gevent.monkey.patch_all()

from flask import Flask, render_template, jsonify, request, Response, send_file
from flask_cors import CORS, cross_origin
import os
import json
import requests
import tempfile
import asyncio

# import libsbgn and important SBGN types
import libsbgnpy.libsbgn as libsbgn
from libsbgnpy import libsbgn, utils, render

from .mondo import diseaseSearch
import backend.workflow as workflow
from backend.workflow.gene_set import GeneSetWrapper
from .neo4j import get_ncats_data
from mygene import MyGeneInfo
from collections import namedtuple

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
        '/api/workflow/genes/from/diseases?identifiers=MONDO:0005148',
        '/api/workflow/genes/from/diseases?identifiers=MONDO:0005148,HGNC:406',
        '/api/workflow/genes/similarity/function?identifiers=MONDO:0005148',
        '/api/workflow/genes/similarity/phenotype?identifiers=MONDO:0005148',
        '/api/workflow/genes/similarity/phenotype?identifiers=HGNC:406',
        '/api/workflow/genes/similarity/phenotype?identifiers=HGNC:406,HGNC:37234',
        '/api/workflow/genes/interactions/genes?identifiers=MONDO:0005148',
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
    output = json.dumps(get_statements(id))
    response = Response(output, status=200, mimetype='application/json')
    return response


@app.route('/api/get-ncats-data/<string:id>')
@cross_origin()
def get_ncats_data_endpoint(id):
    return jsonify(get_ncats_data(id))

@app.route('/api/disease/<string:keywords>')
@cross_origin()
def disease(keywords):
    size = request.args.get('size')
    diseases = getDiseaseIdentifiers(keywords)
    data = json.dumps(diseases)
    response = Response(data, status=200, mimetype='application/json')
    return response
    # return jsonify(search(keywords))

@app.route('/api/workflow/genes/from/<string:category>')
@cross_origin()
def mod0(category):
    identifiers = request.args.get('identifiers')
    identifiers = identifiers.split(",")

    if identifiers is not None:
        filteredIdentifiers = filterIdentifiersByCuries(identifiers, providerMap[category])

        genes = []
        for mondo_id in filteredIdentifiers:
            genes += workflow.mod0_disease_gene_lookup(mondo_id)
        data = json.dumps(genes)

        response = Response(data, status=200, mimetype='application/json')
    else:
        response = Response(status=500)

    return response

@app.route('/api/workflow/genes/similarity/function')
@cross_origin()
def mod1a():
    identifiers = request.args.get('identifiers')
    identifiers = identifiers.split(",")
    geneList = gatherGeneIdentifiers(identifiers)

    return jsonify(workflow.mod1a_functional_similarity(geneList))

@app.route('/api/workflow/genes/similarity/phenotype')
@cross_origin()
def mod1b1():
    identifiers = request.args.get('identifiers')
    identifiers = identifiers.split(",")

    geneIdentifierList = gatherGeneIdentifiers(identifiers)
    return jsonify(workflow.mod1b1_phenotype_similarity(geneIdentifierList))

@app.route('/api/workflow/genes/interactions/genes')
@cross_origin()
def mod1e():
    identifiers = request.args.get('identifiers')
    identifiers = identifiers.split(",")
    geneIdentifierList = gatherGeneIdentifiers(identifiers)
    return jsonify(workflow.mod1e_gene_interactions(geneIdentifierList))

known_pathways = set()
known_pathways.update(filename.replace('.sbgn', '') for filename in os.listdir(os.path.join('backend', 'data', 'sbgn')))
known_pathways.update(filename.replace('.png', '') for filename in os.listdir(os.path.join('backend', 'data', 'diagrams')))

@app.route('/api/gene-to-pathway/<string:gene_id>')
@cross_origin()
def pathway_lookup(gene_id):
    response = requests.post(
        'https://reactome.org/AnalysisService/identifiers/projection/?page=1',
        data=gene_id.strip(),
        headers={'Content-Type': 'text/plain'},
    )

    d = response.json()

    records = []
    for pathway in d['pathways']:
        pathway_id = get(pathway, 'stId')
        if pathway_id not in known_pathways:
            continue
        records.append({
            'pathway_id': pathway_id,
            'species': get(pathway, 'species', 'name'),
            'name': get(pathway, 'name')
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

providerMap = {
    "diseases": ["MONDO", 'DO', 'OMIM'],
    "genes": ["HGNC", "HP"]
}

def gatherGeneIdentifiers(identifiers):
    """
    Converts ["<CURIE>:<ID>"] to a list of objects in the format that are
    adequate to input into the modules.

    ie., [{hit_id: *, hit_symbol: *, input_id: *}]

    :param identifiers:
    :return [BioLinkGeneHit]:
    """

    # TODO: Bad practice. We shouldn't have to create objects just for method conversions.
    geneSetWrapper = GeneSetWrapper()
    BioLinkGeneHit = namedtuple('BioLinkGeneHit', ['hit_id', 'hit_symbol', 'input_id'])

    hits = []
    for identifier in identifiers:

        identifier = identifier.split(":")
        identifier = {
            "curie": identifier[0],
            "id": identifier[1]
        }
        identifierStr = identifier["curie"] + ":" + identifier["id"]

        # dispatch based on item's category in list
        # TODO: makes assumption that curies map completely onto their category
        if identifier["curie"] in providerMap["diseases"]:
            diseaseGenes = workflow.mod0_disease_gene_lookup(identifierStr)
            hits += diseaseGenes

        # TODO: gene-specific identifiers look for equivalencies, gene -> gene
        if identifier["curie"] in providerMap["genes"]:
            mgiGene = geneSetWrapper.hgncCurie2hgncHit(identifierStr)
            # ignoring uniprot id?
            gene = BioLinkGeneHit(mgiGene["input_id"], mgiGene["gene_symbol"], identifierStr)
            hits.append(dict(gene._asdict()))

    return hits

def filterIdentifiersByCuries(identifiers, curies):
    filteredIdentifiers = []
    for identifier in identifiers:
        if identifier.split(":")[0] in curies:
            filteredIdentifiers.append(identifier)
        else:
            print("excluding ", identifier)
    return filteredIdentifiers

def getDiseaseIdentifiers(keywords, size=None):
    diseaseIdentifiers = diseaseSearch(keywords)
    if size is not None:
        size = int(size)
        diseaseIdentifiers = diseaseIdentifiers[:size]
    return diseaseIdentifiers

if __name__ == "__main__":
    app.run()
