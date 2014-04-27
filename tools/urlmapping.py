##create json file that maps the hash filenames with the urls

import json
import re
from collections import OrderedDict

#d1 = open("data.txt", "r")
d2 = open("d2.json", "w")

d = {}
with open("datatest.txt") as f:
    for line in f:
        tok = line.split('\t')
        d[tok[0]] = tok[1]
        print d
d2.write("{")
for file, url in d.iteritems():
    d2.write("\n\t{" + json.dumps('filename')+ ": " + json.dumps(str(file)) + ", " + json.dumps('url') + ": " + json.dumps(str(url)) + "},")
d2.write("\n}")
d2.close()
#for word in maplist:
#    print json.dumps(word)

#for line in d1:
#    try:
#        d2.write(json.dumps(d1))
#    except UnicodeEncodeError:
#        pass
#d1.close()
