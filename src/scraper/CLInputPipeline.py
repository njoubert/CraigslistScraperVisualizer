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
  print "Arrival of ", cl_item.link

  #Construct a suggested database entry from the item
  #Check how to fit this into the database:
    #is it a brand new post? Add it
    #if the post exists, is this a new version of it? Add only the instance
    #if it's already in there, just move on

  
  post, post_i = translate_cl_item_to_db_objects(cl_item, cl_doc)
  dupepost = db.get_post_with_post_as_key(post)
  if (dupepost == None):
    #Just add all the new data, it's new!
    print "New post woot"
    db.insert_post(post)
  else:
    dupepost.last_seen = cl_doc.channel.get_datetime()
    db.update_post_last_seen(dupepost)
    #Gotta check for more info
    print "Post already exists, updating last_seen time ", dupepost
    
    
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
  
  return (post, posti)
  
  
  
  
# db = CLdb.get_db_instance()
# 
# p1 = CLdb.DBPost(region="sfbay", city="sfc", section="apa", cl_id=5)
# try:
#   db.insert_post(p1)
# except:
#   pass
# 
# 
# p2 = db.get_post_with_post_as_key(p1)
# 
# p2.id = None
# p2.region = "pen"
# try:
#   db.insert_post(p2)
# except:
#   pass
