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

static struct PyModuleDef notcurses_context_module = {
    PyModuleDef_HEAD_INIT,
    "notcurses_context", /* name of module */
    NULL,                /* module documentation, may be NULL */
    -1,                  /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    NotcursesContextMethods,
};

PyMODINIT_FUNC
PyInit_notcurses_context(void)
{
    return PyModule_Create(&notcurses_context_module);
}