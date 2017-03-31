#! /usr/bin/env python3

import numpy as np
import nltk;
import pprint;
import csv
import collections
import textwrap

from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

#declared variables
filePath = 'sentiword.txt'
sentences = []
sent_tag = []
wordnet = []
falseNeg = []
falsePos = []
truePos = []
trueNeg = []

global reviewDict
reviewDict = {}

#define two lists: one for positive score and other for negative score
posList = []
negList = []

#variable for confidence matrix
global falsePositive
global falseNegative
global trueNegative
global truePositive

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

sentiLib = sentiWordNet()

#to determine whether the word is stopword in english dictionary or not
def is_stopWord(word):
    if word.lower() in nltk.corpus.stopwords.words('english'):
        return True
    return False

#check whether parametric value is punctuation or not
def is_punctuation(string):
    for char in string:
        if char.isalpha():
            return False
    return True

#Read sentiwordNet and calculate scores
def sentiment(line):

    tokens = word_tokenize(line)
    tag_tuples = nltk.pos_tag(tokens)
    tag_type = 0

    for (string, tag) in tag_tuples:

        if tag.startswith('JJ'):
            tag_type = 'a'
        if tag.startswith('NN'):
            tag_type = 'n'
        if tag.startswith('RB'):
            tag_type = 'r'
        if tag.startswith('VB'):
            tag_type = 'v'

        #remove stop words
        if is_stopWord(string):
            continue

        #if word is a single character
        if len(string) == 1:
            continue

        #remove punctuations and digits
        if not is_punctuation(string):
            token = {'word':string, 'pos':tag_type}
            sent_tag = "%s/%s"%(tag_type, string)
            
            #check if string in dictionary SentiLib or not
            if sent_tag in sentiLib:
                pos, neg = sentiLib[sent_tag]
                posList.append(pos)
                negList.append(neg)

#Function to read input file
def readFileContent():
    print ('Inside readFileContent Method')

    lineCount = 1
    
    print ('PREDICTED SCORE:')
    print ('LineNum\t\t\tReview Id\t\tTitle\t\t\tPositive Score\t\t\tNegative Score\t\t\tObj Score\t\t\tResult')

    with open('Canon S100.txt') as inputfile:

        for line in inputfile:
        
            #read only first 100 reviews
            if lineCount <= 5:
                
                if '##' in line:
                    hashSplit = line.split('##')
                    sentences.append(hashSplit[1])
                    
                    index = sentences.index(hashSplit[1])
                    index = index + 1
                    sentiment(hashSplit[1])
        
                    #calculate total positive score for a line
                    LinePos = calculateMean(posList)
                    lineNeg = calculateMean(negList)
                    objScore = 1 - LinePos - lineNeg
                
                    predScore = PosNeg(LinePos, lineNeg)
                    #dictProgramReview(fileDesc[0], predScore)
                    reviewDict[str(index)] = str(predScore)
                
                    del posList[:]
                    del negList[:]
                
                    print (str(lineCount) , '\t\t' , str(index) , '\t\t' , str(hashSplit[1]) , '\t\t' + str(LinePos) , '\t\t' + str(lineNeg) , '\t\t' + str(objScore)  , '\t\t' , str(PosNeg(LinePos, lineNeg)))
                    print ('...................................................................................')

                    lineCount = lineCount + 1
            else:
                break

    print ('Going inside readManualFile')
    tp, tn, fp, fn = readManualFile()
    print ('True positive: ' , str(tp), '\n','True Negative', str(tn))
    print ('False positive: ', str(fp), '\n','False Negative', str(fn))

#function to calculate more Positive or more negative
def PosNeg(posNum, negNum):
    if posNum >= negNum:
        return 1
    
    else:
        return 0

#function to calculate mean of a list
def calculateMean(list):
    length = len(list)
    total = 0
    
    for x in list:
        total = total + x

    return ((total/length))

#Manually read a file to get the review
def readManualFile():
    
    falsePositive = 0
    falseNegative = 0
    trueNegative = 0
    truePositive = 0
    
    f = open('ManualReview.txt')
    
    for line in range(5):
        print ('line: ' , line)
        id,scoreMan = f.readline().rsplit(None, 1)
        print ('id: ', id, '   score: ', scoreMan)
        
        if id in reviewDict:
            scorePred = reviewDict[str(id)]
        else:
            print ('ID not present in the dictionary')
            pass
        
        #Calculate confidence matrix values
        print ('')
        print ('score pred: ',str(scorePred), 'scoreman: ', str(scoreMan))
        print ('')
        
        if str(scorePred) == str(0):
            if str(scorePred) == str(scoreMan):
                print ('true negative', str(trueNegative), 'predicted score: ' , str(scorePred), 'Manual score: ' , str(scoreMan))
                print ('--------------------------------------------------------')
                trueNegative = trueNegative + 1
                trueNeg.append(id)
            else:
                print ('false negative', str(falseNegative), 'predicted score: ' , str(scorePred), 'Manual score: ' , str(scoreMan))
                print ('--------------------------------------------------------')
                falseNegative = falseNegative + 1
                falseNeg.append(id)
        if str(scorePred) == str(1):
            if str(scorePred) == str(scoreMan):
                print ('true positive', str(truePositive), 'predicted score: ' , str(scorePred), 'Manual score: ' , str(scoreMan))
                print ('--------------------------------------------------------')
                truePositive = truePositive + 1
                truePos.append(id)
            else:
                print ('false positive', str(falsePositive), 'predicted score: ' , str(scorePred), 'Manual score: ' , str(scoreMan))
                print ('--------------------------------------------------------')
                falsePositive = falsePositive + 1
                falsePos.append(str(id))
                falsePos.append(id)
    
    return truePositive, trueNegative, falsePositive, falseNegative

#function to store predicted values in dictionary
#def dictProgramReview(id, score):
#reviewDict.update({str(id) : str(score)})

#Main function
def main():
    
    readFileContent()

    print ('***********after readFileContent********')

    print ('**********************************FALSE POSITIVE**********************')
    for fp in falsePos:
        print ('fp: ', fp)

    print ('**********************************FALSE NEGATIVE**********************')
    for fn in falseNeg:
        print ('fn: ' , fn)

    print ('**********************************TRUE POSITIVE**********************')
    for tp in truePos:
        print ('tp: ', tp)

    print ('**********************************TRUE NEGATIVE**********************')
    for tn in trueNeg:
        print ('tn: ', tn)

#Main point to enter into the actual code working
main()