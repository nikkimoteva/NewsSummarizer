from newsapi import NewsApiClient

class NewsArticle:
    def __init__(self, news_api, country, tone = 0):
        self.title = ""
        self.country = ""
        self.description = ""
        self.url = ""
        self.tone = 0
        self.lang = ""
        self.SetTitle(news_api['title'])
        self.SetCountry(country)
        self.SetDescription(news_api['body'])
        self.SetURL(news_api['url'])
        self.SetTone(tone) 
        self.SetLang(news_api['lang'][:2])

    def GetBody(self, news_api):
        return news_api.get_top_headlines()['articles']
    
    def SetTitle(self, title):
        self.title = title
    def GetTitle(self):
        return self.title
    
    def SetCountry(self, country):
        self.country = country
    def GetCountry(self):
        return self.country
    
    def SetDescription(self, description):
        self.description = description
    def GetDescription(self):
        return self.description
    
    def SetURL(self, url):
        self.url = url
    def GetUrl(self):
        return self.url

    def SetTone(self, tone):
        self.tone = tone
    def GetTone(self):
        return self.tone

    def SetLang(self, lang):
        self.lang = lang
    def GetLang(self):
        return self.lang

