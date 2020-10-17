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
    struct ncplane *ncplane_ptr;
} NcPlaneObject;

static PyObject *
ncplane_put_str(NcPlaneObject *self, PyObject *args, PyObject *kwargs)
{
    static char *keywords[] = {"string", "y_pos", "x_pos", NULL};
    char *string = "Hello, World!";
    int y_pos = -1;
    int x_pos = -1;
    if (self->ncplane_ptr == NULL)
    {
        PyErr_SetString(PyExc_RuntimeError, "NcPlane not attached. Did you try to initialize it directly?");
        return NULL;
    }

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,
                                     "s|ii", keywords,
                                     &string, &y_pos, &x_pos))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }

    int return_code = ncplane_putstr_yx(self->ncplane_ptr, y_pos, x_pos, string);
    if (return_code < 0)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to put string on plane");
        return NULL;
    }
    else
    {
        return PyLong_FromLong(return_code);
    }
}

static PyMethodDef NcPlane_methods[] = {
    {"putstr", (PyCFunctionWithKeywords)ncplane_put_str, METH_VARARGS | METH_KEYWORDS, "Put string at y,x"},
    {NULL, NULL, 0, NULL},
};

static PyTypeObject NcPlaneType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "notcurses.notcurses_context.NcPlane",
    .tp_doc = "Notcurses Plane",
    .tp_basicsize = sizeof(NcPlaneObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = NULL,
    .tp_methods = NcPlane_methods,
};

typedef struct
{
    PyObject_HEAD;
    struct notcurses_options options;
    struct notcurses *notcurses_context_ptr;
} NotcursesContextObject;

static void
NotcursesContext_dealloc(NotcursesContextObject *self)
{
    notcurses_stop(self->notcurses_context_ptr);
}

static int
NotcursesContext_init(NotcursesContextObject *self, PyObject *args, PyObject *kwargs)
{
    static char *keywords[] = {NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", keywords))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse init arguments");
        return -1;
    }
    self->options = (notcurses_options){
        .termtype = NULL,
        .renderfp = NULL,
        .loglevel = NCLOGLEVEL_DEBUG,
        .margin_t = 0,
        .margin_r = 0,
        .margin_b = 0,
        .margin_l = 0,
    };
    self->notcurses_context_ptr = notcurses_init(&(self->options), NULL);
    if (self->notcurses_context_ptr != NULL)
    {
        return 0;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to initialize Notcurses");
        return -1;
    }
}

static NcPlaneObject *
NotcursesContext_get_stdplane(NotcursesContextObject *self, PyObject *Py_UNUSED(ignored))
{
    NcPlaneObject *ncplane_object = PyObject_New(NcPlaneObject, &NcPlaneType);
    if (ncplane_object == NULL)
        return NULL;
    ncplane_object->ncplane_ptr = notcurses_top(self->notcurses_context_ptr);
    return ncplane_object;
}

static PyObject *
NotcursesContext_render(NotcursesContextObject *self, PyObject *Py_UNUSED(ignored))
{
    notcurses_render(self->notcurses_context_ptr);
    return Py_None;
}

static PyMethodDef NotcursesContext_methods[] = {
    {"get_std_plane", (PyCFunction)NotcursesContext_get_stdplane, METH_VARARGS, "Get stardard plane of the context"},
    {"render", (PyCFunction)NotcursesContext_render, METH_VARARGS, "Make the physical screen match the virtual screen."},
    {NULL, NULL, 0, NULL},
};

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
    .tp_methods = NotcursesContext_methods,
};

static PyObject *
get_notcurses_version_str(PyObject *self, PyObject *args)
{
    const char *verstion_str = notcurses_version();
    return PyUnicode_FromString(verstion_str);
}

static PyMethodDef NotcursesMethods[] = {
    {"get_notcurses_version", (PyCFunction)get_notcurses_version_str, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef NotcursesModule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "Notcurses", /* name of module */
    .m_doc = "Notcurses.", /* module documentation, may be NULL */
    .m_size = -1,          /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    NotcursesMethods,
};

PyMODINIT_FUNC
PyInit_notcurses_context(void)
{
    PyObject *py_module; // create the module
    if (PyType_Ready(&NotcursesContextType) < 0)
        return NULL;

    if (PyType_Ready(&NcPlaneType) < 0)
        return NULL;

    py_module = PyModule_Create(&NotcursesModule);
    if (py_module == NULL)
        return NULL;

    Py_INCREF(&NotcursesContextType);
    if (PyModule_AddObject(py_module, "NotcursesContext", (PyObject *)&NotcursesContextType) < 0)
    {
        Py_DECREF(&NotcursesContextType);
        Py_DECREF(py_module);
        return NULL;
    }

    Py_INCREF(&NcPlaneType);
    if (PyModule_AddObject(py_module, "NcPlane", (PyObject *)&NcPlaneType) < 0)
    {
        Py_DECREF(&NcPlaneType);
        Py_DECREF(py_module);
        return NULL;
    }

    return py_module;
}