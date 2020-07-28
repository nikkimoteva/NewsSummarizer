import os

def listOfCountries():
    file='ISO 3166-1.txt'
    f=open(file, 'r')
    content = f.read()
    content_list = content.split("\n")
    f.close()
    return content_list

if __name__ == '__countries__':
    listOfCountries()