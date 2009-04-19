#!/usr/bin/env python
from __future__ import with_statement
import sys
import simplejson
import pprint

with file(sys.argv[1],'r+') as f:
    print pprint.pprint(simplejson.load(f))
