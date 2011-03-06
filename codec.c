#include "codec.h"
#include "Python.h"
#include "percentcoding.h"


/* Codec methods */

static PyObject *
Codec_new(PyTypeObject *type, PyObject *arg, PyObject *kwds)
{
  Codec *self;
  
  if (!(self = (Codec*)type->tp_alloc(type, 0)))
    return NULL;

  return (PyObject *)self;
}


static int
Codec_init(Codec *self, PyObject *args, PyObject *kwds)
{
  const char* safeset = NULL;
  int len = 0;

  if (!PyArg_ParseTuple(args, "s#:init", &safeset, &len))
    return -1;

  /* Initialize the byte -> 2 hex char lookup table.
     By default, everything is "unsafe" and gets percent encoded.
     Anything in safeset is okay.
     The percent character itself is never safe. */
  
  unsigned int i;
  for (i=0; i<256; i++)
    btox((uint8_t)i, &self->chrtohex[(uint8_t)i*2]);

  const uint8_t* p;
  for (i=0, p=(uint8_t*)safeset; i<len; i++, p++)
    if (*p != '%')
      self->chrtohex[*p*2] = self->chrtohex[*p*2+1] = 0;

  return 0;
}


static PyObject *
Codec_encode(Codec *self, PyObject *args)
{
  const char* in = NULL;
  int inlen = 0;

  if (!PyArg_ParseTuple(args, "s#:encode", &in, &inlen))
    return NULL;

  char* out = NULL;
  PyObject *result = NULL;
  Py_ssize_t size;

  /* First pass: calculate size of encoded string.
     Create a new string object of exactly that size. */

  size = percent_encode(in, inlen, NULL, self->chrtohex);

  if (!(result = PyString_FromStringAndSize(NULL,size)))
    return NULL;

  /* Second pass: actually encode this time. */

  out = PyString_AsString(result);
  size = percent_encode(in, inlen, out, self->chrtohex);

  return result;
}


static PyObject *
Codec_decode(Codec *self, PyObject *args)
{
  const char* in = NULL;
  int inlen = 0;

  if (!PyArg_ParseTuple(args, "s#:decode", &in, &inlen))
    return NULL;

  char* out = NULL;
  PyObject *result = NULL;
  Py_ssize_t size;

  /* First pass: calculate size of decoded string.
     Create a new string object of exactly that size. */

  size = percent_decode(in, inlen, NULL);

  if (!(result = PyString_FromStringAndSize(NULL,size)))
    return NULL;

  /* Second pass: actually decode this time. */

  out = PyString_AsString(result);
  size = percent_decode(in, inlen, out);

  return result;
}


static PyMethodDef Codec_methods[] = {
  {"encode",  (PyCFunction)Codec_encode,  METH_VARARGS,
    PyDoc_STR("encode(str) -> str")},
  {"decode",  (PyCFunction)Codec_decode,  METH_VARARGS,
    PyDoc_STR("decode(str) -> str")},
  {NULL,    NULL}    /* sentinel */
};


PyTypeObject CodecType = {
  /* The ob_type field must be initialized in the module init function
   * to be portable to Windows without using C++. */
  PyObject_HEAD_INIT(NULL)
  0,                            /*ob_size*/
  "percentcoding.cext.Codec",   /*tp_name*/
  sizeof(Codec),                /*tp_basicsize*/
  0,                            /*tp_itemsize*/
  /* methods */
  0,                            /*tp_dealloc*/
  0,                            /*tp_print*/
  0,                            /*tp_getattr*/
  0,                            /*tp_setattr*/
  0,                            /*tp_compare*/
  0,                            /*tp_repr*/
  0,                            /*tp_as_number*/
  0,                            /*tp_as_sequence*/
  0,                            /*tp_as_mapping*/
  0,                            /*tp_hash*/
  0,                            /*tp_call*/
  0,                            /*tp_str*/
  0,                            /*tp_getattro */
  0,                            /*tp_setattro*/
  0,                            /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
  0,                            /*tp_doc*/
  0,                            /*tp_traverse*/
  0,                            /*tp_clear*/
  0,                            /*tp_richcompare*/
  0,                            /*tp_weaklistoffset*/
  0,                            /*tp_iter*/
  0,                            /*tp_iternext*/
  Codec_methods,                /*tp_methods*/
  0,                            /*tp_members*/
  0,                            /*tp_getset*/
  0,                            /*tp_base*/
  0,                            /*tp_dict*/
  0,                            /*tp_descr_get*/
  0,                            /*tp_descr_set*/
  0,                            /*tp_dictoffset*/
  (initproc)Codec_init,         /*tp_init*/
  0,                            /*tp_alloc*/
  Codec_new,                    /*tp_new*/
  0,                            /*tp_free*/
  0,                            /*tp_is_gc*/
};

