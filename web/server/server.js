
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var bodyParser = require('body-parser');
var connections = [];

app.use(bodyParser.json());

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