#! /usr/bin/env python3

import nltk
import os
import collections

from nltk.tree import *

import stanfordParser
import readSentiWordNet

#Variables declaraction
sentences = []
lineCount = 1
sentiLib = []

#call to sentiWordNet dictionary
def readSentiDict():
    global sentiLib
    sentiLib = readSentiWordNet.sentiWordNet()
    print ('sentiLib: ' , sentiLib)

#form the input sentence/line in tree structure
def dependancyParseTree():
    concepts = []
    for sent in sentences:
        print('sent passed :', sent)
        concepts.append(stanfordParser.parseDepTree(sent))     #referring stanfordParser.py class
#for i in concepts:
#print ('concepts: ' , i)

#read the review file or training data
def readReviewFile():
    print ('Inside readReviewFile function')
    global lineCount

    with open('TestData.txt') as inputfile:
        for line in inputfile:
            
            #read only first 100 reviews
            if '##' in line:
                
                if lineCount <=10:
                    hashSplit = line.split('##')
                    sentences.append(hashSplit[1])
                    lineCount = lineCount + 1

#Main function definition
def main():
    print('Inside main function')
    readReviewFile()                        #to read input review file
    dependancyParseTree()                   #to parse all the sentences
    #readSentiDict()                        #read sentiWordNet dictionary

#actual program functioning starts from here
main()
