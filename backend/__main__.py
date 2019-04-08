from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
import os
import json

from .mondo import search

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
    if size is not None:
        size = int(size)
        return jsonify(search(keywords)[:size])
    else:
        return jsonify(search(keywords))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

if __name__ == "__main__":
    app.run()
