import os

from flask import Flask, render_template, request, send_from_directory
import requests
import googlesearch
from bs4 import BeautifulSoup


import gentext

app = Flask(__name__)


@app.route("/favicon.png")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.png")


@app.route("/")
def home():
    result = gentext.randomtext()
    return render_template("home.html", result=result)


@app.route("/search", methods=["GET"])
def search():
    searchterm = request.args.get("q", "")
    print(f"Search term is: {searchterm}")
    derpybutton = request.args.get("derpybutton", "") != ""

    corpus = gentext.get_corpus(searchterm)
    randtext = gentext.gentext(corpus, searchterm, 100)
    if not randtext:
        randtext = gentext.gentext(corpus, "The", 100)

    return render_template(
        "search.html", result=f"Results for {searchterm}:<p><p>{randtext}"
    )


# For local testing only.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
