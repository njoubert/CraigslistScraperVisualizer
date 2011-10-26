#!/usr/bin/env python
# encoding: utf-8
"""
CLInputPipeline.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.

This file is responsible for taking in Craigslist posts and filtering it into the database

"""

import CLSchema
import CLdb

def arrive(cl_item):
  print "Arrive ", cl_item.link
  
  #Construct a suggested database entry from the item
  
  #Check how to fit this into the database:
    #is it a brand new post? Add it
    #if the post exists, is this a new version of it? Add only the instance
    #if it's already in there, just move on
  db = CLdb.get_db_instance()
  
  p2 = db.get_post_with_key("sfbay", "sfc", "hhh", 0)

  p2.id = None
  db.insert_post(p2)