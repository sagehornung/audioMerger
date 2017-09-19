
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var bodyParser = require('body-parser');
var connections = [];

app.use(bodyParser.json());

var MongoClient = require('mongodb').MongoClient;
var uri = 'mongodb://biowaves:acoustics@ds139124.mlab.com:39124/biowaves-maps';
// Connect to the db

var dbSave;
MongoClient.connect(uri, function (err, db) {

     if(err) {
         console.log('DB connect error');
         throw err;
     } else {
         console.log('DB connect success');
     }
     dbSave = function(db, callback) {
         console.log('DB SAVE', db);
         db.collection('restaurants').insertOne( {
      "address" : {
         "street" : "2 Avenue",
         "zipcode" : "10075",
         "building" : "1480",
         "coord" : [ -73.9557413, 40.7720266 ]
      },
      "borough" : "Manhattan",
      "cuisine" : "Italian",
      "grades" : [
         {
            "date" : new Date("2014-10-01T00:00:00Z"),
            "grade" : "A",
            "score" : 11
         },
         {
            "date" : new Date("2014-01-16T00:00:00Z"),
            "grade" : "B",
            "score" : 17
         }
      ],
      "name" : "Vella",
      "restaurant_id" : "41704620"
   }, function(err, result) {
    assert.equal(err, null);
    console.log("Inserted a document into the restaurants collection.");
    callback();
  });
};


     //Write databse Insert/Update/Query code here..

});
var room;

app.use(express.static(__dirname + '/bower_components'));
app.get('/', function(req, res, next) {
    console.log(__dirname + '/../app/index.html');
    res.sendFile('C:\\Users\\User\\PycharmProjects\\audioMerger\\web\\app\\index.html');
});

app.post('/update', function (req, res, next) {
    console.log('POST: Whale data', req.body);
    var data = req.body;
    io.to('map').emit('update-map', data);
    res.sendStatus(200);
});


app.post('/save', function (req, res, next) {
    console.log('Saving stuff to DB in the server');
    dbSave();
    res.sendStatus(200);
});

app.post('/recorder', function (req, res, next) {
    console.log('POST: Recorder data', req.body);
    var data = req.body;
    io.to('map').emit('plot-recorder', data);
    res.sendStatus(200);
});

io.on('connection', function(client) {
    console.log('Client connected...');
    connections.push(client);

    client.on('join', function(data) {
        console.log(data);
    });

    client.on('messages', function(data) {
        client.emit('broad', data);
        client.broadcast.emit('broad',data);
    });

    client.on('subscribe', function(data){
        room = data.room;
        client.join(room);
        console.log('joined room', room);
    });

});

server.listen(4200);