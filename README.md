# percentcoding - fast url encoding and decoding #

Percent encoding is a generalization of the text escaping method defined for URIs in [RFC 3986](http://tools.ietf.org/html/rfc3986#section-2.1). Unlike C backslash escaping, which requires that every reserved character be explicitly named (eg. 0x0a corresponds to \n), percent encoding can easily accommodate an arbitrary set of reserved characters.

For the specific case of URI escaping, the percentcoding library also provides a 10x faster drop-in replacement for the `urllib.quote`, `urllib.unquote`, `urllib.quote_plus`, and `urllib.unquote_plus` functions. A unit test suite is included.

## Examples ##

As a faster replacement for `urllib.quote` and `urllib.unquote`:

    #!/usr/bin/env python
    from percentcoding import quote, unquote
    str = "This is a test!"
    escaped = quote(str)
    print escaped
    assert(str == unquote(escaped))

Escaping whitespace in whitespace-delimited records:

    #!/usr/bin/env python
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

(TODO: move into pydoc)

All ASCII characters *not* occurring in the safe set are considered unsafe and will be escaped by `encode`.

With `quote` and `unquote`, the `'+'` character does not map to a space, as is necessary for processing `application/x-www-form-urlencoded`. Like `urllib`, `percentcoding` exports `quote_plus` and `unquote_plus` for that.

The `"%%"` character sequence decodes to `'%'`, but is not the canonical encoding.

When decoding, if an invalid hex sequence is encountered (eg `"%az"`), it is copied as-is.

Per the spec, Unicode and UTF-8 strings are encoded byte-wise, resulting in an ASCII string. When decoding, the result is also an ASCII string, which if originally Unicode can be recovered using the Python string method `decode`:

    unquote(s).decode('utf8')

## Installation ##

Ubuntu / Debian users:

    fakeroot ./debian/rules binary
    dpkg -i ../python-percentcoding*.deb

If there's no "real" packaging for your system yet:

    ./setup.py build_ext --inplace
    ./test.py
    ./setup.py build
    ./setup.py install

