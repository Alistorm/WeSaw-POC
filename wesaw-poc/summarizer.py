#!/usr/bin/python

import sys
import urllib.request
from bs4 import BeautifulSoup
from nltk import pos_tag
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from heapq import nlargest
from collections import defaultdict

def getTextWaPo(url):
    page = urllib.request.urlopen(url).read().decode('utf8','ignore')
    soup = BeautifulSoup(page,"lxml")
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    text = ' '.join(map(lambda body: body.text,soup.find_all('p')))
    text = text.encode('ascii', errors='replace').replace("?".encode("utf8")," ".encode("utf8"))
    return text.decode('ascii', 'ignore')

def summarize(text,lang):
    sents = sent_tokenize(text)
    n = int(round(len(sents)*0.04,0))
    if n < 1:
        n=1
    word_sent = word_tokenize(text.lower())

    if lang=="fr":
        _stopwords = set(stopwords.words('french') + list(punctuation))
        word_sent = [word for word in word_sent if word not in _stopwords]
    elif lang=="en":
        _stopwords = set(stopwords.words('english') + list(punctuation))
        word_tag = pos_tag(word_sent)
        word_sent = [word[0] for word in word_tag if word[0] not in _stopwords and word[1] == "NN"]
    else:
        assert 1==0

    ntags = len(word_sent)
    if ntags > 5:
        ntags = 5

    freq = FreqDist(word_sent)
    
    tags = nlargest(ntags, freq, key=freq.get)
    
    ranking = defaultdict(int)

    for i,sent in enumerate(sents):
        for v in word_tokenize(sent.lower()):
            if v in freq:
                ranking[i] += freq[v]
    
    sents_idx = nlargest(n, ranking, key=ranking.get)
    summary=""
    for j in sorted(sents_idx):
      summary += sents[j]
    return [summary,tags]

def main(source,lang,content):
    text = ""
    if source == "url":
        text = getTextWaPo(content)
    elif source == "text":
        text = content
    else:
        assert 1==0
    return summarize(text,lang)