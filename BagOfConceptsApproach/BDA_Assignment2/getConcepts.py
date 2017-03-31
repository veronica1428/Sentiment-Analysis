#! /usr/bin/env python3

import nltk
#import sentics

from nltk.corpus import wordnet as wn

#sn = sentics.Sentics

#to determine whether the word is stopword in english dictionary or not
def is_stopWord(word):
    if word.lower() in nltk.corpus.stopwords.words('english'):
        return True
    return False

#to remove duplicates from list
def removeDuplicates(globalPOS):

    localPOS = []
    length = len(globalPOS)
    
    for i in globalPOS:
        if i not in localPOS:
            localPOS.append(i)

    return (localPOS)

#break the list into concepts for Noun Phrase only
def getConceptsNP(globalPOS):

    localConcepts = ''
    nConcepts = []
    concepts = []

    print ('globalpos: ', globalPOS)
    
    if len(globalPOS) == 1:
        tag, value = globalPOS[0]
        concepts.append(value)

    length = len(globalPOS)
    for i in range(0,(length-1)):
        for j in range(i+1, length):
            iLabel, iValue = globalPOS[i]
            jLabel, jValue = globalPOS[j]
            
            iStop = is_stopWord(iValue)
            jStop = is_stopWord(jValue)
            
            #Classification according to category
            
            #if bigram is adj and noun
            if ((iLabel == 'JJ') and (jLabel == 'NN')):
                localConcepts = (iValue + '_' + jValue)
                concepts.append(localConcepts)
                concepts.append(jValue)
            
            #if bigram is adjective and stopword
            elif ((iLabel == 'JJ') and (jStop)):
                i = i + 1
                continue
            
            #if bigram is noun and adj
            elif ((iLabel == 'NN') and (jLabel == 'JJ')):
                localConcepts = (iValue)
                concepts.append(localConcepts)

            #if bigram is noun and noun
            elif ((iLabel == 'NN') and (jLabel == 'NN')):
                localConcepts = (iValue + '_' + jValue)
                concepts.append(localConcepts)
                concepts.append(iValue)
                concepts.append(jValue)

            #if bigram is noun and stopword
            elif ((iLabel == 'NN') and (jStop)):
                localConcepts = (iValue)
                concepts.append(localConcepts)
            
            #if bigram is stopword and noun
            elif ((iStop) and (jLabel == 'NN')):
                localConcepts = (jValue)
                concepts.append(localConcepts)

            #if bigram is stopword and adjective
            elif ((iStop) and (jLabel == 'JJ')):
                i = i + 1
                continue

            #for other cases
            else:
                localConcepts = (iValue + '_' + jValue)
                concepts.append(localConcepts)

            i = i + 1
        if i == (length-1):
            break

    #remove duplicates
    nConcepts = removeDuplicates(concepts)
    #print ('concepts : ', nConcepts)
    return nConcepts

#check for concepts
#for i in nConcepts:
#print ('Noun Concepts ', i[0])
#print ('sn:  ', type(i[0]))
#concept_info = sn.concept(i[0])
#sentics.lookup(i[0])

#break the list into concepts for verb phrase also
def getConcepts_All(globalPOS):

    length = len(globalPOS)
    #for i in range(0, (length-1))