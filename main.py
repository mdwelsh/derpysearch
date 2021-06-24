import os
import random
import time
from typing import Text, Tuple

from flask import Flask, render_template, request, send_from_directory
import requests
import googlesearch
from bs4 import BeautifulSoup
import lorem
from lorem.text import TextLorem
import nltk

nltk.download("words")
from nltk.corpus import words


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

    # corpus = gentext.get_corpus(searchterm)
    # randtext = gentext.gentext(corpus, searchterm, 100)
    # if not randtext:
    #    randtext = gentext.gentext(corpus, "The", 100)

    return render_template(
        "search.html", results=f"Results for {searchterm}:<p><p>boogers"
    )


randomword = words.words()


def fakeurl(searchterm: str) -> Tuple[str, str]:
    pathsep = " › "
    prefix = random.choice(["", "www.", "m.", "en."])
    tld = random.choice(
        [".com", ".edu", ".net", ".io", ".co.uk", ".co.jp", ".gov", ".cc"]
    )
    domain = random.sample(randomword, 1)[0]
    path = ""
    for _ in range(random.randint(1, 3)):
        pathentry = random.choice(["-", "_"]).join(random.sample(randomword, random.randint(1, 3)))
        path += pathsep + pathentry
    urlHost = "https://" + prefix + domain + tld
    if len(path) >= 20:
        path = path[0:20] + "..."
    return urlHost, path


@app.route("/searchresults", methods=["GET"])
def searchresults():
    searchterm = request.args.get("q", "")
    print(f"Search results term is: {searchterm}")

    results = []
    for index in range(10):
        urlHost, urlPath = fakeurl(searchterm)
        snippet = lorem.paragraph()
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
