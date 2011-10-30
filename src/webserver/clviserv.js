//clviserv.js - the server side of CraigslistVis
//
//Created by Niels Joubert on 2011-10-17.
//Copyright (c) 2011 Stanford. All rights reserved.

var base

var http = require('http');

function hande_data_req(req, res) {
  res.writeHead(200);
  res.end('Hello there data requested');
  
}

var server = http.createServer(function(req, res) {
  
  console.log(req.url)
  
  if (req.url.indexOf("/data") == 0) {
    handle_data_req(rew, res);
  } else if () {
     
  } else {
    res.sendHeader(404, {"Content-Type": "text/plain"});  
    res.write("404 Not Found\n");  
    res.close();  
    return;  
  }  
  
});
server.listen(8080);
console.log("Server listening on port 8080")