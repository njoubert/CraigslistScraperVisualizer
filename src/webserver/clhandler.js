
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
  , url = require('url');

/**
 * Expose the entrypoint api.
 */
exports = module.exports = function clhandler(options){
  options = options || {}
  
  if (!options.hasOwnProperty("DB_USER")) throw new Error('clhandler api requires DB_USER in options');
  
  //attempt to connect to database
  
  return function clhandler(req,res,next) {
    options.path = req.url;
    options.getOnly = true;
    handle(req,res,next,options);
  };
};

/**
 * Attempt to handle a request for the given .
 *
 * @param {ServerRequest}
 * @param {ServerResponse}
 * @param {Function} next
 * @param {Object} options
 * @api private
 */

var handle = exports.handle = function(req,res,next,options){
  options = options || {};
  if (!options.path) throw new Error('path required');
  
  //send response
  var path = url.parse(options.path);
      
  if (routes.hasOwnProperty(path.pathname)) {
    return routes[path.pathname](req,res,next,options,path);
  }
  return next();
}

/**
 * Stringifies a JS object and writes it to response
 *
 * @param {ServerResponse}
 * @param {Object} jsobject
 */
var resJson = function(res,jsobject) {
  res.writeHeader(200, {"Content-Type":"application/json"});
  res.write(JSON.stringify(jsobject));
  res.end()  
}

/**
 * Here we set up the supported calls
 */
var routes = { }

routes['/getAll.json'] = function(req,res,next,options,path) {
  next(new Error('Not implemented yet'));
};

routes["/getCount.json"] = function(req,res,next,options,path) {
  next(new Error('Not implemented yet'));
};

routes["/getInfo.json"] = function(req,res,next,options,path) {
  js = {
    "options":options,
    "path":path
  }
  resJson(res,js);
};
