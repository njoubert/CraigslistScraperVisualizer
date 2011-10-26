#!/usr/bin/env python
# encoding: utf-8


from StringIO import StringIO
import os
try:
  import json
except ImportError:
  import simplejson as json


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../../config.json")
CONFIG_DATA = json.loads(open(CONFIG_FILE,'r').read())

def get(k,default=None):
  global CONFIG_DATA
  if default == None:
    return CONFIG_DATA[k];
  else:
    return CONFIG_DATA.get(k,default)