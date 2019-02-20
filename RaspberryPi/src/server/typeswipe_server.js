#!/usr/bin/env nodejs

const express = require('express');
const app = express();
const port = 8080;

app.get('/', (req, res) => res.send('TypeSwipe raspberry pi here. Send a post request with { \'state\' : [on/off] } to this server to control the robot state'));

app.post('/home/student/', function(req, res) {
	var msg = req.params.state;
	console.log('Received post message. State param = ' + msg);
});

app.listen(port, () => console.log('Server listening on port ${port}'));

