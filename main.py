from urllib.request import urlopen as urlRequest
import bs4
from bs4 import BeautifulSoup as soup
import scraper
import requests
from datetime import date
from datetime import datetime

from tkinter import *
#import Tkinter as Tk

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
    today = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return today

def addAcrossCluesCnv(canvas, acClues, acIndexes):
    L = Label(canvas, text="Across Clues",fg="red",font = "Verdana 10 bold")
    L.pack()
    
    for i in range(len(acClues)):
         L = Label(canvas, text=acIndexes[i].text + " " + acClues[i].text)
         L.pack()
    print()

def addDownCluesCnv(canvas,dwClues,dwIndexes):
    L = Label(canvas, text="Down Clues",fg="red",font = "Verdana 10 bold")
    L.pack()

    for i in range(len(dwClues)):
         L = Label(canvas, text=dwIndexes[i].text + " " + dwClues[i].text) 
         L.pack()
    print()

    


def main():

    pageContent = scraper.getPageContent(PUZZLE_URL) # getting everything from website
    pageParsed = scraper.parseContent(pageContent) # page content is parsed

    #get clues and indexes
    clues = scraper.getAllOl(pageParsed,"ClueList-list--2dD5-") # found all clue container
    acrossClues = scraper.getAllSpan(clues[0],"Clue-text--3lZl7") # found all across clues
    acrossIndexes = scraper.getAllSpan(clues[0],"Clue-label--2IdMY")  # found all across clue indexes
    downClues = scraper.getAllSpan(clues[1],"Clue-text--3lZl7") # found all down clues
    downIndexes = scraper.getAllSpan(clues[1],"Clue-label--2IdMY")  # found all down clue indexes

    showAcrossClues(acrossClues,acrossIndexes)
    showDownClues(downClues,downIndexes)

    print(getDate())


    #GUI part
    master = Tk()

    #puzzle canvas
    puzzleGrid = Canvas(master, width=7*PUZZLE_SIDE_LENGTH, height=6*PUZZLE_SIDE_LENGTH)
    puzzleGrid.pack(side="left",padx=15,pady=15)
    answers = [['a','b','c','d','e'],['f','g','h','i','j'],['k','l','m','n','o'],['p','q','r','s','t'],['u','v','w','x','y']]
    puzzle = [[11, 12, 5, 2, 0], [0, 15, 6, 10, 0], [10, 0, 12, 5, 2], [12, 15, 8, 6, 1], [5, 0, 9, 5, 2]]

    # clues canvas
    cluesCnv = Canvas(master, width=300, height=300)
    cluesCnv.pack(side = "right",padx=15,pady=15)
   
    #drawing the grid    
    for i in range(0, 5):

        for j in range(0, 5):

            #add label inside boxes
            if(puzzle[j][i] != 0):
                L = Label(puzzleGrid, text=str(puzzle[j][i])).place(x = i*100+5,  y = j*100+5) 
            
            if(puzzle[j][i] != 0):
                L = Label(puzzleGrid, text=str(answers[j][i]),font = "Times").place(x = i*100+50,  y = j*100+50) 
            
            if (puzzle[i][j]==0):
                puzzleGrid.create_rectangle(j*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH, j*100+100, i*100+100, fill="black")
                
            
                

    #Creates all vertical lines at intervals of PUZZLE_SIDE_LENGTH
    for i in range(0, 6, 1):
        puzzleGrid.create_line([(i*100, 0), (i*PUZZLE_SIDE_LENGTH, 5*PUZZLE_SIDE_LENGTH)], tag='table_line')
        

    # Creates all horizontal lines at intervals of PUZZLE_SIDE_LENGTH
    for i in range(0, 6, 1):
        puzzleGrid.create_line([(0, i*100), (5*PUZZLE_SIDE_LENGTH, i*PUZZLE_SIDE_LENGTH)], tag='table_line')
    
    timeLabel = Label(puzzleGrid, text= "Group Name : ASOFT\nDate and Time : " + getDate()).place(x = 510,  y = 460) 
    #timeLabel.pack()


    #add clues to the canvas
    addAcrossCluesCnv(cluesCnv,acrossClues,acrossIndexes)
    addDownCluesCnv(cluesCnv,downClues,downIndexes)


    mainloop()

    



main()