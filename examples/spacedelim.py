#!/usr/bin/env python

import sys, os
sys.path.append( os.path.dirname(sys.argv[0])+"/.." )
import percentcoding
import string

ascii = set([chr(c) for c in xrange(255)])
whitespace = set([c for c in string.whitespace])
safe = ''.join( ascii - whitespace )
codec = percentcoding.Codec(safe)

record = [ "a\nleaf\nfalls", " X\tY\tZ " ]
print " ".join([ codec.encode(v) for v in record])

