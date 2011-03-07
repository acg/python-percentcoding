#!/usr/bin/env python

import sys, os
sys.path.append( os.path.dirname(sys.argv[0])+"/.." )
from percentcoding import quote, unquote

s = "This is a test."
escaped = quote(s)
print escaped
assert(s == unquote(escaped))

