__author__ = 'elpiniki'
#!/usr/env python
#use of hashmap
#try to repeat for all html files in the directory
                #rec = {'Term' : word, 'TF' : word_count[word], 'Filename' : file}
                #hashmapfile.write(str(rec) + "\n")
                #print rec
        #hashmapfile.close()
        #library for stemming PorterStemmer--better than Lancaster one
#######################################################################################################################
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
import os
import json
import requests
from nltk import PorterStemmer

path = "/home/elpiniki/ReSe/tools/"

stopWords = [ "a", "i", "it", "am", "at", "on", "in", "to", "too", "very", \
                 "of", "from", "here", "even", "the", "but", "and", "is", "my", \
                 "them", "then", "this", "that", "than", "though", "so", "are", " ", ""]

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
index = defaultdict(list) #includes all the terms of all the html files
mapfile = open("data", "r") #open data file for the mapping

##Main indexing
for file in os.listdir(path):
    if file.endswith(".html"):
        fileurl = find_url(file) #get the url of the html file
        r = requests.get(fileurl)
        data = r.text
        soup = BeautifulSoup(data)
        filetitle = soup.title.string #get the title of the html file
        text = data.lower() #make all the letters lowercase to ignore the case during the retrieval
        word_list = re.split('\s+|(?<!\d)[,.](?!\d)(?<!\))(?<!@)(?<!\t)(?<!-)', text)

        for i in word_list:
            t = st.stem(i)
            new_word_list.append(t)
        word_count = Counter(new_word_list)

        for word, count in word_count.iteritems():
            if word not in stopWords:
                index[word].append(("{" + json.dumps('tf')+ ": " + str(count), json.dumps('doc') + ": " + json.dumps(str(fileurl))+", " + json.dumps('title') +": " + json.dumps(str(filetitle)) +"}"))

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

dic = {"'":"", "(":"{", ")":"}"}

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

