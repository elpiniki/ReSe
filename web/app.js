var express = require('express');
var app = express();
var db = require('./db/final.json');

app.get('/hello.txt', function(req, res){
    res.send('Hello World');
});

app.get('/', function(req, res){
    res.send('Tipota');
});

app.get('/getResults', function(req, res){
  console.log("[Elpiniki's Server] Received term: " + req.query.term);
  var results = db[req.query.term];
  // grafeis ton algori8mo sou: apo ta results => sto 1 Result
  var result = results[0];
  qresults = {
                "title" : result.doc
            ,   "score" : result.tf
            ,   "link"  : result.doc
            };
  res.set('Access-Control-Allow-Origin', '*');
  res.json(qresults);
})
;
var server = app.listen(3000, function() {
    console.log("[Elpiniki's Server] Listening on port %d", server.address().port);
});