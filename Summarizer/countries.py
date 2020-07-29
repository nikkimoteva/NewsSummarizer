import os

def listOfSpecCountries(file):
    f=open(file, 'r')
    content = f.read()
    content_list = content.split("\n")
    f.close()
    return content_list

def listOfCountries(kind):
    if kind.lower() == 'all':
        return listOfSpecCountries('ISO.3166-1.txt')
    elif kind.lower() == 'newsapi':
        return listOfSpecCountries('NEWSAPI-Countries.txt')
