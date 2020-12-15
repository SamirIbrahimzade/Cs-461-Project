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


    '''
    print("Drawing the gui")
    #GUI part
    master = Tk()
    master.configure(background='gray')


    #puzzle canvas
    print("Creating the puzzle canvas")
    puzzleGrid = Canvas(master, width=7*PUZZLE_SIDE_LENGTH, height=6*PUZZLE_SIDE_LENGTH)
    puzzleGrid.pack(side="left",padx=15,pady=15)
    answers = [['a','b','c','d','e'],['f','g','h','i','j'],['k','l','m','n','o'],['p','q','r','s','t'],['u','v','w','x','y']]
    puzzle = [[11, 12, 5, 2, 0], [0, 15, 6, 10, 0], [10, 0, 12, 5, 2], [12, 15, 8, 6, 1], [5, 0, 9, 5, 2]]
        
    # clues canvas
    print("Creating the clue canvas")
    cluesCnv = Canvas(master, width=300, height=300)
    cluesCnv.pack(side = "right",padx=15,pady=15)

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
                L = Label(puzzleGrid, text=str(matrix[i,j].number), font = "Times 12").place(x = j*100+5,  y = i*100+5)
            
            #if(matrix[i,j].number != -8):
            #    L = Label(puzzleGrid, text=str(answers[j][i]),font = "Times").place(x = i*100+50,  y = j*100+50)
            
            if (matrix[i,j].number==-8):
                puzzleGrid.create_rectangle(j*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH, j*100+100, i*100+100, fill="black")
                
            
                

    puzzleGrid.create_line(2, 0, 2, 500, fill="black", width=2)
    puzzleGrid.create_line(0, 2, 500, 2, fill="black", width=2)

    #Creates all vertical lines at intervals of PUZZLE_SIDE_LENGTH
    for i in range(1, 6, 1):
        puzzleGrid.create_line([(i*100, 0), (i*PUZZLE_SIDE_LENGTH, 5*PUZZLE_SIDE_LENGTH)], tag='table_line')


    # Creates all horizontal lines at intervals of PUZZLE_SIDE_LENGTH
    for i in range(1, 6, 1):
        puzzleGrid.create_line([(0, i*100), (5*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH)], tag='table_line')

    print("Printing the time label to the gui")
    timeLabel = Label(puzzleGrid, text= "Group Name : ASOFT\nDate and Time : " + getDate()).place(x = 510,  y = 460)
    #timeLabel.pack()

    print("Adding clues to the canvas")
    #add clues to the canvas
    addAcrossCluesCnv(cluesCnv,acrossClues,acrossIndexes)
    addDownCluesCnv(cluesCnv,downClues,downIndexes)

    
   
    print("Printing answers to the both gui and terminal")

    print("Across")
    for i in range (len(across_clue)):
        print(across_clue[i].getText(), end=" ---> ")
        colNo = findCellWithNoReturnCol(matrix,across_clue[i].getText()[0])
        for j in range(0,5):
            #L = Label(puzzleGrid, text=str(matrix[j,colNo].letter),font = "Times").place(x = i*100+50,  y = j*100+50)
            print( matrix[j,colNo].letter, end = "" )
        print("")
    
    print("\nDown")
    for i in range (len(horiz_clue)):
        print(horiz_clue[i].getText(), end=" ---> ")
        rowNo = findCellWithNoReturnRow(matrix,horiz_clue[i].getText()[0])
         
        for j in range(0,5):
            if(str(matrix[rowNo, j].letter) != " "):
                L = Label(puzzleGrid, text=str(matrix[rowNo, j].letter),font = "Times 42 bold").place(x = j*100+25,  y = i*100+20)
            print (matrix[rowNo, j].letter, end = "")
        print("")
    

   
    mainloop()
    '''
    scraper.closeDriver()

    resGoogle = search.searchGoogle(acrossClues,acrossIndexes,downClues,downIndexes)

    resDataMuse = search.searchDataMuse(acrossClues,acrossIndexes,downClues,downIndexes)
    print("Result",resGoogle)
    print("Result",resDataMuse)

main()