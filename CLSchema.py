#!/usr/bin/env python
# encoding: utf-8
"""
CLSchema.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.
"""


class CLItem:
  def __init__(self, title, link, description, date, source, issued, post_location="sfb", post_type="hhh", post_link_id="0000000000"):
    self.title             = title
    self.link              = link        
    self.description       = description 
    self.date              = date        
    self.source            = source      
    self.issued            = issued      
        
    self.post_location     = post_location
    self.post_type         = post_type
    self.post_link_id      = post_link_id
        
class CLChannel:
  def __init__(self, link, updateBase, updateFrequency, updatePeriod, items):
    self.link              = link
    
    self.updateBase        = updateBase
    self.updateFrequency   = updateFrequency
    self.updatePeriod      = updatePeriod
    self.items             = items