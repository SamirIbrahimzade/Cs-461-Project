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

class matrix_cell:
    def __init__(self, number, letter):
        self.number = number
        self.letter = letter

PUZZLE_URL = "https://www.nytimes.com/crosswords/game/mini/"
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
    L = Label(canvas, text="Across Clues",fg="red",font = "Verdana 10 bold")
    L.pack()
    
    for i in range(len(acClues)):
         L = Label(canvas, text=acIndexes[i].text + ") " + acClues[i].text)
         L.pack()
    print()

def addDownCluesCnv(canvas,dwClues,dwIndexes):
    L = Label(canvas, text="Down Clues",fg="red",font = "Verdana 10 bold")
    L.pack()

    for i in range(len(dwClues)):
         L = Label(canvas, text=dwIndexes[i].text + ") " + dwClues[i].text)
         L.pack()
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

def callSearch(isAcross,lst):

    word = ""

    for element in lst:
        word = word + element[0]

    if(isAcross):
        resDataMuse2 = search.detailedSearchDataMuse(word)
        
    else:
        resDataMuse2 = search.detailedSearchDataMuse(word)

    return resDataMuse2

# list to store answers to check length
acrossInfo = []
downInfo = []

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
    '''
    resRevDict = search.searchRevDict(acrossClues,downClues)
    #resGoogle = search.searchGoogle(acrossClues,acrossIndexes,downClues,downIndexes)

    resDataMuse = search.searchDataMuse(acrossClues,acrossIndexes,downClues,downIndexes)
    resMerriam = search.searchMerriam(acrossClues,acrossIndexes,downClues,downIndexes)

    print("Result RevDict",resRevDict,"\n\n")
    #print("Result Google",resGoogle,"\n\n")
    print("Result DataMuse",resDataMuse,"\n\n")
    print("Result Merriam",resMerriam,"\n\n")

    

   
    print("google")
    for i in range(len(resGoogle)):
        print(resGoogle[i])
    

    print("\n\ndatamuse")
    for i in range(len(resDataMuse)):
        print(resDataMuse[i])

    print("\n\nmerriam")
    for i in range(len(resMerriam)):
        print(resMerriam[i])

    print("\n\nrevDict")
    for i in range(len(resRevDict)):
        print(resMerriam[i])

    print("datamuse ", resDataMuse[0] )

    print("across index info", acrossInfo)
    print("down index info", downInfo)

    print("across lengths ", acrossLengths)
    print("down lengths ", downLengths)
    
    
    finList = [[]]*(len(acrossClues)+len(downClues))

    for i in range (len(acrossClues)+len(downClues)):
        finList[i] = resDataMuse[i] + resMerriam[i]+ resRevDict[i]
    print(finList)
    '''
    
   
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
    matrix, across_clue, horiz_clue = scraper.getAnswers()

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

    across[1] = ('C',(0,1) ), ('L',(0,2) ), ('U',(0,3) ), ('B',(0,4) )
    across[5] = ('L',(1,1) ), ('A',(1,2) ), ('N',(1,3) ), ('E',(1,4) )
    across[6] = ('M',(2,0) ), ('A',(2,1) ), ('Y',(2,2) ), ('B',(2,3) ), ('E',(2,4) )
    across[7] = ('O',(3,0) ), ('R',(3,1) ), ('E',(3,2) ), ('O',(3,3) )
    across[8] = ('M',(4,0) ), ('A',(4,1) ), ('R',(4,2) ), ('X',(4,3) )

    down[1] = ('C',(0,0) ), ('L',(1,0) ), ('A',(2,0) ), ('R',(3,0) ), ('A',(4,0) )
    down[2] = ('L',(0,1) ), ('A',(1,1) ), ('Y',(2,1) ), ('E',(3,1) ), ('R',(4,1) )
    down[3] = ('U',(0,2) ), ('N',(1,2) ), ('B',(2,2) ), ('O',(3,2) ), ('X',(4,2) )
    down[4] = ('B',(0,3) ), ('E',(1,3) ), ('E',(2,3) )
    down[6] = ('M',(2,4) ), ('O',(3,4) ), ('M',(4,4) )

    print("Down")
    for i in range (len(across_clue)):
        print(across_clue[i].getText(), " ---> ")
        colNo = findCellWithNoReturnCol(matrix,across_clue[i].getText()[0])
        for j in range(0,5):
            #L = Label(puzzleGrid, text=str(matrix[j,colNo].letter),font = "Times").place(x = i*100+50,  y = j*100+50)
            print( matrix[j,colNo].letter, "" )
            if(ord(matrix[j,colNo].letter) != 32):
                downInfo.append((j,colNo))    # adding letters in answers if it's not whitespace to check length
                downLengths[j] += 1
        print("")

    print(across[5][2])
    index = 0
    for i in range(10):
        if(across[i] != 0):
            for j in range(5):
                try:
                    L = Label(newPuzzleGrid, text=str(across[i][j][0]),font = "Times 42 bold").place(x = across[i][j][1][1]*PUZZLE_SIDE_LENGTH+25,  y = across[i][j][1][0]*PUZZLE_SIDE_LENGTH+20)
                except:
                    pass
                index = index + 1
    
    print("\nAcross")
    for i in range (len(horiz_clue)):
        print(horiz_clue[i].getText(), " ---> ")
        rowNo = findCellWithNoReturnRow(matrix,horiz_clue[i].getText()[0])
         
        for j in range(0,5):
            if(str(matrix[rowNo, j].letter) != " "):
                 L = Label(puzzleGrid, text=str(matrix[rowNo, j].letter),font = "Times 42 bold").place(x = j*PUZZLE_SIDE_LENGTH+25,  y = i*PUZZLE_SIDE_LENGTH+20)
            print (matrix[rowNo, j].letter,  "")
            if(ord(matrix[rowNo, j].letter) != 32):
                acrossInfo.append((rowNo, j)) # adding letters in answers if it's not whitespace to check length
                acrossLengths[j] += 1
        print("")
    A = "KEYS" #across 5
    B = "KEYS"

    #resDataMuse2 = search.detailedSearchDataMuse("What a black three-leaf clover represents","?lu?")
    #resDataMuse2 = search.detailedSearchDataMuse("mayb?")
    #print(resDataMuse2)



    # calling detailed search method example
    #callSearch(True,across[6])

    mainloop()
    

main()