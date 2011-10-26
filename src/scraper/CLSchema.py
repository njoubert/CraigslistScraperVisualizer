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
    # there's a decent chance that this will go horribly wrong... We try to protect against that breaking stuff
    # From the title:
    # words (neighborhood) $money xbd xsqft (\(\w+\))? (\$ )? (\d+bd)? 
    sqft = re.findall('(\d+)sqft', self.title)
    if (len(sqft) > 0):
      try:
        sqft = int(sqft[-1])
      except:
        sqft = None
    else:
      sqft = None
      
    price = re.findall('\$(\d+)', self.title)
    if (len(price) > 0):
      try:
        price = int(price[-1])
      except:
        price = None
    else:
      price = None
      
    bd = re.findall('(\d+)bd', self.title)
    if (len(bd) > 0):
      try:
        bd = int(bd[-1])
      except:
        bd = None
    else:
      bd = None
      
    tt = self.title
    try:
      neighborhood = re.findall('(\(.*\))', self.title)
      if (len(neighborhood) > 0):
        neighborhood = neighborhood[-1]
        parts = tt.partition(neighborhood)
        tt = parts[0].rstrip()
      else:
        neighborhood = None
    except:
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
    #again, this might crash or burn bad. we try to contain that. it's okay if we don't get this data right now.
    
    d = self.description.partition("<!-- START CLTAGS -->")[2]
    
    xs0 = re.search('<!-- CLTAG xstreet0=(.*) -->', d)
    if (xs0):
      xs0 = xs0.group(1)
    else:
      xs0 = None

    xs1 = re.search('<!-- CLTAG xstreet1=(.*) -->', d)
    if (xs1):
      xs1 = xs1.group(1)
    else:
      xs1 = None

    city = re.search('<!-- CLTAG city=(.*) -->', d)
    if (xs0):
      city = city.group(1)
    else:
      city = None

    region = re.search('<!-- CLTAG region=(.*) -->', d)
    if (region):
      region = region.group(1)
    else:
      region = None

    maplink = re.search('<a target="_blank" href="(.*)">google map</a>', d)
    if (maplink):
      maplink = maplink.group(1)
    else:
      maplink = None

    derived = {
      'loc_xstreet0':xs0,
      'loc_xstreet1':xs1,
      'loc_city':city,
      'loc_region':region,
      'loc_link':maplink,

    }
    return derived
        
class CLChannel:
  def __init__(self, link, updateBase, updateFrequency, updatePeriod, items):
    self.link              = link
    
    self.updateBase        = updateBase
    self.updateFrequency   = updateFrequency
    self.updatePeriod      = updatePeriod
    self.items             = items
    
  def get_datetime(self):
    return craigslist_datestr_to_datetime(self.updateBase)