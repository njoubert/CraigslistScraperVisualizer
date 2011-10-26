#!/usr/bin/env python
# encoding: utf-8
"""
CLSchema.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.
"""
from datetime import datetime

CL_DATEFORMAT = "%Y-%m-%dT%H:%M:%S"

def craigslist_datestr_to_datetime(str):
  l, m, r = str.rpartition("-") #unfortunately we have to drop TZ at the moment.
  newdate = l
  dt = datetime.strptime(newdate, CL_DATEFORMAT)
  return dt

class CLDocument:
  def __init__(self):
    self.channel = None
    self.items = []

class CLItem:
  def __init__(self, title, link, description, date, source, issued, post_region="sfbay", post_city="sfb", post_section="hhh", post_cl_id="0000000000"):
    self.title             = title
    self.link              = link        
    self.description       = description 
    self.date              = date        
    self.source            = source      
    self.issued            = issued      
        
    self.post_region       = post_region
    self.post_city         = post_city
    self.post_section      = post_section
    self.post_cl_id        = post_cl_id
    
  def get_datetime(self):
    return craigslist_datestr_to_datetime(self.date)
        
class CLChannel:
  def __init__(self, link, updateBase, updateFrequency, updatePeriod, items):
    self.link              = link
    
    self.updateBase        = updateBase
    self.updateFrequency   = updateFrequency
    self.updatePeriod      = updatePeriod
    self.items             = items
    
  def get_datetime(self):
    return craigslist_datestr_to_datetime(self.updateBase)