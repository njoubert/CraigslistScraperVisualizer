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
  def __init__(self):
    self.raw_data = None
    self.document = None
    self.__parsed = False
  
  def parse(self, raw_data):
    self.raw_data = raw_data
    self.document = None
    self.__parsed = False
    try:
      self.dom = xml.dom.minidom.parseString(self.raw_data)
      self.document = CLDocument()
      self._handleDom(self.dom)
      self.__parsed = True
    except IndexError:
      self.__parsed = False
      
    return self.document
    
  def _handleDom(self, dom):
    self._handleChannel(dom.getElementsByTagName("channel")[0])
    self._handleItems(dom.getElementsByTagName("item"))
    
  def _handleChannel(self, dom):
    link = dom.getElementsByTagName("link")[0].childNodes[0].data
    updateBase = dom.getElementsByTagName("syn:updateBase")[0].childNodes[0].data
    updateFrequency = int(dom.getElementsByTagName("syn:updateFrequency")[0].childNodes[0].data)
    updatePeriod = dom.getElementsByTagName("syn:updatePeriod")[0].childNodes[0].data
    items = dom.getElementsByTagName("items")[0].getElementsByTagName("rdf:Seq")[0].getElementsByTagName("rdf:li")
    self.document.channel = CLChannel(link, updateBase, updateFrequency, updatePeriod, items)
    
  def _handleItems(self, dom):
    for i in dom:
      title = i.getElementsByTagName("title")[0].childNodes[0].data
      link = i.getElementsByTagName("link")[0].childNodes[0].data
      description = i.getElementsByTagName("description")[0].childNodes[0].data
      date = i.getElementsByTagName("dc:date")[0].childNodes[0].data
      source = i.getElementsByTagName("dc:source")[0].childNodes[0].data
      issued = i.getElementsByTagName("dcterms:issued")[0].childNodes[0].data
      
      m = re.match('http://sfbay\.craigslist\.org/(\w\w\w)/(\w\w\w)/(\d+)\.html', link)
      post_city= m.group(1)
      post_section = m.group(2)
      post_cl_id = m.group(3)
      
      item = CLItem(title, link, description, date, source, issued, post_city=post_city, post_section=post_section, post_cl_id=post_cl_id)
      self.document.items.append(item)