#!/usr/bin/env nodejs

const express = require('express');
const app = express();
const port = 8080;

app.get('/', (req, res) => res.send('TypeSwipe raspberry pi here. Send a post request with { \'state\' : [on/off] } to this server to control the robot state'));

app.post('/', function(req, res) {
	var msg = req.query.state;
	var response = 'Received post message. State param = ' + msg;
	console.log(response);
	res.send(response);
});

app.listen(port, () => console.log('Server listening on port ${port}'));

