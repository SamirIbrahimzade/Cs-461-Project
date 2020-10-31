import requests
from bs4 import BeautifulSoup as soup


def getPageContent(url):

    pageContent = requests.get(url)

    return pageContent

def parseContent(pageContent):

    page = soup(pageContent.content, "html.parser")

    return page 

def getAllSpan(getFrom,className):

    result = getFrom.findAll("span", {"class": className})  

    return result

def getAllOl(getFrom,className):

    result = getFrom.findAll("ol", {"class": className})     

    return result