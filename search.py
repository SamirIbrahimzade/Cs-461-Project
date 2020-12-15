import requests

from bs4 import BeautifulSoup

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