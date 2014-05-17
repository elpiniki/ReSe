try {
  var express = require('express');
  var app = express();
  var db = require('./db/final.json');
} catch (e) {
  console.log('=============');
  console.log(e);
}

app.get('/hello.txt', function(req, res){
    res.send('Hello World');
});

app.get('/', function(req, res){
  res.render('index.html');
});

app.get('/getResults', function(req, res){
    //if (!req.query.term) {}
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
}) ;

/**
 * Another solution -- anything in ./public will be served as file
 * http://stackoverflow.com/questions/9443840/basic-webserver-with-node-js-and-express-for-serving-html-file-and-assets
 */

app.set('views', __dirname + '/views');
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'ejs');

var server = app.listen(3000, function() {
    console.log("[Elpiniki's Server] Listening on port %d", server.address().port);
});
