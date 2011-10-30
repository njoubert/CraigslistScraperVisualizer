//clviserv.js - the server side of CraigslistVis
//
//Created by Niels Joubert on 2011-10-17.
//Copyright (c) 2011 Stanford. All rights reserved.

var connect = require('connect');

var server = connect.createServer(
  connect.favicon(),
  connect.logger(),
  connect.static(__dirname + '/../webclient'));
server.listen(8080);