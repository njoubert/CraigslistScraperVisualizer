#!/usr/bin/env python
# encoding: utf-8
"""
CLInputPipeline.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.

This file is responsible for taking in Craigslist posts and filtering it into the database

"""
from datetime import datetime

import CLSchema
import CLdb

def arrive(cl_doc, cl_item):
  db = CLdb.get_db_instance()
  
  #Construct a suggested database entry from the item
  #Check how to fit this into the database:
    #is it a brand new post? Add it
    #if the post exists, is this a new version of it? Add only the instance
    #if it's already in there, just move on

  
  post, post_i = translate_cl_item_to_db_objects(cl_item, cl_doc)
  
  dupepost = db.get_post_with_post_as_key(post)
  if (dupepost == None):
    print "Saving brand new post ", cl_item.link
    id = db.insert_post(post)
    post_i.post_id = id
    db.insert_post_instance(post_i)
  else:    
    dupepost.last_seen = cl_doc.channel.get_datetime()
    db.update_post_last_seen(dupepost)
    post_i.post_id = dupepost.id
    
    dupepostis = db.get_postis_with_post_as_key(dupepost)
    found = False
    for dpi in dupepostis:
      if (dpi == post_i):
        found = True
        break
    
    if (found):
      print "Ignoring duplicate ", cl_item.link, " tested ", len(dupepostis)
    else:
      db.insert_post_instance(post_i)
      print "Saving new instance of %d, %s" % (dupepost.id, cl_item.link)

    
    
def translate_cl_item_to_db_objects(ci, cd):
  post = CLdb.DBPost()
  posti = CLdb.DBPostInstance()
  
  post.region = ci.post_region
  post.city = ci.post_city
  post.section = ci.post_section
  post.cl_id = ci.post_cl_id
  post.posted_on = ci.get_datetime()
  post.last_seen = cd.channel.get_datetime()
  
  
  posti.title = ci.title
  posti.link = ci.link
  posti.description = ci.description
  posti.issued = ci.get_datetime()
  
  try:
    dft = ci.parse_derived_title_data()
    posti.title = dft['titletext']
    posti.price = dft['price']
    posti.sqft =  dft['sqft']
    posti.bedroomcount = dft['bd']
    posti.neighborhood = dft['neighborhood']
  except:
    pass

  try:
    dfd = ci.parse_derived_description_data()
    posti.loc_xstreet0 = dfd['loc_xstreet0']
    posti.loc_xstreet1 = dfd['loc_xstreet1']
    posti.loc_city = dfd['loc_city']
    posti.loc_region = dfd['loc_region']
    posti.loc_link = dfd['loc_link']
  except:
    pass
  
  return (post, posti)