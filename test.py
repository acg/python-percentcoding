#!/usr/bin/env python
# coding=utf8

import unittest
import percentcoding
import string

class FunctionTestCase(unittest.TestCase):

  def __init__(self, **keywords):
    unittest.TestCase.__init__(self)
    self.args = []
    self.kwargs = {}

    for k, v in keywords.items():
      setattr(self, k, v)

  def runTest(self):
    self.assertEqual( self.func(*self.args,**self.kwargs), self.expected )

  def shortDescription(self):
    return self.name


URI_UNRESERVED = string.uppercase + string.lowercase + string.digits + "-_.~"
URI_RESERVED = "!*'();:@&=+$,/?#[]"
URI_SAFE = ''.join( set([c for c in URI_UNRESERVED]) - set([c for c in URI_RESERVED]) )

TEST_ENCODE = 0x1
TEST_DECODE = 0x2
TEST_BOTH = TEST_ENCODE | TEST_DECODE

# TODO add more coverage
# TODO add tests with different safe character sets

TRUTH = [
  ("empty",          TEST_BOTH, URI_SAFE, "", ""),
  ("lone percent",   TEST_BOTH, URI_SAFE, "%", "%25"),
  ("double percent", TEST_BOTH, URI_SAFE, "%%", "%25%25"),
  ("whitespace",     TEST_BOTH, URI_SAFE, " \r\n\t\v\f", "%20%0d%0a%09%0b%0c"),
  ("unreserved",     TEST_BOTH, URI_SAFE, URI_UNRESERVED, URI_UNRESERVED),
  ("null",           TEST_BOTH, URI_SAFE, "\x00", "%00"),
  ("embedded null",  TEST_BOTH, URI_SAFE, "abc\x00def", "abc%00def"),
  ("long",           TEST_BOTH, URI_SAFE, " xyz " * 1000, "%20xyz%20" * 1000),
  ("ampersand",      TEST_BOTH, URI_SAFE, "&", "%26"),
  ("symbols",        TEST_BOTH, URI_SAFE, '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', "%21%22%23%24%25%26%27%28%29%2a%2b%2c-.%2f%3a%3b%3c%3d%3e%3f%40%5b%5c%5d%5e_%60%7b%7c%7d~"),
  ("unicode encode", TEST_ENCODE, URI_SAFE, u'“Aha”', '%e2%80%9cAha%e2%80%9d'),
  ("unicode decode", TEST_DECODE, URI_SAFE, '\xe2\x80\x9cAha\xe2\x80\x9d', '%e2%80%9cAha%e2%80%9d'),
]


def main():

  suite = unittest.TestSuite()
  i = 0

  for name, flags, safe, decoded, encoded in TRUTH:

    codec = percentcoding.Codec(safe)

    if flags & TEST_ENCODE:

      suite.addTest(FunctionTestCase(
        name="test %d %s" % (i,name),
        func=codec.encode,
        args=[decoded],
        expected=encoded,
      ))

      i += 1

    if flags & TEST_DECODE:

      suite.addTest(FunctionTestCase(
        name="test %d %s" % (i,name),
        func=codec.decode,
        args=[encoded],
        expected=decoded,
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

