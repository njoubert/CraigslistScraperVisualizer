#!/usr/bin/env python
# encoding: utf-8
"""
CLParser.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.

See:

http://docs.python.org/library/xml.dom.minidom.html
http://docs.python.org/library/xml.dom.html#module-xml.dom
"""



import xml.dom.minidom
import re

from CLSchema import *
import pdb

class CLParser:
  def __init__(self, document):
    self.raw_data = document
    self.items = []
    self.channel = None
    self._parse()
    self.__parsed = False
  
  def _parse(self):
    print "Parsing CL RSS feed"
    try:
      self.dom = xml.dom.minidom.parseString(self.raw_data)
      self._handleDom(self.dom)
      self.__parsed = True
    except IndexError:
      self.__parsed = False
    
  def _handleDom(self, dom):
    self._handleChannel(dom.getElementsByTagName("channel")[0])
    self._handleItems(dom.getElementsByTagName("item"))
    
  def _handleChannel(self, dom):
    link = dom.getElementsByTagName("link")[0].childNodes[0].data
    updateBase = dom.getElementsByTagName("syn:updateBase")[0].childNodes[0].data
    updateFrequency = int(dom.getElementsByTagName("syn:updateFrequency")[0].childNodes[0].data)
    updatePeriod = dom.getElementsByTagName("syn:updatePeriod")[0].childNodes[0].data
    items = dom.getElementsByTagName("items")[0].getElementsByTagName("rdf:Seq")[0].getElementsByTagName("rdf:li")
    self.channel = CLChannel(link, updateBase, updateFrequency, updatePeriod, items)
    
  def _handleItems(self, dom):
    for i in dom:
      title = i.getElementsByTagName("title")[0].childNodes[0].data
      link = i.getElementsByTagName("link")[0].childNodes[0].data
      description = i.getElementsByTagName("description")[0].childNodes[0].data
      date = i.getElementsByTagName("dc:date")[0].childNodes[0].data
      source = i.getElementsByTagName("dc:source")[0].childNodes[0].data
      issued = i.getElementsByTagName("dcterms:issued")[0].childNodes[0].data
      
      m = re.match('http://sfbay\.craigslist\.org/(\w\w\w)/(\w\w\w)/(\d+)\.html', link)
      post_location = m.group(1)
      post_type = m.group(2)
      post_link_id = m.group(3)
      
      item = CLItem(title, link, description, date, source, issued, post_location=post_location, post_type=post_type, post_link_id=post_link_id)
      self.items.append(item)