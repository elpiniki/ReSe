__author__ = 'elpiniki'
#try to repeat for all html files in the directory
                #rec = {'Term' : word, 'TF' : word_count[word], 'Filename' : file}
                #hashmapfile.write(str(rec) + "\n")
        #library for stemming PorterStemmer--better than Lancaster one
#######################################################################################################################
import unicodedata
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
import os
import json
import requests
from nltk import PorterStemmer

path = "/home/elpiniki/Documents/ReSe/tools/finaldb"

stopWords = [ "a", "i", "it", "am", "at", "on", "in", "to", "too", "very", \
                 "of", "from", "here", "even", "the", "but", "and", "is", "my", \
                 "them", "then", "this", "that", "than", "though", "so", "are", " ", "", "php", "gif"]

def avg(list):
    sum = 0
    for elm in list:
        sum += elm
    average = sum/(len(list))
    return average


#function for url mapping given the html file name created by crawler
def find_url(filename):
    mapfile = open("data", "r")
    mydict = {}
    for line in mapfile:
        t = line.split()
        mydict[t[0]] = t[1]
    for key in mydict:
        if filename == key:
            urllink = mydict[key]
            return urllink

##Initialization
st = PorterStemmer() #stemmer
new_word_list = []
length_list = []
index = defaultdict(list) #includes all the terms of all the html files
mapfile = open("data", "r") #open data file for the mapping

##Find title and url for all HTML files
for file in os.listdir(path):
    if file.endswith(".html"):
        fileurl = find_url(file) #get the url of the html file
        try:
            r = requests.get(fileurl)
            #print fileurl
            html = r.text
            soup = BeautifulSoup(html)
            try:
                filetitle1 = soup.title.string #get the title of the html file
                filetitle = ''.join(char for char in filetitle1 if char.islower() or char.isupper() or char.isspace())
                print filetitle
            except AttributeError:
                pass
##Find all terms: main indexer
            utext = soup.get_text()
            text = unicodedata.normalize('NFKD', utext).encode('ascii', 'ignore') #make all the letters ascii
            length = len(text)
            length_list.append(length)
            print length
            word_list = re.split('\s+|(?<!\d)[,.](?!\d)(?<!\))(?<!@)(?<!\t)(?<!-)', text.lower()) #make all the letters lower case and split
            #for i in word_list:
            #    t = st.stem(i) #stem the word
            #    new_word_list.append(t) #create a new list with stem words
            word_count = Counter(word_list)
            for word, count in word_count.items():
                if word not in stopWords and (re.match("^[a-z]*$", word)):
                    try:
                        index[word].append(("{" + json.dumps('tf')+ ": " + str(count), json.dumps('doc') + ": " + json.dumps(str(fileurl))+", " + json.dumps('title') +": " + json.dumps(str(filetitle)) +", " + json.dumps('length') + ": " + json.dumps(str(length)) + "} "))
                    except UnicodeEncodeError:
                        pass
        except requests.exceptions.HTTPError: #by using requests check for errors at the http
            pass
        except requests.exceptions.MissingSchema:
            pass

dbfile = open("dbjson.json", "a")
dbfile.write("{\n\t")
for word in index:
    dbfile.write(json.dumps(word) + ":")
    dbfile.write("\n\t")
    dbfile.write(str(index[word]) + ",")
    dbfile.write("\n")
    dbfile.write("\n")
dbfile.write("}")
dbfile.close()

dbfile1 = open("dbjson.json", "r")
dbfile2 = open("dbjson2.json", "w")
for line in dbfile1:
    dbfile2.write(line.replace("'",""))
dbfile1.close()
dbfile2.close()


dbfile2 = open("dbjson2.json", "r")
dbfile3 = open("dbjson3.json", "w")
for line in dbfile2:
    dbfile3.write(line.replace("(",""))
dbfile2.close()
dbfile3.close()


dbfile3 = open("dbjson3.json", "r")
dbfile4 = open("final.json", "w")
for line in dbfile3:
    dbfile4.write(line.replace(")",""))
dbfile3.close()
dbfile4.close()

print length_list
print avg(length_list)