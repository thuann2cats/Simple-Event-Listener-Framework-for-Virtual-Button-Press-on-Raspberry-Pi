import requests
import datetime

class NewsFeed:
    def __init__(self, topic= 'world', location= 'us'):                                
        url = 'https://newsapi.org/v2/top-headlines'
        api =  '807842cfbedf49b8ad89e103f3882335'
        self.topic = topic                  #Uses ' ' not " "
        self.location = location            #Country/Region
        params = {
            'apiKey': api,                  #API key
            'pageSize': 10,                 #How many articles to print
            'language': 'en',               #Language
            'q': self.topic,                #Topic/Interest
            'from': (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')       #Past 24 hours
        }
        self.response = requests.get(url, params=params)
        self.article = self.response.json()['articles']


        

    def speak(self):                
        for article in self.article:    
            print(article['title'])
    
    def getNewsSummary(self):
        res = ""
        for article in self.article:
            res += article['title'] + "\n"
        return res
    
    def update(self):
        self.article = self.response.json()['articles']
        
nf = NewsFeed(topic="world", location="US")
nf.update()
print(nf.getNewsSummary())