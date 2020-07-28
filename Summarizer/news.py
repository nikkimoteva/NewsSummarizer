from newsapi import NewsApiClient

class newsArticle:
    def __init__(self, news_api):
        self.title = ""
        self.author = ""
        self.description = ""
        self.url = ""
        self.setTitle(news_api['title'])
        self.setAuthor(news_api['author'])
        self.setDesc(news_api['content'])
        self.setURL(news_api['url'])

    def get_body(self, news_api):
        return news_api.get_top_headlines()['articles']
    
    def setTitle(self, title):
        self.title = title
    def get_title(self):
        return self.title
    
    def setAuthor(self, author):
        self.author = author
    def get_author(self):
        return self.author
    
    def setDesc(self, description):
        self.description = description
    def get_description(self):
        return self.description
    
    def setURL(self, url):
        self.url = url
    def get_url(self):
        return self.url

