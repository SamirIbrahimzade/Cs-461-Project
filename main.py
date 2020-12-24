from urllib.request import urlopen as urlRequest
import bs4
from bs4 import BeautifulSoup as soup
import scraper
import search
import requests
from datetime import date
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
#import Tkinter as Tk
import copy

class matrix_cell:
    def __init__(self, number, letter):
        self.number = number
        self.letter = letter

# old https://www.nytimes.com/crosswords/game/mini/2016/06/01
# uptodate https://www.nytimes.com/crosswords/game/mini
PUZZLE_URL = "https://www.nytimes.com/crosswords/game/mini"
PUZZLE_SIDE_LENGTH = 100

def showAcrossClues(acClues,acIndexes):
    print("Printing across clues")
    for i in range(len(acClues)):
        print("", acIndexes[i].text, " ", acClues[i].text)
    print()

def showDownClues(dwClues,dwIndexes):
    print("Printing down clues")
    for i in range(len(dwClues)):
        print("", dwIndexes[i].text, " ", dwClues[i].text)
    print()

def getDate():
    print("Retrieving current date and time of the system ")
    today = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return today

def addAcrossCluesCnv(canvas, acClues, acIndexes):

    L = Label(canvas, text="Across Clues",fg="red",font = "Verdana 10 bold").pack(fill='both')


    for i in range(len(acClues)):
         L = Label(canvas, text=acIndexes[i].text + ") " + acClues[i].text, anchor='w').pack(fill='both')
    print()

def addDownCluesCnv(canvas,dwClues,dwIndexes):
    L = Label(canvas, text="Down Clues",fg="red",font = "Verdana 10 bold").pack(fill='both')

    for i in range(len(dwClues)):
         L = Label(canvas, text=dwIndexes[i].text + ") " + dwClues[i].text, anchor='w').pack(fill='both')
    print()

def findCellWithNoReturnCol( matrix, x ):

    for i in range(0,5):
        for j in range (0,5):
            if matrix[i,j].number == x:
                return j

def findCellWithNoReturnRow(matrix,  x ):

    for i in range(0,5):
        for j in range (0,5):
            if matrix[i,j].number == x:
                return i

def findCellInfoWithNumber(matrix, x):

    for i in range(0,5):
        for j in range (0,5):
            if matrix[i,j].number == x:
                return i,j,int(x)

def callSearch(isAcross,lst):

    word = ""

    for element in lst:
        word = word + element[0]

    if(isAcross):
        resDataMuse2 = search.detailedSearchDataMuse(word)
        
    else:
        resDataMuse2 = search.detailedSearchDataMuse(word)

    return resDataMuse2

# finding intersection of answers to compare
def findIntersectedCells(matrix, acrossBeginningInfo, downBeginningInfo):

    result = {}

    for i in range(0,5):
        for j in range(0,5):
            if(int(matrix[i,j].number) < 0):    # if current cell is black
                result[i,j] = (-1,-1,-1,-1,"-1")
            else:
                for p in range(len(acrossBeginningInfo)):
                    if(acrossBeginningInfo[p][0] == i):
                        for q in range(len(downBeginningInfo)):
                            if(downBeginningInfo[q][1] == j):
                                # storing results in tuples with 4 elements
                                # (0) across answer number that cell belongs to
                                # (1) across distance that cell is far from beginning of word
                                # (2) down answer number that cell belongs to
                                # (3) down distance that cell is far from beginning of word
                                result[i,j] = (acrossBeginningInfo[p][2], (j - acrossBeginningInfo[p][1]), downBeginningInfo[q][2], (i - downBeginningInfo[q][0]), "-1")

    return result

