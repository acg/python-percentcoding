#!/usr/bin/env python

from distutils.core import setup, Extension, Command


setup(
  name='percentcoding',
  version='0.1',
  ext_modules=[
    Extension(
      'percentcoding.cext',
      [
        'codec.c',
        'module.c',
      ],
      extra_compile_args=['-fPIC'],
      define_macros=[],
    ),
  ],
  packages=['percentcoding'],
)

