//clviserv.js - the server side of CraigslistVis
//
//Created by Niels Joubert on 2011-10-17.
//Copyright (c) 2011 Stanford. All rights reserved.

var connect = require('connect');

function handle_data(req,res) {
  console.log("handling data")
}

var server = connect.createServer(connect.logger('tiny'));
server.use('/data', handle_data);
server.use(connect.static(__dirname + '/../webclient'));
server.listen(8080);