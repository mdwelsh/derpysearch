import os
import random
import time
from typing import Text, Tuple

import googlesearch
import lorem
import nltk
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, send_from_directory
from google.cloud import datastore
from lorem.text import TextLorem
from nltk.corpus import words

import corpus

# Get the words corpus from NLTK.
nltk.download("words")

# Create datastore client.
dsclient = datastore.Client()

# Create app.
app = Flask(__name__)

# Random word generator.
randomword = words.words()


@app.route("/favicon.png")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.png")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=["GET"])
def search():
    searchterm = request.args.get("q", "")
    print(f"Search term is: {searchterm}")

    #thecorpus = corpus.Corpus(dsclient, searchterm)
    #thecorpus.load()

    #    logentry = datastore.Entity(dsclient.key("Log"))
    #    logentry.update(
    #        {
    #            "route": "search",
    #            "searchterm": searchterm,
    #        }
    #    )
    #    dsclient.put(logentry)

    derpybutton = request.args.get("derpybutton", "") != ""
    return render_template("search.html")


def fakeurl(searchterm: str) -> Tuple[str, str]:
    pathsep = " › "
    prefix = random.choice(["", "www.", "m.", "en."])
    tld = random.choice(
        [".com", ".edu", ".net", ".io", ".co.uk", ".co.jp", ".gov", ".cc"]
    )
    domain = random.sample(randomword, 1)[0]
    path = ""
    for _ in range(random.randint(1, 3)):
        pathentry = random.choice(["-", "_"]).join(
            random.sample(randomword, random.randint(1, 3))
        )
        path += pathsep + pathentry
    urlHost = "https://" + prefix + domain + tld
    if len(path) >= 20:
        path = path[0:20] + "..."
    return urlHost, path


@app.route("/searchresults", methods=["GET"])
def searchresults():
    searchterm = request.args.get("q", "")
    print(f"Search results term is: {searchterm}")

    thecorpus = corpus.Corpus(dsclient, searchterm)
    thecorpus.load()

    results = []
    for index in range(10):
        urlHost, urlPath = fakeurl(searchterm)
        # snippet = lorem.paragraph()
        snippet = thecorpus.gentext(searchterm, 20)
        if len(snippet) >= 200:
            snippet = snippet[0:199] + "..."

        result = {
            "urlHost": urlHost,
            "urlPath": urlPath,
            "link": f"/result?index={index}",
            "title": lorem.sentence(),
            "snippet": snippet,
        }
        results.append(result)

    return {"results": results}


@app.route("/result")
def resultpage():
    return render_template(
        "resultpage1.html",
        title="This is the title",
        logo="<img src='/static/tselogo.png' width=100>",
        sitename="This is the site name",
        bodytitle="Body title",
        heroimage="<img src='https://picsum.photos/800/400'>",
        heroimagecaption="Hero image caption",
        bodytext=TextLorem(trange=(30, 40)).text(),
    )


# For local testing only.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
