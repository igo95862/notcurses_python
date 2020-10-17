// SPDX-License-Identifier: Apache-2.0
/*
Copyright 2020 igo95862

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <notcurses/notcurses.h>

typedef struct
{
    PyObject_HEAD;
    struct notcurses *notcurses_context_ptr;
} NotcursesContextObject;

static PyObject *
NotcursesContext_dealloc(NotcursesContextObject *self)
{
    if (!notcurses_stop(self->notcurses_context_ptr))
        return NULL;
}

static PyObject *
NotcursesContext_init(NotcursesContextObject *self, PyObject *args, PyObject *kwds)
{
    static char *keywords[] = {NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "", keywords))
        return -1;
    self->notcurses_context_ptr = notcurses_init(NULL, NULL);
}

static PyTypeObject NotcursesContextType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "notcurses.notcurses_context.NotcursesContext",
    .tp_doc = "Notcurses Context",
    .tp_basicsize = sizeof(NotcursesContextObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)NotcursesContext_init,
    .tp_dealloc = (destructor)NotcursesContext_dealloc,
};

static PyObject *
get_notcurses_version_str(PyObject *self, PyObject *args)
{
    const char *verstion_str = notcurses_version();
    return PyUnicode_FromString(verstion_str);
}

static PyMethodDef NotcursesContextMethods[] = {
    {"get_notcurses_version", (PyCFunction)get_notcurses_version_str, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef NotcursesContextModule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "NotcursesContext",  /* name of module */
    .m_doc = "Notcurses Context.", /* module documentation, may be NULL */
    .m_size = -1,                  /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    NotcursesContextMethods,
};

PyMODINIT_FUNC
PyInit_notcurses_context(void)
{
    PyObject *py_module; // create the module
    if (PyType_Ready(&NotcursesContextType) < 0)
        return NULL;

    py_module = PyModule_Create(&NotcursesContextModule);
    if (py_module == NULL)
        return NULL;

    Py_INCREF(&NotcursesContextType);
    if (PyModule_AddObject(py_module, "NotcursesContext", (PyObject *)&NotcursesContextType) < 0)
    {
        Py_DECREF(&NotcursesContextType);
        Py_DECREF(py_module);
        return NULL;
    }

    return py_module;
}