#! /usr/bin/env python

lines = []

#function to print 100 lines from a file
def printLine():
    with open('randomfile2.txt') as inputfile:
        lineCount = 0
        for line in inputfile:
            lineCount = lineCount + 1
            fileDesc = line.split('\t')
            
            if (lineCount<=100):
                lines.append(line)
                print fileDesc[0]
            else:
                break

printLine()
print 'length of LINES: ' + str(len(lines))

