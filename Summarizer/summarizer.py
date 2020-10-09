"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""
import sys
import nltk
import spacy
nlp = spacy.load("en_core_web_sm")
import re
import requests
from newsapi import NewsApiClient
from news import NewsArticle
from countries import *
from mongodbDAO import Mongo 
from MSTranslator import Translate
from ToneAnalyzer import ToneAnalyzer
from WordStem import Stemmer
from eventregistry import EventRegistry, QueryArticlesIter
from Keys import ERKey

 
# summarize the text in 500 letters or 5 sentences maximum.
def summary(headline, mdb, langFrom, langTo):
    # split the text into an array in order to analyze and de-abriviate
    description = headline.GetDescription()
    if not description: return
    description = Translate(langFrom, langTo, description)
    stemLanguages = ListOfSpecCountries('Languages.txt', 'LangMapStem.txt')
    rawTextArray = description.split(" ")
    stemsLang = ""
    stemmedDescription = rawTextArray
    for key, val in stemLanguages.items():
        if langFrom == key:
            stemsLang = val
            stemmedDescription = Stemmer(rawTextArray, str(val).lower())
    # txt_chg is used to analyze the text for summarization without the abriviations
    txt_chg = AbbriviationRemoval(rawTextArray)
    url = headline.GetUrl()
    title = Translate(langFrom, langTo, headline.GetTitle())
    if stemsLang == "":
        stemmedTitle = title
    else:
        stemmedTitle = Stemmer(title, stemsLang.lower())
    whyHow = WhyHow(stemmedTitle, txt_chg, stemmedDescription, langFrom, langTo)
    whoWhere = WhoWhere(url, description, langFrom, langTo)
    tone = ToneAnalyzer(description)
    mdb.InserInDB(headline.GetCountry(), title, url, whoWhere, whyHow, tone)
    print('title: ' + title +
          '\nurl: ' + url + 
          '\nWho/When/Where: ' + whoWhere + 
          '\nSummary: ' + whyHow +
          '\nTone: ' + str(tone))


# make sure that you uncode the abbriviation, so the analyzer won't get confused:
# eg. sentence ending when reached Mr. ; won't = would not
def AbbriviationRemoval(txt): 
    abr = {"I'm": "I am", "Mr." : "Mister", "Ms." : "Miss", "Mrs.": "Missus", "don't": "do not", "he's": "he is",
            "U.S." : "United States", "U.S.A" : "United States of America", "U.A.E" : "United Arab Emirates"}
    for i in range(len(txt)):
        if txt[i] in abr:
            txt[i] = abr[txt[i]]
    return txt

def WhoWhere(url, article, lang_from, lang_to):
    doc = nlp(article)
    names = ""
    for ent in doc.ents:
        entRemovedExtraChars = re.sub(r'\W- +', "", str(ent))
        if ent == doc.ents[-1]:
            names+= entRemovedExtraChars + '.'
        else:
            names += entRemovedExtraChars + ", "
    namesTranslated = Translate(lang_from, lang_to, names)
    return namesTranslated

# article is an array. returns the summarized article
def WhyHow(title, article, stemmed, lang_from, lang_to):
    summaryTitle = RemoveExtraWords(title)
    # without white space
    array_title = summaryTitle.split()
    # sentenceArrayNoPeriod = ' '.join(map(str, article)).split(".")
    sentenceArrayNoPeriod = ' '.join(map(str, stemmed)).split(".")
    keywords = set(array_title)
    rate = [0]*len(sentenceArrayNoPeriod)
    for i in range(len(sentenceArrayNoPeriod)):
        currentSentence = sentenceArrayNoPeriod[i].split()
        for word in currentSentence:
            if word in keywords:
                rate[i]+=1
    summary = Translate(lang_from, lang_to, Compare(sentenceArrayNoPeriod, rate))
    return summary



def RemoveExtraWords(title):
    extraWords = {"to", "and", "with", "after", "since", "but", "yet", "or", "for", "so", "although", "instead", "of",
                    "as", "in"}
    for word in title:
        if word in extraWords:
            title.remove(word)
    return title


