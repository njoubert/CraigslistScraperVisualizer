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
import CLConfig
import CLInputPipeline

CL_RSS_PAGE = "http://sfbay.craigslist.org/sfc/hhh/index.rss"
WAIT_TIME = 12*60
WAIT_OFFSET = 5*60

usage="""This is a craigslist analyzer script."""

optparser = OptionParser(usage=usage)

optparser.add_option("-d", "--data-directory", type="string", default=os.path.join(os.path.dirname(__file__), "../../data", socket.gethostname()),
      help="Where is the data stored?")

(options, args) = optparser.parse_args()
BASEPATH = os.path.abspath(options.data_directory)

def get_all_raw_files_inorder():
  allfiles = []
  for root, dirs, files in os.walk(BASEPATH):
    for name in files:
      fileName, fileExtension = os.path.splitext(name)
      if (fileExtension == ".xml"):
        allfiles.append(os.path.join(root,name))
  def fname_extractor(name):
    return os.path.split(name)[1]
  sorted(allfiles,key=fname_extractor)
  return allfiles
  
def get_docs_generator():
  files = get_all_raw_files_inorder()
  parser = CLParser()
  for f in files:
    raw_data = open(f).read()
    doc = parser.parse(raw_data)
    if doc != None:
      yield doc
    else:
      print "Could not parse %s." % f

def assert_all_post_cl_ids_are_unique(doclist):
  links = [(i.post_cl_id, i.title) for d in doclist for i in d.items]
  icount = {}
  print "counting..."
  for l in links:
    contents = icount.get(l[0],[])
    contents.append(l[1])
    icount[l[0]] = contents
  howmany_not_unique = 0
  for l in links:
    seen = set()
    for titles in icount[l[0]]:
      seen.add(titles)
    if len(seen) > 1:
      print l[0]
      print seen
      howmany_not_unique += 1
  return howmany_not_unique < 1
  
def main():
  docgen = get_docs_generator()
  docs = []
  for d in docgen:
    docs.append(d)
  
  for d in docs:
    for post in d.items:
      CLInputPipeline.arrive(post)
  
  #isUnique = assert_all_post_cl_ids_are_unique(docs)
  #print "Are all post ID's unique?", isUnique
  
if __name__ == '__main__':
  sys.exit(main())

