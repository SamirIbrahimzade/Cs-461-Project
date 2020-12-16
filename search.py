import requests
from bs4 import BeautifulSoup
import urllib, json
import requests
import scraper


# define punctuation
punctuations = '''0123456789çşığ!()-[]{};:'"\,<>./?@#$%^&*_~'''



def searchGoogle(acClues,acIndexes,dnClues,dnIndexes):
    resList = []

    for i in range(len(acClues)):
        google_words = set()
        
        clue = acClues[i].text.replace(" ", "+")

        request = requests.get('https://www.google.com/search?q={}&lr=lang_en'
        .format(clue))
        soup = BeautifulSoup(request.content, "html.parser")
        result_elements = soup.text

        for word in result_elements.split():
            google_words.add(word)


        # getting rid of from unnecessary chars
        mylist = []
        for word in google_words:
            no_punct = ""
            for char in word:
               if char not in punctuations:
                   no_punct = no_punct + char
            no_punct.lower()
            mylist.append(no_punct)
        google_words = mylist

        # Process word list
        #google_words = self.clear_google_words(google_words)
        google_words = list(filter(lambda x: len(x) <= 5, google_words))
        print("Google Search \nWord Count: " + str(len(google_words)))

    resList.append(google_words)
    return resList

def searchDataMuse(acClues,acIndexes,dnClues,dnIndexes):

    resList = []


    for i in range(len(acClues)):
        #print("", acIndexes[i].text, " ", acClues[i].text)

        query = acClues[i].text.replace(" ", "+")
        query = query.lower()

        request = requests.get('https://api.datamuse.com/words?ml={}'.format(query))

        respond = request.json()

        tList = []
        #for j in range(len(respond)):
        for j in range(5):
            tList.append(respond[j]['word'])
        resList.append(tList)


        #resList = list(filter(lambda x: len(x) == length, datamuse_words))
        #print("Datamuse Search \nWord Count: " + str(len(datamuse_words)))
    for i in range(len(dnClues)):
        #print("", acIndexes[i].text, " ", acClues[i].text)

        query = dnClues[i].text.replace(" ", "+")
        query = query.lower()

        request = requests.get('https://api.datamuse.com/words?ml={}'.format(query))

        respond = request.json()

        tList = []
        for item in respond:
            tList.append(item['word'])
        resList.append(tList)
    for i in range(len(resList)):
        resList[i] = list(filter(lambda x: len(x) <= 5, resList[i]))

    return resList


def searchMerriam(acClues,acIndexes,dnClues,dnIndexes):
    
    API_KEY = "dd09241d-bf89-4f78-8834-34dc6e0495c4"

    #for clue in acClues:
    #    print(clue.text.split())

    resList = [[]]*(len(acClues)+len(dnClues))

    ind = 0
    for clue in acClues:
        
        words = clue.text.split()
        rList = []

        if(len(words) <= 3):
            for word in words:

                URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
                URL = URL + word + "?key="+API_KEY
                
                

                try:
                    response = requests.get(URL)
                    #data = json.loads(response.read())
                    #print(word, ind)
                    #print (response.json()[0]['meta']['syns'][0])
                    
                    rList.append(response.json()[0]['meta']['syns'][0])
                    #resList[ind].append(response.json()[0]['meta']['syns'][0])
                    #print(rList,"\n\n")
                except:
                    pass
            resList[ind] = rList

            #print(rList,"\n",resList,'\n\n\n\n')
        ind = ind + 1

         
    for clue in dnClues:
        
        words = clue.text.split()
        rList = []

        if(len(words) <= 3):
            for word in words:

                URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
                URL = URL + word + "?key="+API_KEY
                
                

                try:
                    response = requests.get(URL)
                    #data = json.loads(response.read())
                    #print(word, ind)
                    #print (response.json()[0]['meta']['syns'][0])
                    
                    rList.append(response.json()[0]['meta']['syns'][0])
                    #resList[ind].append(response.json()[0]['meta']['syns'][0])
                    #print(rList,"\n\n")
                except:
                    pass
            resList[ind] = rList

            #print(rList,"\n",resList,'\n\n\n\n')
        ind = ind + 1
    

    return resList


def searchRevDict(acClues,dnClues):
    url = "https://reversedictionary.org/"
    
    resl = scraper.findInputPutKey(url, "query",acClues,dnClues)
    
    return resl
