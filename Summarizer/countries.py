import os

def listOfSpecCountries(file_country, file_lang):
    f_country=open(file_country, 'r')
    f_lang=open(file_lang, 'r')
    content_country = f_country.read()
    content_lang = f_lang.read()
    array_country = content_country.split('\n')
    array_lang = content_lang.split('\n')
    content_list = {}
    for i in range(len(array_country)):
        content_list[str(array_country[i])] = str(array_lang[i])
    f_country.close()
    f_lang.close()
    return content_list

def listOfCountries(kind):
    if kind.lower() == 'all':
        return listOfSpecCountries('ISO.3166-1.txt', 'languages.txt')
    elif kind.lower() == 'newsapi':
        return listOfSpecCountries('NEWSAPI-Countries.txt', 'LanguagesSpec.txt')
