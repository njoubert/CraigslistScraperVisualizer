#!/usr/bin/env python
# encoding: utf-8
"""
util.py

Created by Niels Joubert on 2011-10-17.
Copyright (c) 2011 Stanford. All rights reserved.
"""

def to_unicode_or_bust(obj, encoding='utf-8'):
  if isinstance(obj, basestring):
    if not isinstance(obj, unicode):
      obj = unicode(obj, encoding)
  return obj