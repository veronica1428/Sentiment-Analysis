#! /usr/bin/env python

reviewID = []
dict = {}

#reading paragraphs according to review id's
def readPara():
    print 'inside readPara function'
    revText = open('randomfile2.txt')
    manReview = open('File12.txt')

    for id in manReview:
        ent,reviewText = manReview.readline().rsplit(None, 1)
        print reviewText
        reviewID.append(reviewText)
    
    ch = 0

    for line in revText:
        
        if(ch > 0 and ch < 150):
            textContent = line.split('\t')
            
            ch = ch + 1

        else:
            ch = ch + 1

#entry from here
def main():
    print 'inside main method'
    readPara()

main()



