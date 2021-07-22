from __future__ import division
from itertools import chain
import string

berita = 7
persentase = 50

f1 = open("groundTruth/gt" + str(berita) + "_" + str(persentase) + ".txt", "r")
gTruth = f1.read()

f2 = open("ringkasan/news" + str(berita) + "_" + str(persentase) + ".txt", "r")
ringkas = f2.read()

f = open("hasilUji/ujiBerita"+ str(berita) + "_" + str(persentase) + ".txt", "w")
# f = open("hasilUji/cobacoba.txt", "w")

def getUnigram(tokens):
    countDict = dict()
    for token in tokens:
        if token in countDict:
            countDict[token] += 1
        else:
            countDict[token] = 1
    
    # print(countDict)
    # print()
    f.write(str(countDict) + "\n\n")
    return countDict

def getLCSGrid(x,y):
    n = len(x)
    m = len(y)

    grid = [[0 for i in range(m + 1)] for j in range(n + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                cell = (0, 'e')
            elif x[j - 1] == y[i - 1]:
                cell = (grid[j - 1][i - 1][0] + 1, '\\')
            else:
                over = grid[j - 1][i][0]
                left = grid[j][i - 1][0]

                if left < over:
                    cell = (over, '^')
                else:
                    cell = (left, '<')

            grid[j][i] = cell
    for a in grid:
        print(a)
    print(len(grid))
    print((grid[0]))
    return grid

def getLCS(x, y, maskX):
    grid = getLCSGrid(x, y)
    i = len(x)
    j = len(y)

    while i > 0 and j > 0:
        move = grid[i][j][1]
        if move == '\\':
            maskX[i - 1] = 1
            i -= 1
            j -= 1
        elif move == '^':
            i -= 1
        elif move == '<':
            j -= 1

    return maskX

def getRouge_L(ringkasans, manuals):
    lcsScore = 0.0
    ringkasanUnigram = getUnigram(chain(*ringkasans))
    manualUnigram = getUnigram(chain(*manuals))

    for ringkasan in ringkasans:
        ringkasanMask = [0 for token in ringkasan]
        ringkasanLen = len(ringkasan)

        for manual in manuals:
            getLCS(ringkasan, manual, ringkasanMask)
        
        currentLCSScore = 0.0

        for i in range(ringkasanLen):
            if ringkasanMask[i]:
                token = ringkasan[i]
                if ringkasanUnigram[token] > 0 and manualUnigram[token] > 0:
                    ringkasanUnigram[token] -= 1
                    manualUnigram[token] -= 1
                    currentLCSScore += 1
        
        lcsScore += currentLCSScore
    
    print("LCS =", lcsScore)
    ringkasanWordCount = sum(len(s) for s in ringkasans)
    print("m =", ringkasanWordCount)
    manualWordCount = sum(len(s) for s in manuals)
    print("n =", manualWordCount)

    beta = 8
    precision = lcsScore / ringkasanWordCount
    recall = lcsScore / manualWordCount
    fmeasure = (1 + beta ** 2) * precision * recall / (recall + beta ** 2 * precision + 1e-7) + 1e-6

    f.write(str(precision) + ", " + str(recall) + ", " + str(fmeasure))

    return precision, recall, fmeasure

if __name__ == '__main__':

    # ringkasan = ringkas
    # print("ringkasan sistem")
    # print(ringkasan,"\n")

    # manual = gTruth
    # print("ringkasan manual")
    # print(manual,"\n")

    # print(getRouge_L([ringkasan], [manual]))

    cobaRingkasan = "kevinka"
    cobaManual = "kvinke"

    print(getRouge_L([cobaRingkasan], [cobaManual]))