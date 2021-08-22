import random

import googlesearch
import nltk
import requests
from bs4 import BeautifulSoup
from google.cloud import datastore
from typing import Dict, List

nltk.download('punkt')
nltk.download('brown')
from nltk.corpus import brown
sent_tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")



class Corpus:
    def __init__(self, dsclient: datastore.Client, searchterm: str, seed: str, max_results: int = 10):
        self._dsclient = dsclient
        self._searchterm = searchterm
        self._max_results = max_results
        self._random = random.Random(seed)

    def load(self):
        key = self._dsclient.key("Corpus", self._searchterm)
        dbentry = self._dsclient.get(key)
        if not dbentry:
            self.create(max_results=self._max_results)
            self.save()
        else:
            self.update(dbentry)

    def create(self, max_results=10):
        print(f"Creating corpus for term: {self._searchterm}")

        brown_words = brown.words()
        self._buildcorpus(brown_words)

        rawtext = ""

        # Get search results.
        if max_results > 0:
            count = 0
            for url in googlesearch.search(self._searchterm):
                # Fetch page.
                print(f"[{count+1}/{max_results}] Fetching {url}...")
                try:
                    r = requests.get(url, timeout=3)
                    if r.status_code != 200:
                        # Skip non-200 responses.
                        continue
                    # Get the HTML of the page.
                    html_doc = r.text
                except:
                    continue

                # Get the text from the page and add it to the corpus.
                soup = BeautifulSoup(html_doc, "html.parser")
                pagetext = soup.get_text()
                print(f"Got {len(pagetext.split())} words from {url}")
                rawtext += pagetext
                count += 1
                if count >= max_results:
                    break

            # Make a corpus from the words.
            print(f"Building corpus from {len(rawtext.split())} words...")
            self._buildcorpus(rawtext.split())
            # self._nltk_text = nltk.Text(rawtext.split())

    #    def gentext_nltk(self, startword: str, maxlen: int) -> str:
    #        generated = self._nltk_text.generate(length=maxlen)
    #        return generated

    def gentext(self, startword: str, maxlen: int) -> str:
        retval = ""
        curword = startword
        wordcount = 0
        while wordcount < maxlen:
            if curword in [".", ",", "'", ";", "-", "?", ":"]:
                retval += curword
            else:
                if len(retval) > 0:
                    retval += " "
                retval += curword
            if curword not in self._nextwordprobs:
                return retval

            r = self._random.random()

            problist = list(self._nextwordprobs[curword].items())
            # Sort by probability, decreasing, to make lookup deterministic.
            problist.sort(key=lambda v: v[0], reverse=True)
            for nextword, prob in problist:
                if r <= prob:
                    curword = nextword
                    break
                r -= prob
            wordcount += 1

        # Now, capitalize it properly.
        sentences = sent_tokenizer.tokenize(retval)
        sentences = " ".join([sent.capitalize() for sent in sentences])
        return sentences

    def _buildcorpus(self, wordlist: List[str]):
        # This maps a previous word to the dictionary of counts of next words observed.
        nextwordcounts: Dict[str, Dict[str, int]] = {}
        prevword = wordlist[0]
        for nextword in wordlist[1:]:  # All words from 1....end
            if prevword not in nextwordcounts:
                # We have not seen this word before.
                nextwordcounts[prevword] = {nextword: 1}

            wordcounts = nextwordcounts[prevword]
            if nextword not in wordcounts:
                wordcounts[nextword] = 1
            else:
                wordcounts[nextword] += 1

            prevword = nextword

        # Now calculate frequencies.
        self._nextwordprobs: Dict[str, Dict[str, float]] = {}
        for prevword, wordcounts in nextwordcounts.items():
            totalcount = sum([count for _, count in wordcounts.items()])
            wordprobs = {
                nextword: count / totalcount for nextword, count in wordcounts.items()
            }
            self._nextwordprobs[prevword] = wordprobs

    def save(self):
        entity = {
            "searchterm": self._searchterm,
            "nextwordprobs": self._nextwordprobs,
        }
        #key = self._dsclient.key("Corpus", self._searchterm)
        #insert_entity = datastore.Entity(key=key)
        #insert_entity.update(entity)
        #self._dsclient.put(insert_entity)
        #print(f"Wrote entity to DB with key {key}")

    def update(self, dbentry):
        print(f"Updating from dbentry with search term: {dbentry['searchterm']}")
        self._nextwordprobs = dbentry["nextwordprobs"]

        import json

        with open("foo.json", "w") as fp:
            jval = json.dumps(self._nextwordprobs)
            fp.write(jval)
