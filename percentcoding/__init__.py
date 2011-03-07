#!/usr/bin/env python

from percentcoding.cext import *
import string

URI_UNRESERVED = string.uppercase + string.lowercase + string.digits + "-_.~"
URI_RESERVED = "!*'();:@&=+$,/?#[]"
URI_SAFE = ''.join( set([c for c in URI_UNRESERVED]) - set([c for c in URI_RESERVED]) )
URI_SAFE_FORM = URI_SAFE.replace('+','')

urlcoding = Codec(URI_SAFE)

def quote(s):
  global urlcoding
  return urlcoding.encode(s)

def unquote(s):
  global urlcoding
  return urlcoding.decode(s)

