from flask import Flask, render_template
import os

path = os.path.dirname(os.path.abspath(__name__))
app = Flask(__name__, root_path=f'{path}/web')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hello")
def helloworld():
    return "Hello World!"

@app.route("/hello/<string:name>")
def hello(name):
    return f"Hello {name}!"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404

if __name__ == "__main__":
    app.run()
