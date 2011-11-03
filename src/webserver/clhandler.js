
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
  
  var validateFilters = function(filters) {
      filters = filters || {}
      
      if (!filters.city)
        filters.city = 'sfc'
      if (!filters.limit)
        filters.limit = 10000
      if (!filters.pmax)
        filters.pmax = 7000
      if (!filters.pmin)
        filters.pmin = 100
      if (!filters.brmin)
        filters.brmin = 0
      if (!filters.brmax)
        filters.brmax = 10
      if (!filters.sqmin)
        filters.sqmin = 0
      if (!filters.sqmax)
        filters.sqmax = 10000
        
        
      return filters;    
  }
  
  function querycallback(err,rows,cols) {
    var a = 0
    if (!err) {
      a += 1
      console.log(a)
    }
  }
  
  return {
    insertGeocoded: function(callback) {
      fs.readFile('/Users/njoubert/Dropbox/Code/CLScraper/geocoded.json', function (js_err, js_data) {
        if (js_err) throw js_err;
        var g = JSON.parse(js_data);
        
        function spawnfor(garray,gindex,gmax) {
          if (gindex < gmax) {
           var myid = garray[gindex]['id'];
           console.log(gindex + ", " + myid);        
            if (garray[gindex]['latlon']) {
              var lat = garray[gindex]['latlon']['Na'];
              var lon = garray[gindex]['latlon']['Oa'];
              db.query("UPDATE post_instance SET lat='"+lat+"', lon='"+lon+"' WHERE id='"+myid+"';").execute(function(errorr,rowsr,colsr) { spawnfor(garray,gindex+1,gmax); });
            } else {
              spawnfor(garray,gindex+1,gmax);
            }
          } else {
            callback(false,{"done":g})
          }
        }
        
        spawnfor(g,0,g.length);
        
      });

    },
    getCount: function(callback) {
      db.query().select('count(*)').from('posts').execute(function(error,rows,cols) {callback(error,rows[0]["count(*)"])});
    },
    getPosts: function(callback) {
      db.query().select('*').from('posts').limit(10000).execute(function(error,rows,cols) {callback(error,rows)});
    },
    getAll: function(callback) {
      var querystr = "";
      querystr += "SELECT PI.id, PI.title, P.last_seen, PI.link, PI.price, PI.sqft, PI.bedroomcount, PI.loc_xstreet0, PI.loc_xstreet1, PI.loc_city, PI.loc_region, PI.loc_link"
      querystr += "      FROM posts P, post_instance PI where P.id = PI.post_id "
      querystr += "      AND P.section='apa' "
      querystr += "      AND PI.id = (SELECT MAX(id) FROM post_instance PI_p where PI_p.post_id = PI.post_id) "
      querystr += "      ORDER BY PI.id DESC "
      querystr += "      LIMIT 10000;    "
      
      db.query(querystr).execute(function(error,rows,cols) {callback(error,rows)});
  
      },
    
    /* Distribution methods: */
    getSomeDist: function(name,dbwhat,filters,callback) {
      filters = validateFilters(filters)
      
      var querystr = ""
      querystr +=   "SELECT " + dbwhat
      querystr +=   "    FROM posts P, post_instance PI where P.id = PI.post_id "
      querystr +=   "      AND P.section='apa' "
      querystr +=   "      AND P.city='"+filters.city+"' "
      //if (filters.pmin && filters.pmax && filters.brmin && filters.brmax && filters.sqmin && filters.sqmax) {
        querystr += "      AND (PI.price >='"       +filters.pmin        +"' AND PI.price IS NOT NULL)"; //" OR        PI.price IS NULL)"
        querystr += "      AND (PI.price <='"       +filters.pmax        +"' AND PI.price IS NOT NULL)"; //" OR        PI.price IS NULL)"        
        querystr += "      AND (PI.bedroomcount >='"+filters.brmin       +"' AND PI.bedroomcount IS NOT NULL)";//" OR PI.bedroomcount IS NULL)"
        querystr += "      AND (PI.bedroomcount <='"+filters.brmax       +"' AND PI.bedroomcount IS NOT NULL)";//" OR PI.bedroomcount IS NULL)"
        querystr += "      AND (PI.sqft >='"        +filters.sqmin       +"' AND PI.sqft IS NOT NULL)";//" OR         PI.sqft IS NULL)"
        querystr += "      AND (PI.sqft <='"        +filters.sqmax       +"' AND PI.sqft IS NOT NULL)";//" OR         PI.sqft IS NULL)"
      //}
      querystr += "      AND PI.id = (SELECT MAX(id) FROM post_instance PI_p where PI_p.post_id = PI.post_id) "
      querystr += "      ORDER BY PI.id DESC "
      querystr += "      LIMIT "+filters.limit+";    "
      
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
    for (var i = 0; i < data.length; i++) {
      js.push(data[i][index])
    }
    resJson(res,js);
  };      
}

var returnObjectDist = function(res,index) {
  return function(err,data) {
    // if (data.length > 2000) {
    //  resJson(res,{"count":data.length})
    // } else {
      resJson(res,data);
    // }
  };      
}

var returnAllObjectDist = function(res,index) {
  return function(err,data) {
    resJson(res,data);
  };      
}


/**
 * Here we set up the supported calls
 */
var routes = { }

// routes['/insert.json'] = function(req,res,next,options,db,path) {
//   db.insertGeocoded(resDBdata(res,"posts"));
// };

routes['/getLocations.json'] = function(req,res,next,options,db,path) {
  db.getLocations(resDBdata(res,"posts"));
};

var defineDistRoute = function(name,dbwhat,formatter) {
  routes['/get_'+name+'_dist.json'] = function(req,res,next,options,db,path) {
    db.getSomeDist(name, dbwhat, req.query, formatter(res,name));
  };
}
defineDistRoute("price", "PI.price",returnArrayDist);
defineDistRoute("sqft", "PI.sqft",returnArrayDist);
defineDistRoute("bedroomcount", "PI.bedroomcount",returnArrayDist);
defineDistRoute("location", "PI.id, PI.title, P.last_seen, PI.link, PI.price, PI.sqft, PI.bedroomcount, PI.loc_xstreet0, PI.loc_xstreet1, PI.loc_city, PI.loc_region, PI.loc_link, PI.lat, PI.lon",returnObjectDist);



routes["/getAll.json"] = function(req,res,next,options,db,path) {
  db.getAll(resDBdata(res,"posts_count"));
};
