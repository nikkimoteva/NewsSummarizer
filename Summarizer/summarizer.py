"""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""
import geograpy as geo
import nltk
import requests
from newsapi import NewsApiClient
from news import newsArticle
from countries import listOfCountries


# summarize the text in 500 letters or 5 sentences maximum.
def summary(headline, abr):
    # split the text into an array in order to analyze and de-abriviate
    description = headline.get_description()
    txt_raw = description.split(" ")
    # txt_chg is used to analyze the text for summarization without the abriviations
    txt_chg = abbriviation(abr, txt_raw)
    # a matrix for analysis of importance of each word
    # TODO: rate each word's importance. ignore '.'(period) for now. 
    # add up every sentence's value in txt_no_period. compare 5 highest rated sentences vs best 300 letters
    url = headline.get_url()
    whyHow = why_how(headline.get_title(), txt_chg)
    whoWhere = who_where(url, description)
    title = headline.get_title()
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

def who_where(url, article):
    return ""
    places = geo.get_place_context(url= url)
    #persons = get_human_names()

# article is an array. returns the summarized article
def why_how(title, article):
    summary_title = removeExtraWords(title)
    # without white space
    array_title = summary_title.split()
    txt_no_period = ' '.join(map(str, article)).split(".")
    keywords = set(array_title)
    rate = [0]*len(txt_no_period)
    for i in range(len(txt_no_period)):
        current_sentence = txt_no_period[i].split()
        for word in current_sentence:
            if word in keywords:
                rate[i]+=1
    return compare(txt_no_period, rate)


def removeExtraWords(title):
    extraWords = {"to", "and", "with", "after", "since", "but", "yet", "or", "for", "so", "although", "instead", "of",
                    "as", "in"}
    for word in title:
        if word in extraWords:
            title.remove(word)
    return title


# compare 5 highest rated sentences vs best 300 letters
def compare(txt_no_period, rate):
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
                paragraph+=txt_no_period[key]
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
    newsapi = NewsApiClient(api_key='cf837dbe80ba4179beaa9ee8bcdfa08e')
    top_headlines = newsapi.get_top_headlines()['articles']
    #TODO: get headlines queried by country
    countries = listOfCountries()
    print(countries)
    abr = {"I'm": "I am", "Mr." : "Mister", "Ms." : "Miss", "Mrs.": "Missus", "don't": "do not", "he's": "he is",
            "U.S." : "United States", "U.S.A" : "United States of America", "U.A.E" : "United Arab Emirates"}
    for headline in top_headlines:
        headline_obj = newsArticle(headline)
        summary(headline_obj, abr)


if __name__ == "__main__":
    main()
