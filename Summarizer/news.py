from newsapi import NewsApiClient

class newsArticle:
    def __init__(self, news_api, country):
        self.title = ""
        self.country = ""
        self.description = ""
        self.url = ""
        self.setTitle(news_api['title'])
        self.setCountry(country)
        self.setDesc(news_api['content'])
        self.setURL(news_api['url'])

    def get_body(self, news_api):
        return news_api.get_top_headlines()['articles']
    
    def setTitle(self, title):
        self.title = title
    def get_title(self):
        return self.title
    
    def setCountry(self, country):
        self.country = country
    def get_country(self):
        return self.country
    
    def setDesc(self, description):
        self.description = description
    def get_description(self):
        return self.description
    
    def setURL(self, url):
        self.url = url
    def get_url(self):
        return self.url

