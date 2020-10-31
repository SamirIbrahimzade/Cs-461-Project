from urllib.request import urlopen as urlRequest
import bs4
from bs4 import BeautifulSoup as soup

print("Cs 461 project")

def main():

    puzzleURL = "https://www.nytimes.com/crosswords/game/mini/"

    urlClient = urlRequest(puzzleURL)
    pageString = urlClient.read()       # getting everything from website
    urlClient.close()

    pageParsed = soup(pageString, "html.parser")    # page content is parsed

    clues = pageParsed.findAll("ol", {"class":"ClueList-list--2dD5-"})      # found all clue containers

    acrossClues = clues[0].findAll("span", {"class":"Clue-text--3lZl7"})    # found all across clues
    acrossIndexes = clues[0].findAll("span", {"class": "Clue-label--2IdMY"})  # found all across clue indexes

    downClues = clues[1].findAll("span", {"class":"Clue-text--3lZl7"})      # found all down clues
    downIndexes = clues[1].findAll("span", {"class":"Clue-label--2IdMY"})   # found all down clue indexes


    print("Printing across clues")
    for i in range(len(acrossClues)):
        print("", acrossIndexes[i].text, " ", acrossClues[i].text)
    print()

    print("Printing down clues")
    for i in range(len(downClues)):
        print("", downIndexes[i].text, " ", downClues[i].text)

    return 0





main()