# compare 5 highest rated sentences vs best 300 letters
def Compare(sentenceArrayNoPeriod, rate):
    #sentence_length = []
    sentenceRate = {}
    #sentenceRate = 0
    begin = 0
    topHighest = [-1, -1, -1, -1, -1]
    # get the highest rated sentences
    for i in range (len(sentenceArrayNoPeriod)):
        lengthOfCurrentSentence = len(sentenceArrayNoPeriod[i].split())
        sentenceRate[i] = rate[i]
            #sentenceRate+=rate[j]
        # push all the data on the same spectrum of [0,1]
        if lengthOfCurrentSentence > 0:
            sentenceRate[i] = sentenceRate[i] / lengthOfCurrentSentence
        if sentenceRate[i] > topHighest[0]:
        #if sentenceRate > topHighest[0]:
            topHighest[0] = sentenceRate[i]
            topHighest.sort()
        begin += lengthOfCurrentSentence
    # make sure the length of text is within the constraints
    topHighest = DecreaseLength(topHighest)
    paragraph = ""
    # form the paragraph
    for k in range(len(topHighest)):
        for key, val in sentenceRate.items():
            if topHighest[k] == val:
                paragraph+= re.sub('\n', '', sentenceArrayNoPeriod[key])
                paragraph += ". "
    return paragraph

def DecreaseLength(topHighest):
    # comparison for length of text, must be within constraint of 300letters or 5sentences.
    while len(topHighest) > 1:
        difference = topHighest[-1] - topHighest[0]
        if difference >= 2:
            topHighest = topHighest[1:]
        else:
            break
    len_sen = []
    len_wrd = 0
    for val in range(len(topHighest)):
        len_sen.append(topHighest[val])
        len_wrd += topHighest[val]
    """if len_wrd > 300:
        topHighest = topHighest[1:]
        decrease_length(topHighest)
    else:
        return topHighest"""
    while -1 in topHighest:
        topHighest.remove(-1)
    while 0 in topHighest:
        topHighest.remove(0)
    return topHighest
    

# compare 3 stories, combine them into an unbiased text summary
# skip any other occurance of that story when bias <0.2 - use Azure for bias analysis
#def readHeadline():
    # TODO:
    # check for the headlines, in case there are similar articles
    # OR
    # compare the content of the articles
    # OR
    # just keep the articles. they might be of importance and give more context
    # OR
    # *** Get unique articles, see if there's a way
    #repetitions = {title: []}


def main():
    mongoDelete = Mongo()
    mongoDelete.DeleteAllDB()
    mongoDelete.CloseConnection()
    """api_key = 'cf837dbe80ba4179beaa9ee8bcdfa08e'
    newsapi = NewsApiClient(api_key= api_key)
    countries = listOfCountries('newsAPI')"""
    er = EventRegistry(apiKey = ERKey, allowUseOfArchive = False)
    countries = OneListOfCountry('Countries.txt')
    translate = sys.argv[1]
    """for count in countries:
        current_country = str(count)
        current_language = countries[count]
        mdb = Mongo()
        top_5 = newsapi.get_top_headlines(page_size=5, page=1, country=current_country)['articles']
        for headline in top_5:
            headline_obj = newsArticle(headline, current_country)
            summary(headline_obj, mdb, abr, current_language, str(translate))
        mdb.closeConnection()"""
    for country in countries:
        currentCountry = str(country)
        mdb = Mongo()
        countryNews = er.getLocationUri(currentCountry)
        top10 = QueryArticlesIter(
                                    sourceLocationUri = [countryNews],
                                    isDuplicateFilter=False,
                                    dataType='news'
                                    )
        for headline in top10.execQuery(er, sortBy="date", sortByAsc=False, maxItems=3):
            # print(article['lang'], article['url'], article['title'], article['body'])
            headlineObj = NewsArticle(headline, currentCountry)
            summary(headlineObj, mdb, headlineObj.GetLanguage(), translate)
        mdb.CloseConnection()
        
    #TODO: get headlines queried by country, loop over the country and 
    #      look through the api with queried countries and top 5 hits     

if __name__ == "__main__":
    main()
