#!/usr/bin/env python

import unittest
import percentcoding
import string


class CodecTestCase(unittest.TestCase):

  def __init__(self, **keywords):
    unittest.TestCase.__init__(self)

    for k, v in keywords.items():
      setattr(self, k, v)

  def runTest(self):

    codec = percentcoding.Codec( self.safe )
    self.assertEqual( self.decoded, codec.decode(self.encoded) )
    self.assertEqual( self.encoded, codec.encode(self.decoded) )

  def shortDescription(self):
    return self.name


URI_UNRESERVED = string.uppercase + string.lowercase + string.digits + "-_.~"
URI_RESERVED = "!*'();:@&=+$,/?#[]"
URI_SAFE = ''.join( set([c for c in URI_UNRESERVED]) - set([c for c in URI_RESERVED]) )

# TODO add more coverage
# TODO add tests with different safe character sets
# TODO add tests that only work in one direction (eg because non-canonical encoding)

TRUTH = [
  ("empty", URI_SAFE, "", ""),
  ("lone percent", URI_SAFE, "%", "%25"),
  ("double percent", URI_SAFE, "%%", "%25%25"),
  ("whitespace", URI_SAFE, " \r\n\t\v\f", "%20%0d%0a%09%0b%0c"),
  ("unreserved", URI_SAFE, URI_UNRESERVED, URI_UNRESERVED),
  ("null", URI_SAFE, "\x00", "%00"),
  ("embedded null", URI_SAFE, "abc\x00def", "abc%00def"),
  ("long", URI_SAFE, " xyz " * 1000, "%20xyz%20" * 1000),
  ("ampersand", URI_SAFE, "&", "%26"),
  ("symbols", URI_SAFE, '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', "%21%22%23%24%25%26%27%28%29%2a%2b%2c-.%2f%3a%3b%3c%3d%3e%3f%40%5b%5c%5d%5e_%60%7b%7c%7d~"),
]


def main():

  suite = unittest.TestSuite()
  i = 0

  for name, safe, decoded, encoded in TRUTH:

    suite.addTest(CodecTestCase(
      name="test %d %s" % (i,name),
      safe=safe,
      decoded=decoded,
      encoded=encoded,
    ))

    i += 1

  runner = unittest.TextTestRunner(verbosity=2)
  results = runner.run(suite)

  if len(results.failures) or len(results.errors):
    return 1
  else:
    return 0


if __name__ == '__main__':
  import sys
  sys.exit(main())

