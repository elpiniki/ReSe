var express = require('express');
var app = express();

app.get('/hello.txt', function(req, res){
    res.send('Hello World');
});

app.get('/', function(req, res){
    res.send('Tipota');
});

app.get('/getResults', function(req, res){
  qresults = {
                "title" : "University of Delaware | V2G"
            ,   "score" : "12.32"
            ,   "link"  : "http://www.udel.edu/v2g"
            };
  res.set('Access-Control-Allow-Origin', '*');
  res.json(qresults);
})
;
var server = app.listen(3000, function() {
    console.log('Listening on port %d', server.address().port);
});