from urllib.request import urlopen as urlRequest
import bs4
from bs4 import BeautifulSoup as soup
import scraper
import requests
from datetime import date

PUZZLE_URL = "https://www.nytimes.com/crosswords/game/mini/"

def showAcrossClues(acClues,acIndexes):
    print("Printing across clues")
    for i in range(len(acClues)):
        print("", acIndexes[i].text, " ", acClues[i].text)
    print()

def showDownClues(dwClues,dwIndexes):
    print("Printing across clues")
    for i in range(len(dwClues)):
        print("", dwIndexes[i].text, " ", dwClues[i].text)
    print()

def getDate():
    today = str(date.today())
    return today

    


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
    



main()