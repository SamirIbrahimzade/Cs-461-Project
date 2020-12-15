import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

DRIVER_PATH = 'chromedriver.exe'

options = Options()
#options.headless = True
options.add_argument("--window-size=1800,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

class matrix_cell:
    def __init__(self, number, letter):
        self.number = number
        self.letter = letter


def getPageContent(url):
    print("Requesting page content from " + url)
    pageContent = requests.get(url)

    return pageContent

def parseContent(pageContent):
    print("Parsing the retrived page content with BeatifulSoup ")
    page = BeautifulSoup(pageContent.content, "html.parser")

    return page 

def getAllSpan(getFrom,className):

    result = getFrom.findAll("span", {"class": className})  

    return result

def getAllOl(getFrom,className):
    print("Detecting all clue containers ")
    result = getFrom.findAll("ol", {"class": className})     

    return result

def closeDriver():
    driver.quit()

def getAnswers():

    driver.get("https://www.nytimes.com/crosswords/game/mini")
    sleepTime = 1.5
    print("Connected to the https://www.nytimes.com/crosswords/game/mini")
    print("Waiting time between requests is " + str(sleepTime) + " seconds")
    print("Waiting " + str(sleepTime) + " seconds")

    time.sleep(sleepTime)

    print("----------------Clicking to the OK button----------------")
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div[2]/div[3]/div/article/div[2]/button/div/span").click()

    print("Waiting " + str(sleepTime) + " seconds")
    time.sleep(sleepTime)
    print("----------------Clicking to the REVEAL button----------------")
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/button").click()

    print("Waiting " + str(sleepTime) + " seconds")
    time.sleep(sleepTime)
    print("----------------Clicking to the PUZZLE button----------------")
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]/a").click()
    
    print("Waiting " + str(sleepTime) + " seconds")
    time.sleep(sleepTime)
    print("----------------Clicking to the REVEAL button----------------")
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/article/div[2]/button[2]/div/span").click()

    print("Waiting " + str(sleepTime) + " seconds")
    time.sleep(sleepTime*2)
    print("----------------Clicking to the CLOSE POP UP button----------------")
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/span").click()

    print("Retrieving and parsing the html including the answers")
    html = driver.page_source
    soup = BeautifulSoup (html, "html.parser")

    clueler =  soup.find("div", {"class": "layout"}).find("article", {"aria-label" : "Main Puzzle Layout"}).findAll("section")[2]

    #print(clueler.getText())
    across_clue = clueler.findAll("div")[1].findAll("li")
    horiz_clue = clueler.findAll("div")[0].findAll("li")
    #print(across_clue[0].getText())
    #print("**************************************************************")
    #print(horiz_clue[0].getText())

    gler = soup.find(id = "xwd-board").find(role = "table").findAll("g")



    x = 0
    for i in range (0,5):
        for j in range (0,5):
            #print(gler[x].getText())
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
    
    driver.quit()
    print("Closed the web browser driver")
    print("Returning the answers")
    return matrix, across_clue, horiz_clue
