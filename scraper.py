import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

DRIVER_PATH = 'chromedriver.exe'



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
    #driver.quit()
    return
   

def getAnswers():

    options = Options()
    #options.headless = True
    options.add_argument("--window-size=800,600")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    # old https://www.nytimes.com/crosswords/game/mini/2016/06/01
    # uptodate https://www.nytimes.com/crosswords/game/mini
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

def findInputPutKey(getUrl, inputId,acClues,dnClues):

    options2 = Options()
    options2.headless = True
    options2.add_argument("--window-size=800,600")

    driver2 = webdriver.Chrome(options=options2, executable_path=DRIVER_PATH)


    driver2.get(getUrl)
    resList = [[]]*(len(acClues)+len(dnClues))
    

    ind = 0
    for clue in acClues:
        print("Searching for ==> ", clue.text,"\n")
        driver2.find_element_by_id(inputId).send_keys(clue.text)
        time.sleep(0.3)
        btn = driver2.find_element_by_id("search-button")
        btn.click()
        time.sleep(1.2)
        rList = []

        words = driver2.find_elements_by_class_name("item")
        try:
            for i in range(0,10):
                if(len(words[i].text) <= 5):
                    #print(words[i].text)
                    rList.append(words[i].text)
        except:
            pass
        #print("\n")
        resList[ind] = rList
        ind = ind + 1
        btn = driver2.find_element_by_id("clear-search-button")
        btn.click()
        time.sleep(1)
    

    for clue in dnClues:
        print("Searching for ==> ",clue.text,"\n")
        driver2.find_element_by_id(inputId).send_keys(clue.text)
        time.sleep(0.3)
        btn = driver2.find_element_by_id("search-button")
        btn.click()
        time.sleep(1.2)
        rList = []
        words = driver2.find_elements_by_class_name("item")
        try:
            for i in range(0,10):
                if(len(words[i].text) <= 5):
                    #print(words[i].text)
                    rList.append(words[i].text)
        except:
            pass
        resList[ind] = rList
        ind = ind + 1
        #print("\n")
        btn = driver2.find_element_by_id("clear-search-button")
        btn.click()
        time.sleep(1)

    driver2.quit()
    return resList
    