#!/usr/bin/env python

"""percentcoding: fast percent encoding and decoding

An example of percent encoding is the one defined for URIs in RFC 3986. Percent encoding can also be used for general purpose text escaping. Unlike C backslash escaping, which requires that every reserved character be explicitly named (eg. 0x0a corresponds to \\n), percent encoding can easily accommodate an arbitrary set of reserved characters. For the specific case of URI escaping, the percentcoding library provides a 10x faster drop-in replacement for the urllib.quote, urllib.unquote, urllib.quote_plus, and urllib.unquote_plus functions.
"""

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Topic :: Text Processing :: General
Topic :: Text Processing :: Filters
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: OS Independent
"""

from distutils.core import setup, Extension

doclines = __doc__.split("\n")

setup(
  name='percentcoding',
  version='0.1',
  ext_modules=[
    Extension(
      'percentcoding.cext',
      [
        'codec.c',
        'module.c',
        'percentcoding.c',
      ],
      extra_compile_args=['-fPIC'],
      define_macros=[],
    ),
  ],
  packages=['percentcoding'],
  maintainer="Alan Grow",
  maintainer_email="alangrow+percentcoding@gmail.com",
  url="https://github.com/acg/python-percentcoding",
  license = "https://github.com/acg/python-percentcoding/blob/master/LICENSE",
  platforms = ["any"],
  description = doclines[0],
  classifiers = filter(None, classifiers.split("\n")),
  long_description = "\n".join(doclines[2:]),
)

