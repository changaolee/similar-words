from flask import Flask, request, jsonify
from search import Search

app = Flask(__name__)
search = Search()


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/init")
def init_vector():
    search.init_vector()
    return "finished!"


@app.route("/similar_word", methods=["POST"])
def similar_word():
    params = request.json
    words = search.query_word(params["word"], params["top_k"])
    return jsonify(words)