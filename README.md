# percentcoding - fast url encoding and decoding for Python #

Percent encoding is defined for URIs in [RFC 3986](http://tools.ietf.org/html/rfc3986#section-2.1). It is also useful in more general purpose text escaping. Unlike C backslash escaping, which requires that every "unsafe" character be explicitly named (eg. `0x0a` corresponds to `\n`), percent encoding can easily accommodate an arbitrary set of "unsafe" characters.

This library exposes a fast C implementation of percent encoding and decoding to Python. A unit test suite is included.

## Examples ##

As a replacement for `urllib.quote` and `urllib.unquote`:

    from percentcoding import quote, unquote
    str = "This is a test!"
    escaped = quote(str)
    print escaped
    assert(str == unquote(escaped))

Escaping whitespace in whitespace-delimited records:

    import percentcoding
    import string

    ascii = set([chr(c) for c in xrange(255)])
    whitespace = set([c for c in string.whitespace])
    safe = ''.join( ascii - whitespace )
    codec = percentcoding.Codec(safe)

    record = [ "a\nleaf\nfalls", " X\tY\tZ " ]
    print " ".join([ codec.encode(v) for v in record])

## Performance ##

The `percentcoding` library is about 10x faster than the standard `urllib.quote` and `urllib.unquote` implementations. This is not surprising; the standard implementations are pure Python.

    $ ./benchmark.py

    percentcodec.encode x 10000
    0.348151922226

    percentcodec.decode x 10000
    0.381587028503

    urllib.quote x 10000
    4.51035284996

    urllib.unquote x 10000
    3.50923490524

## Notes ##

All ASCII characters *not* occurring in the safe set are considered unsafe.

The `'+'` character does not decode to a space, as is necessary for processing `application/x-www-form-urlencoded`. See the following examples.

To form decode a string `s`:

    quote(s.replace("+"," "))

To form encode a string `s`:

    codec = percentcoding.Codec(URI_SAFE_FORM)
    codec.encode(s.replace(" ","+"))

The `"%%"` character sequence decodes to `'%'`, but is not the canonical encoding.

## Installation ##

Until there's real packaging for your system:

    ./setup.py build_ext --inplace
    ./test.py
    ./setup.py build
    ./setup.py install

