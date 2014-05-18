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

function getResults(wList, db, N) {
  var documents = {}
  // Object iteration
  for (var i = 0; i < wList.length; i++) {
    word = wList[i];
    var results = db[word];
    for (var j = 0; j < results.length && j < 10; j++) {
      var df = results.length;
      if (results[j].title.indexOf(word)){
        console.log("FOUND!")
        n = 15
      } else {
        console.log("NOT!");
        n = 0
      }
      var score = ((1 + Math.log(1+Math.log(results[j].tf)))/(0.05+0.05*(results[j].l/12470))) * Math.log((N+1)/df) + n;
      console.log("CALC: " + 1 + " tf:" + results[j].tf + " innerlog:" + Math.log(results[j].tf) + " idf:" + Math.log((N+1)/df));
      console.log("df: " + df + ", Word: " + word + ", Doc: " + results[j].doc + ", Score: " + score)

      console.log(documents[results[j].doc]);

      if (documents[results[j].doc]) {
        documents[results[j].doc].score = (documents[results[j].doc].score + score);
        console.log("update score");
      } else {
        documents[results[j].doc] = {"title": results[j].title, "score": score};
        console.log("add to doc: " + documents[results[j].doc])
      }
    }
  }
  return documents;
}

app.get('/getResults', function(req, res){
  //if (!req.query.term) {}
  var useStemming = false;
  var chopped = [];
  console.log("[Elpiniki's Server] Received term: " + req.query.term);

  if (useStemming) {
      var sh = require("execSync");
      var result = sh.exec("bash -c './tools/stem.py " + req.query.term + "'");
      console.log("[Elpiniki's Server] code: " + result.code);

      console.log("[Elpiniki's Server] out: " + result.stdout);
      var validJSON = result.stdout.replace(/'/g, '"');
      console.log(validJSON);
      chopped = JSON.parse(validJSON);

      console.log(chopped);
  } else {
      chopped = req.query.term.split(/\s+/);
      console.log(chopped)
  }
  var db1 = {
    "energy": [{"tf":1, "doc":"doc1", "title":"T1" }, {"tf":8, "doc":"doc2", "title":"T1"}, {"tf":3, "doc":"doc3", "title":"T1"}]
  , "pizza" : [{"tf":2, "doc":"doc2", "title":"T1"}, {"tf":3, "doc":"doc3", "title":"T1"}, {"tf":8, "doc":"doc4", "title":"T1"}]
  }

  //var documents = getResults(["energy", "pizza"], db1, 4); // This is used
  //for testing
  var documents = getResults(chopped, db, 373);

  //console.log(documents);

  // grafeis ton algori8mo sou: apo ta results => sto 1 Result
  var qresults = {
    "doc1" : {"title":"Document1", "score":6}
  , "doc2" : {"title":"Document2", "score":3}
  , "doc3" : {"title":"Document3", "score":13}
  }
  res.set('Access-Control-Allow-Origin', '*');
  res.json(documents);
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