def compareAnswerCandidatesFirstIteration(resDataMuse, intersectionInfo):

    across = resDataMuse[0:5]
    down = resDataMuse[5:10]

    # first getting rid of answer candidates that are not in the same size with answers (bigger than length 5 gotten rid of before)

    # index of those words are not in the same length of the answers
    acrossDeleteIndexes = []
    downDeleteIndexes = []

    # finding indexes for answer candidates that are not same length with answer
    for i in range(len(across)):
        for j in range(len(across[i])):
            if(acrossLengths[i] != len(across[i][j])):
                acrossDeleteIndexes.append((i,j))
    # indexes are chosen and deleted from search list
    for i in reversed(range(len(acrossDeleteIndexes))):
        p = acrossDeleteIndexes[i][0]
        q = acrossDeleteIndexes[i][1]
        del across[p][q]

    # same process for down
    for i in range(len(down)):
        for j in range(len(down[i])):
            if(downLengths[i] != len(down[i][j])):
                downDeleteIndexes.append((i,j))
    # indexes are chosen and deleted from search list
    for i in reversed(range(len(downDeleteIndexes))):
        p = downDeleteIndexes[i][0]
        q = downDeleteIndexes[i][1]
        del down[p][q]

    # storing answers with index of clues instead of 0,1,2,3,4
    newAcross = [[]]*10
    newDown = [[]]*10
    for i in range(0,10):
        for j in range(len(acrossBeginningInfo)):
            if(acrossBeginningInfo[j][2] == i):
                newAcross[i] = across[j]

    for i in range(0,10):
        for j in range(len(downBeginningInfo)):
            if(downBeginningInfo[j][2] == i):
                newDown[i] = down[j]

    possibleMatches = []
    #return newAcross, newDown
    
    for k in range(len(newAcross)):
        if(len(newAcross[k]) > 0 ):
            for t in range(0,5):
                if(acrossBeginningInfo[t][2] == k):
                    p = acrossBeginningInfo[t][0]
                    q = acrossBeginningInfo[t][1]
            temp = "-1"
            for x in range(q,5):
                acrossBeginIndex, acrossDistance, downBeginIndex, downDistance, temp = intersectionInfo[p, x]

                for i in range(len(newAcross[acrossBeginIndex])):
                    for j in range(len(newDown[downBeginIndex])):
                        if(newAcross[acrossBeginIndex][i][acrossDistance] == newDown[downBeginIndex][j][downDistance]):
                            print(newAcross[acrossBeginIndex][i], " ", newDown[downBeginIndex][j])
                            possibleMatches.append((newAcross[acrossBeginIndex][i], newDown[downBeginIndex][j]))
                            for y in range(0,5):
                                if(downBeginningInfo[y][2] == downBeginIndex):
                                    a = downBeginningInfo[y][0]
                                    b = downBeginningInfo[y][1]

                                print()

                            newMatchPossibility = ((p,q), newAcross[acrossBeginIndex][i], (a,b), newDown[downBeginIndex][j], (acrossBeginIndex,downBeginIndex))



    
                            compareAnswerCandidatesNewIteration(newAcross, newDown, intersectionInfo, newMatchPossibility)
    
    

    print()
    return
    

def compareAnswerCandidatesNewIteration(newAcross, newDown, intersectionInfo, newMatchPossibility):

    print(newMatchPossibility)
    # newIntersectionInfo = copy.deepcopy(intersectionInfo)
    # for i in range(newMatchPossibility[0][1],len(newMatchPossibility[1])):
    #     x = newMatchPossibility[0][0]
    #     newIntersectionInfo[x,i][4] = newMatchPossibility[1][i]

    # for i in range(len(newAcross)):
    #     if(len(newAcross[i]) > 0):
    #         for j in range(len(newAcross[i])):
    #             #print(newAcross[i][j])
    #             for k in range(len(newAcross[i][j])):
    #                 x = newMatchPossibility[0][0]
    #                 y = newMatchPossibility[0][1]
    #                 nfinAcross.append((newAcross[i][j][k], (j,k)))
    #
    # for i in range(len(newDown)):
    #     if(len(newDown[i]) > 0):
    #         for j in range(len(newDown[i])):
    #             #print(newAcross[i][j])
    #             for k in range(len(newDown[i][j])):
    #                 x = newMatchPossibility[0][0]
    #                 y = newMatchPossibility[0][1]
    #                 nfinDown.append((newDown[i][j][k], (j,k)))

    nfinAcross.append((newMatchPossibility[4][0],newMatchPossibility[1]))
    nfinDown.append((newMatchPossibility[4][1], newMatchPossibility[3]))

    print()


    return

