
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
  
  //for more info see: http://nodejsdb.org/db-mysql/
  
  return {
    getCount: function(callback) {
      db.query().select('count(*)').from('posts').execute(function(error,rows,cols) {callback(error,rows[0]["count(*)"])});
    },
    getPosts: function(callback) {
      db.query().select('*').from('posts').limit(10000).execute(function(error,rows,cols) {callback(error,rows)});
    },
    getAll: function(callback) {
      db.query('SELECT * FROM posts p, post_instance pi WHERE p.city=\'sfc\' AND p.id = pi.post_id LIMIT 10000;')
      .execute(function(error,rows,cols) {callback(error,rows)});
    },
    
    /* Distribution methods: */
    getSomeDist: function(what,filters,callback) {
      filters = filters || {}
      
      if (!filters.city)
        filters.city = 'sfc'
      
      var querystr = ""
      querystr +=   "SELECT PI." + what
      querystr +=   "    FROM posts P, post_instance PI where P.id = PI.post_id "
      querystr +=   "      AND P.section='apa' "
      querystr +=   "      AND P.city='"+filters.city+"' "
      if (filters.pmin && filters.pmax && filters.brmin && filters.brmax && filters.sqmin && filters.sqmax) {
        querystr += "      AND (PI.price >='"       +filters.pmin        +"' OR PI.price=NULL)"
        querystr += "      AND (PI.price <='"       +filters.pmax        +"' OR PI.price=NULL)"
        querystr += "      AND (PI.bedroomcount >='"+filters.brmin       +"' OR PI.bedroomcount=NULL)"
        querystr += "      AND (PI.bedroomcount <='"+filters.brmax       +"' OR PI.bedroomcount=NULL)"
        querystr += "      AND (PI.sqft >='"        +filters.sqmin       +"' OR PI.sqft=NULL)"
        querystr += "      AND (PI.sqft <='"        +filters.sqmax       +"' OR PI.sqft=NULL)"
      }
      querystr += "      AND PI.id = (SELECT MAX(id) FROM post_instance PI_p where PI_p.post_id = PI.post_id) "
      querystr += "      ORDER BY PI.id DESC "
      querystr += "      LIMIT 10000;    "

      db.query(querystr).execute(function(error,rows,cols) {callback(error,rows)});
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
      js = data;
    }
    resJson(res,js);
  };    
}

var returnArrayDist = function(res,index) {
  return function(err,data) {
    var js = [];
    console.log(data);
    for (var i = 0; i < data.length; i++) {
      js.push(data[i][index])
    }
    resJson(res,js);
  };      
}

/**
 * Here we set up the supported calls
 */
var routes = { }

routes['/getPosts.json'] = function(req,res,next,options,db,path) {
  db.getPosts(resDBdata(res,"posts"));
};



var defineDistRoute = function(name) {
  routes['/get_'+name+'_dist.json'] = function(req,res,next,options,db,path) {
    db.getSomeDist(name, req.query, returnArrayDist(res,name));
  };
}
defineDistRoute("price");
defineDistRoute("sqft");
defineDistRoute("bedroomcount");


routes["/getCount.json"] = function(req,res,next,options,db,path) {
  db.getCount(resDBdata(res,"posts_count"));
};