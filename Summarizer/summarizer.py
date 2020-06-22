import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# summarize the text in 300 letters or 5 sentences maximum.
def summary(text, abr):
    # split the text into an array in order to analyze and de-abriviate
    txt_raw = text.split(" ")
    # txt_chg is used to analyze the text for summarization
    txt_chg = abbriviation(abr, txt_raw)
    txt_period = txt_chg.join(map(str, txt_chg)).split(".")
    # a matrix for analysis of importance of each word
    # TODO: rate each word's importance. ignore '.'(period) for now. 
    # add up every sentence's value in txt_period. compare 5 highest rated sentences vs best 300 letters
    rate = np.zeroes(len(text))



# make sure that you uncode the abbriviation, so the analyzer won't get confused:
# eg. sentence ending when reached Mr. ; won't = would not
def abbriviation(abr, txt):
    for i in range(len(txt)):
        if abr[txt[i]]:
            txt[i] = abr[txt[i]]
    return txt

# compare 5 highest rated sentences vs best 300 letters
def compare(txt_period, rate):
    sentence_length = []
    sentence_rate = {}
    #sentence_rate = 0
    begin = 0
    top_highest = [-1, -1, -1, -1, -1]
    # get the highest rated sentences
    for i in range (len(txt_period)):
        length_of_sentence = txt_period[i].split()
        # might have to delete this variable. it records the length of words in every single sentence
        sentence_length.append(length_of_sentence)
        for j in range (begin, begin+length_of_sentence):
            sentence_rate[i] += rate[j]
            #sentence_rate+=rate[j]
        # push all the data on the same spectrum of [0,1]
        sentence_rate[i] = sentence_rate[i] / length_of_sentence
        if sentence_rate[i] > top_highest[0]:
        #if sentence_rate > top_highest[0]:
            top_highest[0] = sentence_rate[i]
            top_highest.sort()
        begin += length_of_sentence
        sentence_rate=0
    """while len(top_highest) > 1:
        difference = top_highest[-1] - top_highest[0]
        if difference > 0.2:
            top_highest = top_highest[1:]
        else:
            break
    len_sen = []
    len_wrd = 0
    for val in range(len(top_highest)):
        len_sen.append(len(top_highest[val]))
        len_wrd += len(top_highest[val])
    if len_wrd > 300:
        top_highest = top_highest[1:]
        decrease_length(top_highest)"""
    # make sure the length of text is within the constraints
    top_highest = decrease_length(top_highest)
    paragraph = ""
    # form the paragraph
    for key in range(len(top_highest)):
        paragraph+=txt_period[sentence_rate[top_highest[key]]]
        paragraph += ". "
    return paragraph

def decrease_length(top_highest):
    # comparison for length of text, must be within constraint of 300letters or 5sentences.
    while len(top_highest) > 1:
        difference = top_highest[-1] - top_highest[0]
        if difference > 0.2:
            top_highest = top_highest[1:]
        else:
            break
    len_sen = []
    len_wrd = 0
    for val in range(len(top_highest)):
        len_sen.append(len(top_highest[val]))
        len_wrd += len(top_highest[val])
    if len_wrd > 300:
        top_highest = top_highest[1:]
        decrease_length(top_highest)
    else:
        return top_highest
    
    
    


# compare 3 stories, combine them into an unbiased text summary
# skip any other occurance of that story when bias <0.2 - use Azure for bias analysis
def readHeadline():
    # TODO:
    # check for the headlines, in case there are similar articles
    # OR
    # compare the content of the articles
    # OR
    # just keep the articles. they might be of importance and give more context
    repetitions = {title: []}


def main():
    return 0
    abr = {"I'm": "I am", "Mr." : "Mister", "Ms." : "Miss", "Mrs.": "Missus", "don't": "do not", "he's": "he is"}
    summary(text, abr)


if __name__ == "__main__":
    main()
