#! /usr/bin/env python3

import collections
import csv
import numpy as np

from nltk.corpus import wordnet as wn

#variables declaration
filePath = 'sentiword.txt'

#loading senti word net dictionary
def sentiWordNet():
    
    sent_scores = collections.defaultdict(list)
    
    f = open(filePath)
    reader = csv.reader(f, delimiter='\t')
    for line in reader:
        if line[0].startswith("#"):
            continue
        if len(line) == 1:
            continue
        
        POS, ID, PosScore, NegScore, SynsetTerms, Gloss = line
        
        if len(POS) == 0 or len(ID) == 0:
            continue
        # print POS,PosScore,NegScore,SynsetTerms
        for term in SynsetTerms.split(" "):
            # drop #number at the end of every term
            term = term.split("#")[0]
            term = term.replace("-", " ").replace("_", " ")
            key = "%s/%s" % (POS, term.split("#")[0])
            sent_scores[key].append((float(PosScore), float(NegScore)))
    
    for key, value in sent_scores.items():
        sent_scores[key] = np.mean(value, axis=0)
    
    return sent_scores
