#!/usr/bin/env python
# encoding: utf-8

import oursql

import CLConfig

CLDB_INSTANCE = None

#ORM Wrapper around database. Exposes API for talking to data.
#Duplicates are denied my MySQL's unique constraints
class CLdb:
  def __init__(self, server, port, dbname, user, passwd):
    self.server = server
    self.port = port
    self.dbname = dbname
    self.user = user
    self.passwd = passwd
    self.connected = False
    self.conn = None
    self._connect()
    
  def _connect(self):
    self.conn = oursql.connect(host=str(self.server), user=str(self.user), passwd=str(self.passwd), db=str(self.dbname), port=int(self.port), charset="utf8", use_unicode=True)
    self.connected = True
  
  def _check_connect(self):
    if (not self.connected):
      _connect()
    
  def get_post_with_id(self, id):
    self._check_connect()
    curs = self.conn.cursor()
    curs.execute('SELECT * FROM `posts` WHERE `id` = ?', params=[0])
    row = curs.fetchone()
    if (row != None):
      return DBPost(int(row[0]), row[1], row[2], row[3], row[4], row[5])
    else:
      return None;

  def get_post_with_key(self, region, city, section, cl_id):
    self._check_connect()
    curs = self.conn.cursor()
    curs.execute('SELECT * FROM `posts` WHERE `region` = ? AND `city` = ? AND `section` = ? AND cl_id = ?', params=(region, city, section, int(cl_id)))
    row = curs.fetchone()
    if (row != None):
      return DBPost(int(row[0]), row[1], row[2], row[3], row[4], row[5])
    else:
      return None;
      
  def get_post_with_post_as_key(p):
    return get_post_with_key(p.region, p.city, p.section, p.cl_id)
    
  def get_post_instance_with_ids(self, id=None, post_id=None):
    self._check_connect()
    
    #implement
    return DBPostInstance()
    
  def insert_post(self, p):
    self._check_connect()
    curs = self.conn.cursor()
    if (p.id == None):
      curs.execute('INSERT INTO posts (region, city, section, cl_id) VALUES (?, ?, ?, ?)', params=(p.region, p.city, p.section, p.cl_id))
      newid = curs.lastrowid
      p.id = newid;
    else:
      print "Why does this have an id already?"
      
    return DBPost()
    
  def insert_post_instance(self, db_post_instance):
    self._check_connect()
    #make sure the instance has a valid post id!
    
    #returns post with correct ID's filled out
    return DBPostInstance()
  

def get_db_instance():
  global CLDB_INSTANCE
  if CLDB_INSTANCE == None:
    CLDB_INSTANCE = CLdb(CLConfig.get("DB_SERV"), CLConfig.get("DB_PORT"), CLConfig.get("DB_BASE"), CLConfig.get("DB_USER"), CLConfig.get("DB_PASS"))
    return CLDB_INSTANCE
  else:
    return CLDB_INSTANCE
    
## Database Schema Follows    
    
class DBPost:
  def __init__(self, id=None, region=None, city=None, section=None, cl_id=0, first_seen=None):
    self.id = id
    
    self.region = region
    self.city = city
    self.section = section
    self.cl_id = 0
    self.first_seen = first_seen
    
  def __eq__(self, o):
    return (self.id == o.id) and (self.region == o.region) and (self.city == o.city) and (self.section == o.section) and (self.cl_id == o.cl_id)
  
  def __unicode__(self):
    return "DBPost (%d, %s, %s, %s, %s, %s)" % (self.id, self.region, self.city, self.section, self.cl_id, self.first_seen)
  def __str__(self):
    return "DBPost (%d, %s, %s, %s, %s, %s)" % (self.id, self.region, self.city, self.section, self.cl_id, self.first_seen)
    
    
class DBPostInstance:
  def __init__(self, id=0, post_id=0, title=None, link=None, description=None, issued=None, price=0, sqft=0, neighborhood=None, bedroomcount=0, loc_xstreet0=None, loc_xstreet1=None, loc_city=None, loc_region=None, loc_link=None):
    self.id = id
    self.post_id = post_id
    
    self.title = title
    self.link = link
    self.description = description
    self.issued = issued
    self.price = price
    self.sqft = sqft
    self.neighborhood = neighborhood
    self.bedroomcount = bedroomcount
    self.loc_xstreet0 = loc_xstreet0
    self.loc_xstreet1 = loc_xstreet1
    self.loc_city = loc_city
    self.loc_region = loc_region
    self.loc_link = loc_link