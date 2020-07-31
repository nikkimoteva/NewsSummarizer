import os

def ListOfSpecCountries(fileCountry, fileLang):
    fCountry=open(fileCountry, 'r')
    fLang=open(fileLang, 'r')
    contentCountry = fCountry.read()
    contentLang = fLang.read()
    arrayCountry = contentCountry.split('\n')
    arrayLang = contentLang.split('\n')
    contentList = {}
    for i in range(len(arrayCountry)):
        contentList[str(arrayCountry[i])] = str(arrayLang[i])
    fCountry.close()
    fLang.close()
    return contentList

def OneListOfCountry(file):
    f=open(file, 'r')
    content = f.read()
    countries = content.split('\n')
    f.close()
    return countries

def ListOfCountries(kind):
    if kind.lower() == 'all':
        return ListOfSpecCountries('ISO.3166-1.txt', 'languages.txt')
    elif kind.lower() == 'newsapi':
        return ListOfSpecCountries('NEWSAPI-Countries.txt', 'LanguagesSpec.txt')
