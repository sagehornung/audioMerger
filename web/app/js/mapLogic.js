var map, whale;
    var whaleMap = {};
    var whaleMapPtr = {};
    var recorders = [];
    var vectorsArray = [];

    var colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00'];
    var whaleImgs = [
        'http://res.cloudinary.com/dtf5iuzbg/image/upload/c_scale,w_25/v1505704745/whale_red_lky0d6.png',
        'http://res.cloudinary.com/dtf5iuzbg/image/upload/c_scale,w_25/v1505704390/whale_green_ti38zv.png',
        'http://res.cloudinary.com/dtf5iuzbg/image/upload/c_scale,w_25/v1505704745/whale_blue_rz5zfv.png',
        'http://res.cloudinary.com/dtf5iuzbg/image/upload/c_scale,w_25/v1505704391/whale_yellow_ao8bz3.png'
    ];

    var icons = {
        whale: {
            icon: 'http://res.cloudinary.com/dtf5iuzbg/image/upload/c_scale,w_30,bo_1px_solid_rgb:0000ff/v1505261225/whale1600_rnwr0w.png'
        },
        recorder: {
            icon: 'http://res.cloudinary.com/dtf5iuzbg/image/upload/c_scale,w_25/v1505451762/recorder_rm2mod.png',
        }
    };

    var lineSymbol = {
            path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
            strokeColor: '#820000'
        };

    function updateWhale(whaleObj) {

        console.log('Update whale location', whaleObj);

        if(!whaleMap[whaleObj.id])  {
            whaleMap[whaleObj.id] = [];
        }

        if(!whaleMapPtr[whaleObj.id])  {
            whaleMapPtr[whaleObj.id] = [];
        }

        addWhalePoint(whaleObj, 'whale');
        plotAllPairs();

    }

    function removeWhale(id) {

        for (var i = 0; i <vectorsArray.length; i++)
        {
            vectorsArray[i].setMap(null); //or line[i].setVisible(false);
        }

        console.log('removeWhale called with id ', id);
        console.log('WhaleMap array obj before', whaleMap[id]);
        if(whaleMap[id].length > 0 ) {
            var ele = whaleMap[id].pop();
            var m = whaleMapPtr[id].pop();
            m.setMap(null);
        }



        console.log('WhaleMap array obj after', whaleMap[id], 'ele', ele);
//        drawWhalesOnScreen();
        plotAllPairs();
    }

    function addWhalePoint(whaleObj, iconType) {
        console.log('addWhalePoint', whaleObj)
        var lat = whaleObj.lat;
        var lng = whaleObj.lng;
        var whale = {position: new google.maps.LatLng(lat, lng), type: iconType, lat: lat, lng: lng};
        whaleMap[whaleObj.id].push(whale);
        var marker = new google.maps.Marker({
            position: whale.position,
            icon: whaleImgs[whaleObj.id],
            map: map
        });
        whaleMapPtr[whaleObj.id].push(marker);
    }

    function plotAllPairs() {

        for (var key in whaleMap) {
            if (whaleMap.hasOwnProperty(key)) {
                var whalePosArr = whaleMap[key];
                console.log('whalePosArr', whalePosArr.length, whalePosArr);
                if(whalePosArr.length > 1) {
                    for(var i = 0; i < whalePosArr.length - 1; i++) {
                        console.log('Plotting pair of pts', whalePosArr[i], whalePosArr[i + 1]);
                        plotWhalePathVector(whalePosArr[i], whalePosArr[i + 1], key);
                    }
                }
            }
        }
    }


    function plotWhalePathVector(v1, v2, key){

        console.log('v1 & v2', v1.lat, v1.lng, v2.lat, v2.lng);

        // Create the polyline and add the symbols via the 'icons' property.
        var vector = new google.maps.Polyline({
            path: [{lat: parseFloat(v1.lat), lng: parseFloat(v1.lng)}, {lat: parseFloat(v2.lat), lng: parseFloat(v2.lng)}],
            strokeColor: colors[key],
            icons: [
                {
                    icon: lineSymbol,
                    offset: '50%'
                }
            ],
            map: map
        });
        vectorsArray.push(vector);
    }

    function addRecorderPoint(point, iconType) {
        console.log('Plotting a recorder point', point);
        var lat = point.lat;
        var lng = point.lng;
        recorders.push( {position: new google.maps.LatLng(lat, lng), type: iconType} );
        drawRecordersOnScreen();
    }

    function drawRecordersOnScreen(){
        console.log('Drawing all recorders');
        recorders.forEach(function(recorder) {
            var marker = new google.maps.Marker({
                position: recorder.position,
                icon: icons[recorder.type].icon,
                map: map
            });
        });
    }

    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 10,
            center: new google.maps.LatLng(36.6734051, -122.4007693),
            mapTypeId: 'roadmap'
        });

    }


    $( "#b0" ).click(function() {
        console.log('JQuery remove 0');
        removeWhale('0')
    });
    $( "#b1" ).click(function() {
        console.log('JQuery remove 1');
        removeWhale('1')
    });
    $( "#b2" ).click(function() {
        console.log('JQuery remove 2');
        removeWhale('2')
    });
    $( "#b3" ).click(function() {
        console.log('JQuery remove 3');
        removeWhale('3')
    });

    var socket = io.connect('192.168.1.84:4200');
    socket.on('connect', function(data) {
        socket.emit('join', 'Hello World from client');
        socket.emit('subscribe', {room: 'map'});

    });

    socket.on('update-map', function(data) {
        console.log('Updating map with whale data', data);
        updateWhale(data);
    });

    socket.on('plot-recorder', function(data) {
        console.log('Updating map with recorder position', data);
        addRecorderPoint(data, 'recorder');
    });