# list to store answers to check length
acrossBeginningInfo = []
downBeginningInfo = []

finAcross = [[]] * 10
finDown = [[]] * 10
nfinAcross = []
nfinDown = []

acrossLengths = [0,0,0,0,0]
downLengths = [0,0,0,0,0]


def main():

    pageContent = scraper.getPageContent(PUZZLE_URL) # getting everything from website
    pageParsed = scraper.parseContent(pageContent) # page content is parsed

    #get clues and indexes
    clues = scraper.getAllOl(pageParsed,"ClueList-list--2dD5-") # found all clue container
    acrossClues = scraper.getAllSpan(clues[0],"Clue-text--3lZl7") # found all across clues
    print("Detected all across clues ")
    acrossIndexes = scraper.getAllSpan(clues[0],"Clue-label--2IdMY")  # found all across clue indexes
    print("Detected all across clue indexes ")
    downClues = scraper.getAllSpan(clues[1],"Clue-text--3lZl7") # found all down clues
    print("Detected all down clue indexes ")
    downIndexes = scraper.getAllSpan(clues[1],"Clue-label--2IdMY")  # found all down clue indexes
    print("Detected all down clue indexes ")
    print()
    showAcrossClues(acrossClues,acrossIndexes)
    showDownClues(downClues,downIndexes)
    print("Retrieved date and time is " + getDate())

    #scraper.closeDriver()
    

    print()

    #resRevDict = search.searchRevDict(acrossClues,downClues)
    #resGoogle = search.searchGoogle(acrossClues,acrossIndexes,downClues,downIndexes)

    resDataMuse = search.searchDataMuse(acrossClues,acrossIndexes,downClues,downIndexes)
    #resMerriam = search.searchMerriam(acrossClues,acrossIndexes,downClues,downIndexes)

    #print("Result RevDict",resRevDict,"\n\n")
    #print("Result Google",resGoogle,"\n\n")
    print("Result DataMuse",resDataMuse,"\n\n")
    #print("Result Merriam",resMerriam,"\n\n")

    

   
    # print("google")
    # for i in range(len(resGoogle)):
    #     print(resGoogle[i])
    

    #print("\n\ndatamuse")
    #for i in range(len(resDataMuse)):
    #    print(resDataMuse[i])

    # print("\n\nmerriam")
    # for i in range(len(resMerriam)):
    #     print(resMerriam[i])

    #print("\n\nrevDict")
    # for i in range(len(resRevDict)):
    #     print(resMerriam[i])

    print("datamuse ", resDataMuse[0] )
    
    
    finList = [[]]*(len(acrossClues)+len(downClues))
    #
    for i in range (len(acrossClues)+len(downClues)):
         finList[i] = resDataMuse[i] #+ resRevDict[i] + resMerriam[i]
    print(finList)


    ############################################################################################################
    print("Drawing the GUI")
    #GUI part
    master = Tk()
    master.title("ASOFT PUZZLE SOLVER")
    master.configure()


    #puzzle canvas
    print("Creating the puzzle canvas")

    #title
    titleGrid = Canvas(master, width=6*PUZZLE_SIDE_LENGTH, height=PUZZLE_SIDE_LENGTH)
    titleGrid.pack(side='top',padx=15,pady=15)
    tittleLabel = Label(titleGrid, text="NYT Mini Crossword Puzzle",font = "Times 36 bold").place(x = 0,  y = 0)


    puzzleGrid = Canvas(master, width=5*PUZZLE_SIDE_LENGTH, height=6*PUZZLE_SIDE_LENGTH)
    puzzleGrid.pack(side="left",padx=15,pady=15)
    puzzleGrid.outline='black'
    puzzleGrid.width=2
    answers = [['a','b','c','d','e'],['f','g','h','i','j'],['k','l','m','n','o'],['p','q','r','s','t'],['u','v','w','x','y']]
    puzzle = [[11, 12, 5, 2, 0], [0, 15, 6, 10, 0], [10, 0, 12, 5, 2], [12, 15, 8, 6, 1], [5, 0, 9, 5, 2]]

    newPuzzleGrid = Canvas(master, width=5*PUZZLE_SIDE_LENGTH, height=6*PUZZLE_SIDE_LENGTH)
    newPuzzleGrid.pack(side='right',padx=15,pady=15)
    #newPuzzleGrid.outline='black'
    #newPuzzleGrid.width=2

    # clues canvas
    print("Creating the clue canvas")
    cluesCnv = Canvas(master, width=4*PUZZLE_SIDE_LENGTH, height=4*PUZZLE_SIDE_LENGTH)
    cluesCnv.pack(side = "top",padx=15,pady=15)

    print()
    print("Starting the process of retrieving answers !")
    matrix, across_clue, horiz_clue = scraper.getAnswers(PUZZLE_URL)

    # getting indexes of answer beginnings and storing them
    for i in range(len(acrossIndexes)):
        acrossBeginningInfo.append(findCellInfoWithNumber(matrix, acrossIndexes[i].text))
    for i in range(len(downIndexes)):
        downBeginningInfo.append(findCellInfoWithNumber(matrix,downIndexes[i].text))

    # getting lengths of across answers
    # selecting each answer beginning (first letter) info and going across counting every white cell
    for i in range(len(acrossBeginningInfo)):
        rowNo= acrossBeginningInfo[i][0]
        colNo = acrossBeginningInfo[i][1]
        for j in range(colNo, 5):
            if(int(matrix[rowNo,j].number) >= 0):
                acrossLengths[i] += 1

    # getting lengths of down answers
    # selecting each answer beginning (first letter) info and going down counting every white cell
    for i in range(len(downBeginningInfo)):
        rowNo = downBeginningInfo[i][0]
        colNo = downBeginningInfo[i][1]
        for j in range(rowNo, 5):
            if (int(matrix[j, colNo].number) >= 0):
                downLengths[i] += 1

    # intersectionInfo[i,j] = (leftMostNumber, distanceFromLeft, topMostNumber, distanceFromTop) (explained in detail in findIntersectedCells function)
    intersectionInfo = findIntersectedCells(matrix, acrossBeginningInfo, downBeginningInfo)
    # for i in range(0,5):
    #     for j in range (0,5):
    #         print(intersectionInfo[i,j])

    #na,nd = 
    compareAnswerCandidatesFirstIteration(resDataMuse, intersectionInfo)


    print()
    #drawing the grid    
    print("Drawing the grid of the puzzle and filling the black squares")
    for i in range(0, 5):

        for j in range(0, 5):

            #add label inside boxes
            if(matrix[i,j].number != 0 and matrix[i,j].number != -8):
                L = Label(puzzleGrid, text=str(matrix[i,j].number), font = "Times 12").place(x = j*PUZZLE_SIDE_LENGTH+5,  y = i*PUZZLE_SIDE_LENGTH+5)
                L = Label(newPuzzleGrid, text=str(matrix[i,j].number), font = "Times 12").place(x = j*PUZZLE_SIDE_LENGTH+5,  y = i*PUZZLE_SIDE_LENGTH+5)

            
            #if(matrix[i,j].number != -8):
            #    L = Label(puzzleGrid, text=str(answers[j][i]),font = "Times").place(x = i*100+50,  y = j*100+50)
            
            if (matrix[i,j].number==-8):
                puzzleGrid.create_rectangle(j*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH, j*PUZZLE_SIDE_LENGTH+PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH+PUZZLE_SIDE_LENGTH, fill="black")
                newPuzzleGrid.create_rectangle(j*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH, j*PUZZLE_SIDE_LENGTH+PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH+PUZZLE_SIDE_LENGTH, fill="black")

                

    puzzleGrid.create_line(2, 0, 2, 5*PUZZLE_SIDE_LENGTH, fill="black", width=2)
    puzzleGrid.create_line(0, 2, 5*PUZZLE_SIDE_LENGTH, 2, fill="black", width=2)

    newPuzzleGrid.create_line(2, 0, 2, 5*PUZZLE_SIDE_LENGTH, fill="black", width=2)
    newPuzzleGrid.create_line(0, 2, 5*PUZZLE_SIDE_LENGTH, 2, fill="black", width=2)
    

    #Creates all vertical lines at intervals of PUZZLE_SIDE_LENGTH
    for i in range(0, 6, 1):
        puzzleGrid.create_line([(i*PUZZLE_SIDE_LENGTH, 0), (i*PUZZLE_SIDE_LENGTH, 5*PUZZLE_SIDE_LENGTH)], tag='table_line')
        newPuzzleGrid.create_line([(i*PUZZLE_SIDE_LENGTH, 0), (i*PUZZLE_SIDE_LENGTH, 5*PUZZLE_SIDE_LENGTH)], tag='table_line')


    # Creates all horizontal lines at intervals of PUZZLE_SIDE_LENGTH
    for i in range(0, 6, 1):
        puzzleGrid.create_line([(0, i*PUZZLE_SIDE_LENGTH), (5*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH)], tag='table_line')
        newPuzzleGrid.create_line([(0, i*PUZZLE_SIDE_LENGTH), (5*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH)], tag='table_line')

    print("Printing the time label to the gui")
    timeLabel = Label(newPuzzleGrid, text= "Group Name : ASOFT\nDate and Time : " + getDate()).place(x = 260,  y = 560)
    #timeLabel.pack()

    print("Adding clues to the canvas")
    #add clues to the canvas
    addAcrossCluesCnv(cluesCnv,acrossClues,acrossIndexes)
    addDownCluesCnv(cluesCnv,downClues,downIndexes)



    print("Printing answers to the both gui and terminal")


    across = [0]*10
    down = [0]*10

    Nacross = [0] * 10
    Ndown = [0] * 10

    #print(na,"\n\n\n",nd,"\n\n\n")
    print(nfinAcross,nfinDown)

    for i in range(len(down)):
        for j in range(len(nfinDown)):
            if(nfinDown[j][0] == i):
                down[i] = nfinDown[j][1]

    for i in range(len(across)):
        for j in range(len(nfinAcross)):
            if(nfinAcross[j][0] == i):
                across[i] = nfinAcross[j][1]

    for i in range(len(acrossBeginningInfo)):
        print()

    print("Across info",acrossBeginningInfo)
    print("Down info",downBeginningInfo)
    
    print("across")
    print(across)

    print("down")
    print(down)

    print()

    for i in range(0, 5):
        ind = 0
        for j in range(0, 5):

            #add label inside boxes
            print(matrix[j,i].number)
            if(matrix[j,i].number != -8):
                word = down[downBeginningInfo[i][2]]
                print(word)
                if(word != 0 and (ind < len(word))):
                    
                    L = Label(newPuzzleGrid, text=str(word[ind]).upper(),font = "Times 42 bold").place(x = i*PUZZLE_SIDE_LENGTH+25,  y = j*PUZZLE_SIDE_LENGTH+20)
                    ind = ind + 1

    for i in range(0, 5):
        ind = 0
        for j in range(0, 5):

            #add label inside boxes
            if(matrix[i,j].number != -8):
                word = across[acrossBeginningInfo[i][2]]
                
                if(word != 0):
                    
                    L = Label(newPuzzleGrid, text=str(word[ind].upper()),font = "Times 42 bold").place(x = j*PUZZLE_SIDE_LENGTH+25,  y = i*PUZZLE_SIDE_LENGTH+20)
                    ind = ind + 1









    # across[1] = ('C',(0,1) ), ('L',(0,2) ), ('U',(0,3) ), ('B',(0,4) )
    # across[5] = ('L',(1,1) ), ('A',(1,2) ), ('N',(1,3) ), ('E',(1,4) )
    # across[6] = ('M',(2,0) ), ('A',(2,1) ), ('Y',(2,2) ), ('B',(2,3) ), ('E',(2,4) )
    # across[7] = ('O',(3,0) ), ('R',(3,1) ), ('E',(3,2) ), ('O',(3,3) )
    # across[8] = ('M',(4,0) ), ('A',(4,1) ), ('R',(4,2) ), ('X',(4,3) )
    #
    # down[1] = ('C',(0,0) ), ('L',(1,0) ), ('A',(2,0) ), ('R',(3,0) ), ('A',(4,0) )
    # down[2] = ('L',(0,1) ), ('A',(1,1) ), ('Y',(2,1) ), ('E',(3,1) ), ('R',(4,1) )
    # down[3] = ('U',(0,2) ), ('N',(1,2) ), ('B',(2,2) ), ('O',(3,2) ), ('X',(4,2) )
    # down[4] = ('B',(0,3) ), ('E',(1,3) ), ('E',(2,3) )
    # down[6] = ('M',(2,4) ), ('O',(3,4) ), ('M',(4,4) )

    print("Down")
    for i in range (len(across_clue)):
        print(across_clue[i].getText(), " ---> ")
        colNo = findCellWithNoReturnCol(matrix,across_clue[i].getText()[0])
        for j in range(0,5):
            #L = Label(puzzleGrid, text=str(matrix[j,colNo].letter),font = "Times").place(x = i*100+50,  y = j*100+50)
            print( matrix[j,colNo].letter, end = "" )
        print("")

    # print(across[5][2])
    # index = 0
    # for i in range(10):
    #     if(across[i] != 0):
    #         for j in range(5):
    #             try:
    #                 L = Label(newPuzzleGrid, text=str(across[i][j][0]),font = "Times 42 bold").place(x = across[i][j][1][1]*PUZZLE_SIDE_LENGTH+25,  y = across[i][j][1][0]*PUZZLE_SIDE_LENGTH+20)
    #             except:
    #                 pass
    #             index = index + 1

    print("\nAcross")
    for i in range (len(horiz_clue)):
        print(horiz_clue[i].getText(), " ---> ")
        rowNo = findCellWithNoReturnRow(matrix,horiz_clue[i].getText()[0])
        nl = []

        for j in range(0,5):
            if(str(matrix[rowNo, j].letter) != " "):
                L = Label(puzzleGrid, text=str(matrix[rowNo, j].letter),font = "Times 42 bold").place(x = j*PUZZLE_SIDE_LENGTH+25,  y = i*PUZZLE_SIDE_LENGTH+20)
                ans = ('',(i,j) )
                nl.append(ans)
            Nacross[rowNo] = nl 
            #Nacross[rowNo] = nl
            print (matrix[rowNo, j].number,  "*********\n")
            print (rowNo,"************\n")
        print("")
    A = "KEYS" #across 5
    B = "KEYS"

    print(Nacross)


    #resDataMuse2 = search.detailedSearchDataMuse("What a black three-leaf clover represents","?lu?")
    #resDataMuse2 = search.detailedSearchDataMuse("mayb?")
    #print(resDataMuse2)



    # calling detailed search method example
    #callSearch(True,across[6])
    print()
    print()
    print()

    print("across")
    print(across)

    print("down")
    print(down)

    mainloop()
    

main()