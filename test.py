from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests


def findCellWithNoReturnCol( x ):

    for i in range(0,5):
        for j in range (0,5):
            if matrix[i,j].number == x:
                return j

def findCellWithNoReturnRow( x ):

    for i in range(0,5):
        for j in range (0,5):
            if matrix[i,j].number == x:
                return i

DRIVER_PATH = 'chromedriver.exe'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.get("https://www.nytimes.com/crosswords/game/mini")
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span").click()
time.sleep(1) 
#driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button")
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div/span").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/span").click()

print("test")


html = driver.page_source

#print(html)
#driver.close()

soup = BeautifulSoup (html)



clueler =  soup.find("div", {"class": "layout"}).find("article", {"aria-label" : "Main Puzzle Layout"}).findAll("section")[2]

#print(clueler.getText())
across_clue = clueler.findAll("div")[1].findAll("li")
horiz_clue = clueler.findAll("div")[0].findAll("li")
print(across_clue[0].getText())
print("**************************************************************")
print(horiz_clue[0].getText())




class matrix_cell:
    def __init__(self, number, letter):
        self.number = number
        self.letter = letter

gler = soup.find(id = "xwd-board").find(role = "table").findAll("g")
x = 0
for i in range (0,5):
    for j in range (0,5):
        print(gler[x].getText())
        x += 1

#print("*/*/*/*/*/*/**/*\n",gler,"\n/*/*/*/*/*/*/*/*/*\n")


x = 0
matrix = {}

for i in range (0,5):
    for j in range (0,5):
        if(len(gler[x].getText()) == 0):
            matrix[i,j] = matrix_cell(-8," ")
        elif(len(gler[x].getText()) == 2):
            matrix[i,j] = matrix_cell(0, gler[x].getText()[0])
        elif(len(gler[x].getText()) == 3):
            matrix[i,j] = matrix_cell(gler[x].getText()[0], gler[x].getText()[1])

        x += 1 




for i in range(0,5):
    for j in range (0,5):
        print(matrix[i,j].number, end = "")
    print("")

#print("*/*/*/*/*/*/**/*\n",across_clue,"\n/*/*/*/*/*/*/*/*/*\n")

for i in across_clue:
    print(i.getText(), end=" ---> ")
    colNo = findCellWithNoReturnCol(i.getText()[0])
    for j in range(0,5):
        print( matrix[j,colNo].letter, end = "" )
    print("")

for i in horiz_clue:
    print(i.getText(), end =" ----> ")
    rowNo = findCellWithNoReturnRow(i.getText()[0])
    for j in range(0,5):
        print (matrix[rowNo, j].letter, end = "")
    print("")





#print(my_bs.getText())