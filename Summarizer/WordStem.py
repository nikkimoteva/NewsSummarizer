from nltk.stem.snowball import SnowballStemmer
from nltk.stem.isri import ISRIStemmer
from nltk.stem.rslp import RSLPStemmer

def Stemmer(wordList, language):
    for word in wordList:
        wordStemmer = SnowballStemmer(language, ignore_stopwords=True)
        word = wordStemmer.stem(word)
    return wordList