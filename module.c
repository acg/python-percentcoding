#include "Python.h"
#include "codec.h"

/* List of functions defined in the module */

static PyMethodDef percentcoding_methods[] = {
  {NULL,    NULL}    /* sentinel */
};

PyDoc_STRVAR(module_doc, "Fast percent encoding and decoding (AKA \"url encoding\").");

/* Initialization function for the module (*must* be called initcext) */

PyMODINIT_FUNC
initcext(void)
{
  /* Make sure exposed types are subclassable. */

  CodecType.tp_base = &PyBaseObject_Type;

  /* Finalize the type object including setting type of the new type
   * object; doing it here is required for portability, too. */

  if (PyType_Ready(&CodecType) < 0)
    return;

  /* Create the module and add the functions */

  PyObject* mod = Py_InitModule3("percentcoding.cext", percentcoding_methods, module_doc);
  if (mod == NULL)
    return;

  Py_INCREF(&CodecType);
  PyModule_AddObject(mod, "Codec", (PyObject*)&CodecType);
}

