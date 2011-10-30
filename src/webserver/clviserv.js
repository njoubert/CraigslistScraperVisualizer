//clviserv.js - the server side of CraigslistVis
//
//Created by Niels Joubert on 2011-10-17.
//Copyright (c) 2011 Stanford. All rights reserved.

var fs = require('fs');
var connect = require('connect');

var clhandler = require('./clhandler.js')

//set up config
var configfile = "../../config.json"
var configfiledata = fs.readFileSync(configfile)
var config = JSON.parse(configfiledata)

//set up all the layers in the server.
//you can think of it as requests passing through the layers in the order given
connect.createServer()
  .use(connect.logger('tiny'))
  .use(connect.staticCache())
  .use('/data', clhandler(config))
  .use(connect.static(__dirname + "/../.." + config.STATIC_BASEDIR))
  .listen(8080);