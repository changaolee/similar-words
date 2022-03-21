from flask import Flask
from search import Search

app = Flask(__name__)
search = Search()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/init")
def init_vector():
    search.init_vector()
