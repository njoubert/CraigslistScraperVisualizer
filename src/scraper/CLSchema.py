#!/usr/bin/env python
# encoding: utf-8
"""
CLSchema.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.
"""

from datetime import datetime
import re

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
    
  def parse_derived_title_data(self):
    #there's a decent chance that this will go horribly wrong...
    
    #From the title:
    # words (neighborhood) $money xbd xsqft (\(\w+\))? (\$ )? (\d+bd)? 
    sqft = re.findall('(\d+)sqft', self.title)
    if (len(sqft) > 0):
      sqft = int(sqft[-1])
    else:
      sqft = None
      
    price = re.findall('\$(\d+)', self.title)
    if (len(price) > 0):
      price = int(price[-1])
    else:
      price = None
      
    bd = re.findall('(\d+)bd', self.title)
    if (len(bd) > 0):
      bd = int(bd[-1])
    else:
      bd = None
      
    tt = self.title
    neighborhood = re.findall('(\(.*\))', self.title)
    if (len(neighborhood) > 0):
      neighborhood = neighborhood[-1]
      parts = tt.partition(neighborhood)
      tt = parts[0].rstrip()
    else:
      neighborhood = None

    derived = {
      'price': price,
      'sqft': sqft,
      'bd': bd,
      'neighborhood': neighborhood,
      'titletext': tt
    }
    
    return derived
    
  def parse_derived_description_data(self):
    return {'fuck':'this'}
        
class CLChannel:
  def __init__(self, link, updateBase, updateFrequency, updatePeriod, items):
    self.link              = link
    
    self.updateBase        = updateBase
    self.updateFrequency   = updateFrequency
    self.updatePeriod      = updatePeriod
    self.items             = items
    
  def get_datetime(self):
    return craigslist_datestr_to_datetime(self.updateBase)