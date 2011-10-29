#!/usr/bin/env python
# encoding: utf-8
"""
scraper.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.

See:

http://docs.python.org/library/urllib.html
"""

import pdb
import sys
import os
import random
import time
import datetime
import socket
from urllib import *
from optparse import OptionParser

from CLSchema import *
from CLParser import *
import CLConfig
import CLInputPipeline


# CL_RSS_PAGE = "http://sfbay.craigslist.org/sfc/hhh/index.rss"
# WAIT_TIME = 12*60
# WAIT_OFFSET = 5*60

usage="""This is a craigslist scraper script."""

optparser = OptionParser(usage=usage)
optparser.add_option("-s", "--simple", action="store_true", default=False,
      help="Should we just save the XML doc periodically")

optparser.add_option("-d", "--data-directory", type="string", default=os.path.join(os.path.dirname(__file__), "../../data", socket.gethostname()),
      help="Where do we save data?")
  

(options, args) = optparser.parse_args()
BASEPATH = os.path.abspath(options.data_directory)

def pull_craigslist():
  try:
    s = urlopen(CLConfig.get("CL_RSS_PAGE"))
    html = s.read()
    return html
  except IOError:
    print "Could not open html page."
    exit

def parse_craigslist(document):
  parser = CLParser()
  return parser.parse(document)

def simple_save_current_feed(parse=False):
  doc = pull_craigslist()
  document = parse_craigslist(doc)
  td = datetime.now()  
  filedir = os.path.join(BASEPATH, "%d_%d" % (td.year, td.month))
  try:
    os.makedirs(filedir)
  except OSError:
    if (not os.path.exists(filedir)):
      print "Could not create data directory! Exiting..."
      exit
  
  if parse:
    for post in document.items:
      try:
        CLInputPipeline.arrive(document, post)
      except:
        print "Could not add item %s", post.link
      
  tid = int(time.time())
  text_file = open(os.path.join(filedir,"dl_%d.xml" % tid), "w")
  text_file.write(doc)
  text_file.close()
  return document.channel.updateBase

def save_loop(parse=False):
  while True:
    updateBase = simple_save_current_feed(parse=parse)
    waitsec = CLConfig.get("WAIT_TIME") + random.randint(-CLConfig.get("WAIT_OFFSET"),CLConfig.get("WAIT_OFFSET"))
    print "Pulled craigslist data with timestamp %s. Next pull in %s seconds" % (updateBase, waitsec)
    time.sleep(waitsec)

def main():
  if options.simple:
    save_loop(parse=False)
  else:    
    try:
      save_loop(parse=True)
    except IOError:
      print "Couldn't parse"
       
if __name__ == '__main__':
  sys.exit(main())

