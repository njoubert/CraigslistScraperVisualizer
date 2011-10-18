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

CL_RSS_PAGE = "http://sfbay.craigslist.org/sfc/hhh/index.rss"

usage="""
This is a craigslist scraper script.
"""

optparser = OptionParser(usage=usage)
optparser.add_option("-s", "--simple", action="store_true", default=False,
      help="Should we just save the XML doc periodically")

(options, args) = optparser.parse_args()


def pull_craigslist():
  try:
    s = urlopen(CL_RSS_PAGE)
    html = s.read()
    return html
  except IOError:
    print "Could not open html page."
    exit

def parse_craigslist(document):
    return CLParser(document)


def main():
  if options.simple:
    basepath = os.path.join(os.getcwd(), "data", socket.gethostname())

    while True:
      document = pull_craigslist()
      tid = int(time.time())
      td = datetime.date.today()  
      filedir = os.path.join(basepath, "%d_%d" % (td.year, td.month))
      try:
        os.makedirs(filedir)
      except OSError:
        if !(os.path.exists(filedir)):
          print "Could not create data directory! Exiting..."
          exit
      text_file = open(os.path.join(filedir,"dl_%d.xml" % tid), "w")
      text_file.write(document)
      text_file.close()
      waitsec = 540 + random.randint(-300,180)
      print "Pulled document from craigslist at %d. Next pull in %s seconds" % (tid, waitsec)
      time.sleep(waitsec)
    
  else:    
    try:
      parser = parse_craigslist(pull_craigslist())
    except IOError:
      print "Couldn't parse"
       
if __name__ == '__main__':
  sys.exit(main())

