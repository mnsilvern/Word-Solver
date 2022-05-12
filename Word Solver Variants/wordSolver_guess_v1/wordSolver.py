#clear variables
#from IPython import get_ipython
#get_ipython().magic('reset -sf')

#import nltk
#from nltk.corpus import words
#from nltk.tag import pos_tag
from collections import Counter

import math

import copy



# #letter frequency
# letterScore = [['a',8.5],['b',2.1],['c',4.5],['d',3.4],['e',11.1],['f',1.8],['g',2.5],['h',3.0],['i',7.5],['j',.2],['k',1.1],['l',5.5],['m',3.0],['n',6.7],['o',7.2],['p',3.2],['q',.2],['r',7.6],['s',5.7],['t',7.0],['u',3.6],['v',1.0],['w',1.3],['x',.3],['y',1.8],['z',.3]]
# #maxScore = 
# discount = .5

#------------------------------------------------------------------------------
#N letter words
numCharacters = 5
spaceReduction = .25
printNum = 5
roundNum = 6
#wordSource = 'wordleList.txt'
wordSource = 'wordleLegalGuess.txt'

goodSetMade = []
greySetMade = []
yellowSetMade = [[] for _ in range(numCharacters)]
greenSetMade = [[] for _ in range(numCharacters)]


#------------------------------------------------------------------------------

# #importing english words
# wordList = words.words()
# charNList = []

# #slimming word list down to N letter words
# for i in range(len(wordList)):
#     if len(wordList[i]) == numCharacters:
#         charNList.append(wordList[i])

# #tagging N letter words with grammer type
# taggedList = pos_tag(charNList)

# #making list of N letter words with no proper nouns
# charNListNoPN = []
# for i in range(len(charNList)):
#     if taggedList[i][1] != 'NNP':
#         charNListNoPN.append(taggedList[i][0])

#------------------------------------------------------------------------------

#this is the complete possible wordle list (big time cheating)
with open(wordSource,'r') as f:
    wordleList = f.readlines()
charNListNoPN = [s.replace("\n", "") for s in wordleList]
#------------------------------------------------------------------------------
#functions

def greyLet(greySetMade,greyGuess):
    
    for i in range(len(greyGuess[0])):
        if greyGuess[0][i] != ' ':
            if greyGuess[0][i] not in greySetMade:
                greySetMade.append(greyGuess[0][i])
                
    return greySetMade

def yellowLet(goodSetMade,yellowSetMade,yellowGuess):
    
    for i in range(len(yellowGuess[0])):
        if yellowGuess[0][i] != ' ':
                if yellowGuess[0][i] not in goodSetMade:
                    goodSetMade.append(yellowGuess[0][i])

    for j in range(len(yellowGuess[0])):
        if yellowGuess[0][j] != ' ':
            if (yellowGuess[0][j] not in yellowSetMade[j]):
                yellowSetMade[j].append(yellowGuess[0][j])

    return goodSetMade,yellowSetMade

def greenLet(goodSetMade,greenSetMade,greenGuess):

    for i in range(len(greenGuess[0])):
        if greenGuess[0][i] != ' ':
            if greenGuess[0][i] not in goodSetMade:
                goodSetMade.append(greenGuess[0][i])

    for j in range(len(greenGuess[0])):
        if greenGuess[0][j] != ' ':
            if (greenGuess[0][j] not in greenSetMade[j]):
                greenSetMade[j] = (greenGuess[0][j])
    
    return goodSetMade,greenSetMade

def guessListMaker(numCharacters,charNListNoPN,goodSetMade,greySetMade,yellowSetMade,greenSetMade):
    greyListMade = []
    goodListMade = []
    yellowListMade = []
    greenListMade = []
    
    #weed out greySetMade
    for i in range(len(charNListNoPN)):
        status = 1
        for j in range(numCharacters):
            if status == 0:
                break
            if charNListNoPN[i][j] in greySetMade:
                #counting freq. of that letter in greenSetMade
                countsGreen = 0
                countsYellow = 0
                for k in range(numCharacters):    
                    if bool(greenSetMade[k]) == True:
                        if greenSetMade[k] == charNListNoPN[i][j]:
                            countsGreen = countsGreen + 1
                    if charNListNoPN[i][j] in yellowSetMade[k]:
                        countsYellow = countsYellow + 1
                #counting freq. of that letter in word
                countsWord = Counter(charNListNoPN[i])[charNListNoPN[i][j]]
                #only put on greyListMade if freq. in word is greater than freq. in greenListMade
                if countsWord > countsGreen and countsYellow == 0:                                      
                    status = 0
        if status == 1:
            if charNListNoPN[i] not in greyListMade:
                greyListMade.append(charNListNoPN[i])

    #pare down to yellowListMade
    for i in range(len(greyListMade)):
        status = 1
        for j in range(numCharacters):
            if greyListMade[i][j] in yellowSetMade[j]:
                status = 0
            if status == 0:
                break
        if status == 1:
            if greyListMade[i] not in yellowListMade:
                yellowListMade.append(greyListMade[i])
              
    #pare down to goodListMade
    for i in range(len(yellowListMade)):
        status = 1
        for j in range(len(goodSetMade)):
            if goodSetMade[j] not in yellowListMade[i]:
                status = 0
            if status == 0:
                break
        if status == 1:
            if yellowListMade[i] not in goodListMade:
                goodListMade.append(yellowListMade[i])
                
    #pare down to greenListMade
    for i in range(len(goodListMade)):
        status = 1
        for j in range(numCharacters):
            if (bool(greenSetMade[j]) == True) and (goodListMade[i][j] != greenSetMade[j]):
                status = 0
            if status == 0:
                break
        if status == 1:
            if goodListMade[i] not in greenListMade:
                greenListMade.append(goodListMade[i])
                
    return greyListMade,goodListMade,yellowListMade,greenListMade

