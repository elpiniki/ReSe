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

  var sh = require("execSync");
  var result = sh.exec("bash -c './tools/stem.py " + req.query.term + "'");
  console.log("[Elpiniki's Server] code: " + result.code);
  console.log("[Elpiniki's Server] out: " + result.stdout);
  var validJSON = result.stdout.replace(/'/g,'"');
  console.log(validJSON);
  var stemmed  = JSON.parse(validJSON);

  console.log(stemmed);

  var documents = {}
  // Object iteration
  for (var i = 0; i < stemmed.length; i++) {
    word = stemmed[i];
    var results = db[word];
    for (var j = 0; j < results.length; j++) {
      var df = results.length;
      var N = 450;
      var score = (1 + Math.log(1+Math.log(result.tf))) * Math.log(N+1/df);
      if (documents[j.doc]) {
        documents[j.doc].score = documents[j.doc].score + score;
      } else {
        documents[j.doc] = {"title": j.title, "score": score}
      }
    };
  };

  // grafeis ton algori8mo sou: apo ta results => sto 1 Result
  var result = results[0];
  var qresults = {
    "doc1" : {"title":"Document1", "score":6}
  , "doc2" : {"title":"Document2", "score":3}
  , "doc3" : {"title":"Document3", "score":13}
  }
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
