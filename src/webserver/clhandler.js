
/*!
 * CLVis - clhandler
 */
 
/**
 * API for access to Craigslist database
 *
 * Examples:
 *
 *     connect(
 *       clapi('/data')
 *     ).listen(3000);
 *
 *
 * Options:
 *
 *    - `none`   No options currently supported
 *
 * @param {String} root
 * @param {Object} options
 * @return {Function}
 * @api public
 */
var fs = require('fs')
  , path = require('path')
  , url = require('url')
  , mysql = require('db-mysql');




/**
 * Database Wrapper
 */

var cldb = function(mysqldb) {
  
  var db = mysqldb
  
  return {
    getCount: function(callback) {
      db.query().select('count(*)').from('posts').execute(function(error,rows,cols) {callback(error,rows[0]["count(*)"])});
    },
    getPosts: function(callback) {
      db.query().select('*').from('posts').limit(10000).execute(function(error,rows,cols) {callback(error,rows)});
    }
  }
}

/**
 * Expose the entrypoint api.
 */
exports = module.exports = function clhandler(options){
  options = options || {}
  
  if (!options.hasOwnProperty("DB_USER")) throw new Error('clhandler api requires DB_USER in options');
  
  //attempt to connect to database
  
  var db;
  new mysql.Database({
    hostname: options["DB_SERV"],
    user: options["DB_USER"],
    password: options["DB_PASS"],
    database: options["DB_BASE"]
  }).on('error', function(error) {
    console.log('DB: Error' + error)
  }).on('ready', function(server) {
    console.log('DB: Connected to ' + server.hostname + ' (' + server.version + ')'); db = cldb(this);
  }).connect();
  
  console.log('Craigslist Request Handler initializing...');
  return function clhandler(req,res,next) {
    options.path = req.url;
    options.getOnly = true;
    handle(req,res,next,options,db);
  };
};

/**
 * Attempt to handle a request for the given .
 */

var handle = exports.handle = function(req,res,next,options,db){
  options = options || {};
  if (!options.path) throw new Error('path required');
  
  //send response
  var path = url.parse(options.path);
  
  if (routes.hasOwnProperty(path.pathname)) {
    return routes[path.pathname](req,res,next,options,db,path);
  }
  return next();
}

/**
 * Stringifies a JS object and writes it to response
 */
var resJson = function(res,jsobject) {
  res.writeHeader(200, {"Content-Type":"application/json"});
  res.write(JSON.stringify(jsobject));
  res.end()  
}

var resDBdata = function(res,indx) {
  return function(err,data) {
    var js;
    if (err) {
      console.log("DB Error: " + err);
      js = { "error":err };
    } else {
      js = { indx:data };
    }
    resJson(res,js);
  };    
}

/**
 * Here we set up the supported calls
 */
var routes = { }

routes['/getAll.json'] = function(req,res,next,options,db,path) {
  db.getPosts(resDBdata(res,"posts"));
};

routes["/getCount.json"] = function(req,res,next,options,db,path) {
  db.getCount(resDBdata(res,"posts_count"));
};

routes["/getInfo.json"] = function(req,res,next,options,db,path) {
  js = {
    "options":options,
    "path":path
  }
  resJson(res,js);
};
