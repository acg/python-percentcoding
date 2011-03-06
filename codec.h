#ifndef __PERCENTCODING_CODEC_H__
#define __PERCENTCODING_CODEC_H__

#include "Python.h"

/* Python percentcoding.cext.Codec class */

typedef struct {
  PyObject_HEAD
  char chrtohex[256*2];
} Codec;

extern PyTypeObject CodecType;

#define Codec_Check(v)  (Py_TYPE(v) == &CodecType)

#endif
