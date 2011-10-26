#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

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
    curs.execute('SELECT * FROM `posts` WHERE `id` = ?', params=[id])
    row = curs.fetchone()
    if (row != None):
      return DBPost(int(row[0]), row[1], row[2], row[3], row[4], row[5])
    else:
      return None;

  def get_post_with_key(self, region, city, section, cl_id):
    self._check_connect()
    curs = self.conn.cursor()
    curs.execute('SELECT * FROM `posts` WHERE `region` = ? AND `city` = ? AND `section` = ? AND cl_id = ?', params=(region, city, section, cl_id))
    row = curs.fetchone()
    if (row != None):
      return DBPost(int(row[0]), row[1], row[2], row[3], row[4], row[5])
    else:
      return None;
      
  def get_post_with_post_as_key(self, p):
    return self.get_post_with_key(p.region, p.city, p.section, p.cl_id)
      
  def get_postis_with_post_as_key(self, post):
    if (post.id == None):
      return []
    else:
      self._check_connect()
      curs = self.conn.cursor()
      curs.execute('SELECT * FROM `post_instance` WHERE `post_id` = ?', params=[post.id])
      rows = curs.fetchall()
      postis = []
      for r in rows:
        postis.append(DBPostInstance(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14]))
      return postis
    return []
    
  def insert_post(self, p):
    self._check_connect()
    curs = self.conn.cursor()
    if (p.id == None):
      curs.execute('INSERT INTO posts (region, city, section, cl_id, created, posted_on, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?)', params=(p.region, p.city, p.section, p.cl_id, p.created, p.posted_on, p.last_seen))
      newid = curs.lastrowid
      p.id = newid;
    else:
      print "Why does this have an id already?"
    return p.id
  
  def update_post_last_seen(self, p):
    self._check_connect()
    curs = self.conn.cursor()
    if (p.id != None):
      curs.execute('UPDATE posts SET last_seen = ? WHERE `id` = ?', params=(p.last_seen, p.id))
    else:
      print "We need an IDq"
    
    
  def insert_post_instance(self, i):
    self._check_connect()
    #make sure the instance has a valid post id!
    curs = self.conn.cursor()
    if (i.post_id == None or not (type(i.post_id).__name__ == 'int' or type(i.post_id).__name__ == 'long')):
      print "Why does this not have a post_id?", type(i.post_id)
    elif (i.id == None):
      curs.execute('INSERT INTO post_instance (post_id, title, link, description, issued, price, sqft, neighborhood, bedroomcount, loc_xstreet0, loc_xstreet1, loc_city, loc_region, loc_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', params=(i.post_id, i.title, i.link, i.description, i.issued, i.price, i.sqft, i.neighborhood, i.bedroomcount, i.loc_xstreet0, i.loc_xstreet1, i.loc_city, i.loc_region, i.loc_link))
      newid = curs.lastrowid
      i.id = newid;
    else:
      print "Why does this have an id already?"
    return i.id
  

def get_db_instance():
  global CLDB_INSTANCE
  if CLDB_INSTANCE == None:
    CLDB_INSTANCE = CLdb(CLConfig.get("DB_SERV"), CLConfig.get("DB_PORT"), CLConfig.get("DB_BASE"), CLConfig.get("DB_USER"), CLConfig.get("DB_PASS"))
    return CLDB_INSTANCE
  else:
    return CLDB_INSTANCE
    
## Database Schema Follows    
    
class DBPost:
  def __init__(self, id=None, region=None, city=None, section=None, cl_id=0, created=datetime.now(), posted_on=datetime.now(), last_seen=datetime.now()):
    self.id = id
    
    self.region = region
    self.city = city
    self.section = section
    self.cl_id = cl_id
    
    self.created = created
    self.posted_on = posted_on
    self.last_seen = last_seen
    
  def __eq__(self, o):
    return (o != None) and (self.id == o.id) and (self.region == o.region) and (self.city == o.city) and (self.section == o.section) and (self.cl_id == o.cl_id)
  
  def __unicode__(self):
    if self.id == None:
      return "DBPost (%s, %s, %s, %s, %s)" % (self.region, self.city, self.section, self.cl_id, self.posted_on)
    else:
      return "DBPost ((%d): %s, %s, %s, %s, %s, %s, %s)" % (self.id, self.region, self.city, self.section, self.cl_id, self.created, self.posted_on, self.last_seen)
  
  def __str__(self):
    return self.__unicode__().encode('utf-8')
    
    
class DBPostInstance:
  def __init__(self, id=None, post_id=None, title=None, link=None, description=None, issued=datetime.now(), price=0, sqft=0, neighborhood=None, bedroomcount=0, loc_xstreet0=None, loc_xstreet1=None, loc_city=None, loc_region=None, loc_link=None):
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
    
  def __eq__(self, o):
    ti = (self.title == o.title)
    li = (self.link == o.link)
    de = (self.description == o.description)
    iss = (self.issued == o.issued)
    pr = (self.price == o.price)
    sq = (self.sqft == o.sqft)
    ne = (self.neighborhood == o.neighborhood)
    be = (self.bedroomcount == o.bedroomcount)
    
    alleq = (o != None) and ti and li and de and iss and pr and sq and ne and be
    
    # if (not alleq):
    #   print "We failed on ti=%r li=%r de=%r iss=%r pr=%r sq=%r ne=%r be=%r " % (ti, li, de, iss, pr, sq, ne, be)
    #   if (not de):
    #     print ">>>", self.description
    #     print "<<<", o.description
      
    return alleq

    
  def __unicode__(self):
    if self.id == None:      
      return "DBPostInstance (%s, %s, %s, %s, %s, %s, %s)" % (self.title, self.link, self.issued, self.price, self.neighborhood, self.bedroomcount, self.description)

    else:
      return "DBPostInstance ((%d, %d): %s, %s, %s, %s, %s, %s, %s)" % (self.id, self.post_id, self.title, self.link, self.issued, self.price, self.neighborhood, self.bedroomcount, self.description)
  
  def __str__(self):
    return self.__unicode__().encode('utf-8')
