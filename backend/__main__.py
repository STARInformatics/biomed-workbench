from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS, cross_origin
import os
import json

from .mondo import search
from .workflow import diseaseLookUp

path = os.path.dirname(os.path.abspath(__name__))
app = Flask(__name__, root_path=f'{path}/web')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/graph")
def graph():
    return render_template('graph.html')

@app.route("/demo")
def demo():
    return render_template('demo.html')

@app.route("/hello")
def helloworld():
    return "Hello World!"

@app.route("/hello/<string:name>")
def hello(name):
    return f"Hello {name}!"

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

@app.route('/api/disease-to-gene/<string:mondo_id>')
@cross_origin()
def gene_lookup(mondo_id):
    size = request.args.get('size')

    input_object, disease_associated_genes, input_curie_set = diseaseLookUp(mondo_id)
    df = disease_associated_genes

    records = []

    for d in df.to_dict(orient='record'):
        records.append({
            'disease_id' : d['input_id'],
            'gene_id' : d['hit_id'],
            'gene_symbol' : d['hit_symbol'],
            'relation' : d['relation']
        })

    if size is not None:
        size = int(size)
        records = records[:size]

    return jsonify(records)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

if __name__ == "__main__":
    app.run()
