from flask import Flask
from milvus import Milvus

app = Flask(__name__)
milvus_cli = Milvus()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/init")
def init_vector():
    return milvus_cli.init_vector()


@app.route("/query")
def query_vector():
    return milvus_cli.query_vector()
