__author__ = 'elpiniki'

#!/usr/env python
#no duplicates
#problem with lower and uppercase: I made all the text lower case. this is not good solution.
#use of hashmap
#try to repeat for all html files in the directory
                #rec = {'Term' : word, 'TF' : word_count[word], 'Filename' : file}
                #hashmapfile.write(str(rec) + "\n")
                #print rec
        #hashmapfile.close()
        #https://wiki.python.org/moin/UsingPickle
        ##ALLAGHHHGHGHGHG
        #library for stemming PorterStemmer--better than Lancaster one
        #### test test test test test
#######################################################################################################################
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import re
import os
import json
#from nltk.stem.lancaster import LancasterStemmer
from nltk import PorterStemmer
import pickle
from pprint import pprint
from sys import argv

path = "/home/elpiniki/Dropbox/rese/indexer/"

stopWords = [ "a", "i", "it", "am", "at", "on", "in", "to", "too", "very", \
                 "of", "from", "here", "even", "the", "but", "and", "is", "my", \
                 "them", "then", "this", "that", "than", "though", "so", "are", " ", ""]
#stemEndings = [ "-s", "-es", "-ed", "-er", "-ly" "-ing", "-'s", "-s'"]

def parsetext(f):
    soup = BeautifulSoup(f)
    t = soup.get_text()
    return t

def replace_all(file, dic):
    for line in file:
        for i, j in dic.iteritems():
            file.write(line.replace(i, j))
    return file

st = PorterStemmer()
new_word_list = []
index = defaultdict(list) #includes all the terms of ALL the html files
for file in os.listdir(path):
    #if file.endswith(".html"):
    #    print file
    #    htmlfile = open(file, "r")
    #    text = parsetext(htmlfile)
    if file.endswith(".txt"):
        text = open(file, "r").read()
        text = text.lower() #make all the letters lowercase to ignore the case during the retrieval
        #print text
        #text = st.stem(text)
        #print text
        word_list = re.split('\s+|(?<!\d)[,.](?!\d)(?<!\))(?<!@)(?<!\t)(?<!-)', text)
        for i in word_list:
            t = st.stem(i)
            new_word_list.append(t)
        print new_word_list
        word_count = Counter(new_word_list)

        for word, count in word_count.iteritems():
            if word not in stopWords:
                index[word].append(("{" + json.dumps('tf')+ ": "  + str(count), json.dumps('doc') + ": " + json.dumps(str(file))+"}"))
        #dbfile = open("db.txt", "a")
        #dbfile.write(str(index))
        #dbfile.close()
 #       print
newlist = list(index.items())

t = json.dumps(newlist)
#print index

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

#test = json.dump(newlist, separators=(','))
#print test
#dbfile = open("db.txt", "a")
#dbfile.write(str(newlist))
#dbfile.close()

#print newlist.pop(1)

#"phoneNumbers": [
     #   { "type": "home", "number": "212 555-1234" },
      #  { "type": "fax",  "number": "646 555-4567" }
   # ]
 #       print
#pprint(index(1))
 #       print

        #jsonfile = open("db.json", "a")
        #for word in total_list:
        #    try:
        #       jsonfile.write("Term: " + word + "TF: " + str(word_count[word]) + "filename: " + file + "\n")
        #    except UnicodeEncodeError:
        #        pass

        #jsonfile.close()

pickle.dump( index, open( "inverted_index.p", "wb" ), -1 )