#assigning average bits of uncertainty to each word against greenWordList
def wordUnc(numCharacters,listUnc,listUnc2,greenSetUnc,yellowSetUnc,greySetUnc,goodSetUnc):
    wordUncSumList = [0]*len(listUnc)
    wordUncAvgList = [0]*len(listUnc)
    
    for i in range(len(listUnc)):
        
        wordUncSum = 0
        
        for j in range(len(listUnc2)):
            greySetTemp = copy.deepcopy(greySetUnc)
            yellowSetTemp = copy.deepcopy(yellowSetUnc)
            greenSetTemp = copy.deepcopy(greenSetUnc)
            goodSetTemp = copy.deepcopy(goodSetUnc)
            
            if listUnc[i] != listUnc2[j]:
                
                #assigning greenSetTemp, yellowSetTemp, greySetTemp, and goodSetTemp for that word
                wordUnc = 0
                for k in range(numCharacters):
                    if listUnc[i][k] == listUnc2[j][k]:
                        #green set + good set
                        if listUnc[i][k] not in goodSetTemp:
                            goodSetTemp.append(listUnc[i][k])
                        
                        if listUnc[i][k] not in greenSetTemp[k]:
                            greenSetTemp[k] = listUnc[i][k]
                    else:

                        if listUnc[i][k] in listUnc2[j]:
                            
                            #yellow set + good set
                            if listUnc[i][k] not in goodSetTemp:
                                goodSetTemp.append(listUnc[i][k])
                            
                            if listUnc[i][k] not in yellowSetTemp[k]:
                                yellowSetTemp[k].append(listUnc[i][k])
                        else:
                            #grey set
                            if listUnc[i][k] not in greySetTemp:
                                greySetTemp.append(listUnc[i][k])
                
                greyListTemp,goodListTemp,yellowListTemp,greenListTemp = guessListMaker(numCharacters,listUnc,goodSetTemp,greySetTemp,yellowSetTemp,greenSetTemp)
                
                # print('Control Word: ' + str(listUnc[i]))
                # print('Target Word: ' + str(listUnc[j]))
                # print('greyListTemp ' + str(len(greyListTemp)))
                # print('goodListTemp ' + str(len(goodListTemp)))
                # print('yellowListTemp ' + str(len(yellowListTemp)))
                # print('greenListTemp ' + str(len(greenListTemp)))
                
                wordUnc = len(greenListTemp)
                wordUncSum = wordUncSum + wordUnc
        
        wordUncSumList[i] = wordUncSum
        print('word ' + str(i) + '/' + str(len(wordUncSumList)-1))
        
    #creating sorted list of avg. uncertainties w/ word
    wordUncAvgListValues = [x / len(wordUncSumList) for x in wordUncSumList]
    for l in range(len(wordUncAvgListValues)):
        wordUncAvgList[l] = [wordUncAvgListValues[l],listUnc[l]]
    wordUncAvgListSorted = sorted(wordUncAvgList, reverse=False)
                
    return wordUncAvgListSorted
#-----------------------------------------------------------------------------        
#main  

wordSpaceList = [0]*(roundNum+1)
wordSpaceList[0] = len(charNListNoPN)

for round in range(roundNum):
    
    greyPrompt = input('enter your grey letters this round\n')
    greyGuess = [greyPrompt]
    yellowPrompt = input('enter your yellow letters this round\n')
    yellowGuess = [yellowPrompt]
    greenPrompt = input('enter green letters this round\n')
    greenGuess = [greenPrompt]

    greySetMade = greyLet(greySetMade,greyGuess)
    goodSetMade,yellowSetMade = yellowLet(goodSetMade,yellowSetMade,yellowGuess)
    goodSetMade,greenSetMade = greenLet(goodSetMade,greenSetMade,greenGuess)
    greyListMade,goodListMade,yellowListMade,greenListMade = guessListMaker(numCharacters,charNListNoPN,goodSetMade,greySetMade,yellowSetMade,greenSetMade)
    
    wordSpaceList[round+1] = len(greenListMade)
    
    wordUncAvgListSorted = wordUnc(numCharacters,greenListMade,greenListMade,greenSetMade,yellowSetMade,greySetMade,goodSetMade)
    
    print('--------------------------------------')
    
    print('space size history: ' + str(wordSpaceList))
    
    if (min(wordUncAvgListSorted)[0] >= spaceReduction*wordSpaceList[round+1]) and (wordSpaceList[round+1] > 2):
        wordUncAvgListSorted = wordUnc(numCharacters,yellowListMade,greenListMade,greenSetMade,yellowSetMade,greySetMade,goodSetMade)
        print('estimated new space size: ' + str(min(wordUncAvgListSorted)[0]))
        print('yellowList used')
    else:
        print('estimated new space size: ' + str(min(wordUncAvgListSorted)[0]))
        print('greenList used')
    
    print('\n')
    

    if len(wordUncAvgListSorted) <= 5:
        printNum = len(wordUncAvgListSorted)
    for i in range(printNum):
        print(wordUncAvgListSorted[i])
    print('round finished')
    print('--------------------------------------')
    input("Press Enter to continue...")
        