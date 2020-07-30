"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""
import sys
import geograpy as geo
import nltk
import spacy
nlp = spacy.load("en_core_web_sm")
import re
import requests
from newsapi import NewsApiClient
from news import newsArticle
from countries import listOfCountries, listOfSpecCountries
from mongodbDAO import Mongo 
from MSTranslator import translate
from WordStem import stemmer


# summarize the text in 500 letters or 5 sentences maximum.
def summary(headline, mdb, abr, lang_from, lang_to):
    # split the text into an array in order to analyze and de-abriviate
    description = headline.get_description()
    if not description: return
    description = translate(lang_from, lang_to, description)
    stem_languages = listOfSpecCountries('Languages.txt', 'LangMapStem.txt')
    txt_raw = description.split(" ")
    for key, val in stem_languages.items():
        if lang_to in stem_languages.keys():
            stemmed_description = stemmer(txt_raw, str(val))
    stemmed_description = txt_raw
    # txt_chg is used to analyze the text for summarization without the abriviations
    txt_chg = abbriviation(abr, txt_raw)
    # a matrix for analysis of importance of each word
    # TODO: rate each word's importance. ignore '.'(period) for now. 
    # add up every sentence's value in txt_no_period. compare 5 highest rated sentences vs best 300 letters
    url = headline.get_url()
    title = translate(lang_from, lang_to, headline.get_title())
    stemmed_title = stemmer(title, lang_to)
    whyHow = why_how(stemmed_title, txt_chg, stemmed_description, lang_from, lang_to)
    whoWhere = who_where(url, description, lang_from, lang_to)
    mdb.inserInDB(title, url, whoWhere, whyHow)
    print('title: ' + title +
          '\nurl: ' + url + 
          '\nWho: ' + whoWhere + 
          '\nSummary: ' + whyHow)




# make sure that you uncode the abbriviation, so the analyzer won't get confused:
# eg. sentence ending when reached Mr. ; won't = would not
def abbriviation(abr, txt): 
    for i in range(len(txt)):
        if txt[i] in abr:
            txt[i] = abr[txt[i]]
    return txt

def who_where(url, article, lang_from, lang_to):
    #places = geo.get_place_context(url= url)
    doc = nlp(article)
    names = ""
    for ent in doc.ents:
        tmp = re.sub(r'\W- +', "", str(ent))
        if ent == doc.ents[-1]:
            names+= tmp + '.'
        else:
            names += tmp + ", "
    names_translated = translate(lang_from, lang_to, names)
    return names_translated

# article is an array. returns the summarized article
def why_how(title, article, stemmed, lang_from, lang_to):
    summary_title = removeExtraWords(title)
    # without white space
    array_title = summary_title.split()
    # txt_no_period = ' '.join(map(str, article)).split(".")
    txt_no_period = ' '.join(map(str, stemmed)).split(".")
    keywords = set(array_title)
    rate = [0]*len(txt_no_period)
    for i in range(len(txt_no_period)):
        current_sentence = txt_no_period[i].split()
        for word in current_sentence:
            if word in keywords:
                rate[i]+=1
    summary = translate(lang_from, lang_to, compare(article, txt_no_period, rate))
    return summary



def removeExtraWords(title):
    extraWords = {"to", "and", "with", "after", "since", "but", "yet", "or", "for", "so", "although", "instead", "of",
                    "as", "in"}
    for word in title:
        if word in extraWords:
            title.remove(word)
    return title


# compare 5 highest rated sentences vs best 300 letters
def compare(article, txt_no_period, rate):
    #sentence_length = []
    sentence_rate = {}
    #sentence_rate = 0
    begin = 0
    top_highest = [-1, -1, -1, -1, -1]
    # get the highest rated sentences
    for i in range (len(txt_no_period)):
        length_of_current_sentence = len(txt_no_period[i].split())
        # might have to delete this variable. it records the length of words in every single sentence
        """sentence_length.append(length_of_current_sentence)
        for j in range (length_of_current_sentence):
            try:
                sentence_rate[i] += rate[j]
            except:
                sentence_rate[i] = rate[j]"""
        sentence_rate[i] = rate[i]
            #sentence_rate+=rate[j]
        # push all the data on the same spectrum of [0,1]
        if length_of_current_sentence > 0:
            sentence_rate[i] = sentence_rate[i] / length_of_current_sentence
        if sentence_rate[i] > top_highest[0]:
        #if sentence_rate > top_highest[0]:
            top_highest[0] = sentence_rate[i]
            top_highest.sort()
        begin += length_of_current_sentence
    # make sure the length of text is within the constraints
    top_highest = decrease_length(top_highest)
    paragraph = ""
    # form the paragraph
    for k in range(len(top_highest)):
        for key, val in sentence_rate.items():
            if top_highest[k] == val:
                paragraph+=article[key]
            #paragraph+=txt_no_period[sentence_rate[top_highest[key]]]
            paragraph += ". "
    return paragraph

def decrease_length(top_highest):
    # comparison for length of text, must be within constraint of 300letters or 5sentences.
    while len(top_highest) > 1:
        difference = top_highest[-1] - top_highest[0]
        if difference >= 2:
            top_highest = top_highest[1:]
        else:
            break
    len_sen = []
    len_wrd = 0
    for val in range(len(top_highest)):
        len_sen.append(top_highest[val])
        len_wrd += top_highest[val]
    """if len_wrd > 300:
        top_highest = top_highest[1:]
        decrease_length(top_highest)
    else:
        return top_highest"""
    while -1 in top_highest:
        top_highest.remove(-1)
    while 0 in top_highest:
        top_highest.remove(0)
    return top_highest
    

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
    mongo_delete = Mongo()
    mongo_delete.deleteAllDB()
    mongo_delete.closeConnection()
    api_key = 'cf837dbe80ba4179beaa9ee8bcdfa08e'
    newsapi = NewsApiClient(api_key= api_key)
    countries = listOfCountries('newsAPI')
    translate = sys.argv[1]
    abr = {"I'm": "I am", "Mr." : "Mister", "Ms." : "Miss", "Mrs.": "Missus", "don't": "do not", "he's": "he is",
            "U.S." : "United States", "U.S.A" : "United States of America", "U.A.E" : "United Arab Emirates"}
    for count in countries:
        current_country = str(count)
        current_language = countries[count]
        mdb = Mongo()
        top_5 = newsapi.get_top_headlines(page_size=5, page=1, country=current_country)['articles']
        for headline in top_5:
            headline_obj = newsArticle(headline, current_country)
            summary(headline_obj, mdb, abr, current_language, str(translate))
        mdb.closeConnection()
    #TODO: get headlines queried by country, loop over the country and 
    #      look through the api with queried countries and top 5 hits     

if __name__ == "__main__":
    main()
