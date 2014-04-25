########################################################################################################################
##  Crawler for the Search and Data Mining Course
##  Version 8.0
##  Author: Elpiniki Apostolaki-Iosifidou (elpiniki@udel.edu)
##  The "mycrawler.py" creates and saves all html files that contain the word research.
##  The name of the html files is the hash of the html content. We will not have duplicates in the database.
##  The data.txt contains the mapping between htmlname and url.
########################################################################################################################

from _bsddb import DB
import urlparse
import requests
from bs4 import BeautifulSoup

import urlparse
import posixpath

import urllib2

# function of parsing the url and get the major components
def urljoin(base, url):
    join = urlparse.urljoin(base, url)
    url = urlparse.urlparse(join)
    path = posixpath.normpath(url[2])
    return urlparse.urlunparse(
        (url.scheme, url.netloc, path, url.params, url.query, None)
    )

require_url = "http://www.udel.edu/" #remain at this domain while crawling 
url = "http://www.ece.udel.edu/"  #start from this url

#we do not want to visit any page twice so we keep historical records already seen
unvisited = {url}  #stack of urls to visit and scrape
visited = set()  #historic records of urls

#our stack should grow to a spesific point and then shrink and when the programm finishes the stack should be empty and has nothing else to do
DB_file = open('data', 'w+') #at the data.txt keep records of the urls
while len(unvisited) > 0:
    url = unvisited.pop()  #pop the one we process so as next time to process the next one
    try:
        r = requests.get(url) #get the url
        r.raise_for_status()
        if r.url in visited: #check the historic records
            continue
        visited.add(url)

        soup = BeautifulSoup(r.text)
        text = soup.get_text()
        if 'research' in text: #this is a helpful step for my project however, it does not bring only pages with research, since the word research may be an anchor. 
            print r.url
            usock = urllib2.urlopen(url)
            data = usock.read()
            usock.close()
            i = len(visited)
            Html_name = hash(data) #create name of the file using hash, as a result to create the database for the project with unique file names
            print Html_name
            Html_file = open("%d.html" % Html_name, "w+") 
            Html_file.write(data) #at the data file we will have the mapping of file name (hash) and the url
            Html_file.close()
            DB_file = open('data', 'a')
            DB_file.write(str(Html_name) + '    ' + str(url) + '\n')
            DB_file.close()
        for tag in soup.findAll('a', href=True): #find the links to continue crawling
            link = tag['href']
            newurl = urljoin(r.url, link)
            if newurl not in visited and newurl not in unvisited and require_url in newurl:
                unvisited.add(newurl)
    except requests.exceptions.HTTPError: #by using requests check for errors at the http
        pass
