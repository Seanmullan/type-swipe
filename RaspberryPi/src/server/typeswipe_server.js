#!/usr/bin/env nodejs

const express = require('express');
const bodyParser = require('body-parser');
const port = 8080;

const app = express();

app.use(bodyParser.urlencoded({ extended: true })); 
app.use( bodyParser.json() );

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

  next();
});

app.get('/', (req, res) => res.send('TypeSwipe raspberry pi here. Send a post request with { \'state\' : [on/off] } to this server to control the robot state'));

app.post('/', function(req, res) {
  // Load json file
  let json = require('../data/system_control.json')
  
  if (req.body.state == "Start") json.system.run = 1;
  else if (req.body.state == "Stop") json.system.run = 0;
  else json.system.run = 2;

  // Upload changes in the file
  var fs = require('fs');
  fs.writeFile('../data/system_control.json', JSON.stringify(json), 'utf8');

  res.send( req.body )
  
});

app.listen(port, () => console.log('Server listening on port ' + port));
