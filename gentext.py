import random

import googlesearch
import nltk
import requests
from bs4 import BeautifulSoup

print("Starting")


def calc_prob(wordlist, word):
    # Return the probability that "word" is generated by "wordlist"
    # eg., calc_prob(d["cow"], "moo") == 1/10
    # .     calc_prob(d["cow"], "barf") == 0
    justwords = [x[0] for x in wordlist]
    justcounts = [x[1] for x in wordlist]
    if word in justwords:
        i = justwords.index(word)
        return justcounts[i] / sum(justcounts)
    else:
        return 0


def pickword(wordlist):
    # return a random word from wordlist according to its frequency
    r = random.random()
    for word, count in wordlist:
        p = calc_prob(wordlist, word)
        if r < p:
            return word
        else:
            r -= p


def gentext(corpus, startword, maxlen):
    retval = ""
    curword = startword
    wordcount = 0
    while wordcount < maxlen:
        if curword in [".", ",", "'", ";", "-", "?", ":"]:
            retval += curword
        else:
            retval += " " + curword
        if curword not in corpus:
            # yer DONE
            return
        wordlist = corpus[curword]
        curword = pickword(wordlist)
        wordcount += 1
    return retval


def makecorpus(wordlist):
    corpus = {}
    prevword = wordlist[0]
    for nextword in wordlist[1:]:  # All words from 1....end
        if prevword not in corpus:
            # We have not seen this word before.
            corpus[prevword] = [[nextword, 1]]
        else:
            # We have seen this word before.
            countlist = corpus[prevword]
            corpus[prevword] = updatelist(countlist, nextword)
        prevword = nextword
    return corpus


def updatelist(countlist, nextword):
    # Given a list that looks like this:
    #   [ ["beeb", 3], ["cow", 2] ]
    # Return a list that looks like this:
    #   [ ["beeb", 3], ["cow", 2], [nextword, 1] ]   <-- If nextword is not in countlist
    #   [ ["beeb", 4], ["cow", 2] ]                  <-- If nextword is in countlist
    justwords = [x[0] for x in countlist]
    justcounts = [x[1] for x in countlist]
    if nextword not in justwords:
        return countlist + [[nextword, 1]]
    else:
        i = justwords.index(nextword)
        justcounts[i] += 1
        return list(zip(justwords, justcounts))


def randomtext():
    nltk.download("brown")
    from nltk.corpus import brown
    text = brown.words(categories="learned")[0:20000]
    print(f"Loaded text with {len(text)} words")
    print("Making corpus")
    corpus = makecorpus(text)
    print(f"Corpus has {len(corpus)} entries")
    return gentext(corpus, "The", 100)


def get_corpus(searchterm, max_results=100):
    rawtext = ""

    # Get search results.
    count = 0
    for url in googlesearch.search(searchterm):
        # Fetch page.
        print(f"Fetching {url}...")
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            # Skip non-200 responses.
            continue
        # Get the HTML of the page.
        html_doc = r.text
        # Get the text from the page and add it to the corpus.
        soup = BeautifulSoup(html_doc, 'html.parser')
        pagetext = soup.get_text()
        print(f"Got {len(pagetext.split())} words from {url}")
        rawtext += pagetext
        count += 1
        if count >= max_results:
            break

    # Make a corpus from the words.
    print(f"Making corpus from {len(rawtext.split())} words...")
    corpus = makecorpus(rawtext.split())
    print(f"Corpus has {len(corpus)} entries")
    return corpus
