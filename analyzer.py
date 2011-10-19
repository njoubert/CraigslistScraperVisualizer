#!/usr/bin/env python
# encoding: utf-8
"""
analyzer.py

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
WAIT_TIME = 12*60
WAIT_OFFSET = 5*60

usage="""This is a craigslist analyzer script."""

optparser = OptionParser(usage=usage)

optparser.add_option("-d", "--data-directory", type="string", default=os.path.join(os.getcwd(), "data", socket.gethostname()),
      help="Where is the data stored?")
  

(options, args) = optparser.parse_args()
BASEPATH = os.path.abspath(options.data_directory)



def get_all_raw_files_inorder():
  allfiles = []
  for root, dirs, files in os.walk(BASEPATH):
    for name in files:
      allfiles.append(os.path.join(root,name))
  def fname_extractor(name):
    return os.path.split(name)[1]
  sorted(allfiles,key=fname_extractor)
  return allfiles
    
def main():
  files = get_all_raw_files_inorder()
  parser = CLParser()
  for f in files:
    raw_data = open(f).read()
    doc = parser.parse(raw_data)
    print doc.channel.updateBase
       
if __name__ == '__main__':
  sys.exit(main())

