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
#include <notcurses/direct.h>

typedef struct
{
    PyObject_HEAD;
    uint64_t ncchannels_ptr;
} NcChannelsObject;

static PyMethodDef NcChannels_methods[] = {
    {NULL, NULL, 0, NULL},
};

static PyTypeObject NcChannelsType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "notcurses._notcurses._NcChannels",
    .tp_doc = "Notcurses Channels",
    .tp_basicsize = sizeof(NcChannelsObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = NULL,
    .tp_methods = NcChannels_methods,
};

typedef struct
{
    PyObject_HEAD;
    struct ncplane *ncplane_ptr;
} NcPlaneObject;

static PyMethodDef NcPlane_methods[] = {
    {NULL, NULL, 0, NULL},
};

static PyTypeObject NcPlaneType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "notcurses._notcurses._NcPlane",
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

static PyMethodDef NotcursesContext_methods[] = {
    {NULL, NULL, 0, NULL},
};

static PyTypeObject NotcursesContextType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "notcurses._notcurses._NotcursesContext",
    .tp_doc = "Notcurses Context",
    .tp_basicsize = sizeof(NotcursesContextObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_methods = NotcursesContext_methods,
};

typedef struct
{
    PyObject_HEAD;
    struct ncdirect *ncdirect_ptr;
    bool has_been_enabled;
} NcDirectObject;

static void
NcDirect_dealloc(NcDirectObject *self)
{
    if (self->has_been_enabled)
    {
        ncdirect_stop(self->ncdirect_ptr);
    }
}

static PyMethodDef NcDirect_methods[] = {
    {NULL, NULL, 0, NULL},
};

static PyTypeObject NcDirectType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "notcurses._notcurses._NcDirect",
    .tp_doc = "Notcurses Direct",
    .tp_basicsize = sizeof(NcDirectObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor) NcDirect_dealloc,
    .tp_methods = NcDirect_methods,
};

// Functions

/* Prototype

static PyObject *
_ncdirect_init(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    if (!PyArg_ParseTuple(args, "O!", &NcDirectType, &ncdirect_ref))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_init arguments");
        return NULL;
    }
    struct ncdirect *ncdirect_ptr = ncdirect_init(NULL, NULL, 0);
    if (ncdirect_ptr != NULL)
    {
        ncdirect_ref->ncdirect_ptr = ncdirect_ptr;
        Py_RETURN_NONE;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse NcDirect_init arguments");
        return NULL;
    }
}

*/
// NcDirect
static PyObject *
_nc_direct_init(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    if (!PyArg_ParseTuple(args, "O!", &NcDirectType, &ncdirect_ref))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_init arguments");
        return NULL;
    }
    struct ncdirect *ncdirect_ptr = ncdirect_init(NULL, NULL, 0);
    if (ncdirect_ptr != NULL)
    {
        ncdirect_ref->ncdirect_ptr = ncdirect_ptr;
        ncdirect_ref->has_been_enabled = true;
        Py_RETURN_NONE;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcDirectObject");
        return NULL;
    }
}

static PyObject *
_nc_direct_putstr(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    const char *string = NULL;
    const NcChannelsObject *channels_object = NULL;
    if (!PyArg_ParseTuple(args, "O!s|O",
                          &NcDirectType, &ncdirect_ref,
                          &string,
                          &channels_object))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_putstr arguments");
        return NULL;
    }
    uint64_t channels = 0;
    if (PyObject_IsInstance((PyObject *)channels_object, (PyObject *)&NcChannelsType))
    {
        channels = channels_object->ncchannels_ptr;
    }
    else if ((PyObject *)channels_object == (PyObject *)Py_None)
    {
        channels = 0;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Unknown _NcChannels type");
        return NULL;
    }

    int return_code = ncdirect_putstr(ncdirect_ref->ncdirect_ptr, channels, string);
    if (return_code >= 0)
    {
        return PyLong_FromLong(return_code);
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed put string on NcDirect");
        return NULL;
    }
}

static PyObject *
_nc_direct_get_dim_x(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    if (!PyArg_ParseTuple(args, "O!", &NcDirectType, &ncdirect_ref))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_get_dim_x arguments");
        return NULL;
    }
    if (ncdirect_ref != NULL)
    {
        return PyLong_FromLong(ncdirect_dim_x(ncdirect_ref->ncdirect_ptr));
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcDirectObject");
        return NULL;
    }
}

static PyObject *
_nc_direct_get_dim_y(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    if (!PyArg_ParseTuple(args, "O!", &NcDirectType, &ncdirect_ref))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_get_dim_y arguments");
        return NULL;
    }
    if (ncdirect_ref != NULL)
    {
        return PyLong_FromLong(ncdirect_dim_y(ncdirect_ref->ncdirect_ptr));
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcDirectObject");
        return NULL;
    }
}

static PyObject *
_nc_direct_disable_cursor(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    if (!PyArg_ParseTuple(args, "O!", &NcDirectType, &ncdirect_ref))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_disable_cursor arguments");
        return NULL;
    }
    if (ncdirect_ref != NULL)
    {
        ncdirect_cursor_disable(ncdirect_ref->ncdirect_ptr);
        Py_RETURN_NONE;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcDirectObject");
        return NULL;
    }
}

static PyObject *
_nc_direct_enable_cursor(PyObject *self, PyObject *args)
{
    NcDirectObject *ncdirect_ref = NULL;
    if (!PyArg_ParseTuple(args, "O!", &NcDirectType, &ncdirect_ref))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncdirect_enable_cursor arguments");
        return NULL;
    }
    if (ncdirect_ref != NULL)
    {
        ncdirect_cursor_enable(ncdirect_ref->ncdirect_ptr);
        Py_RETURN_NONE;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcDirectObject");
        return NULL;
    }
}
// NcChannels

static PyObject *
_nc_channels_set_background_rgb(PyObject *self, PyObject *args)
{
    NcChannelsObject *nchannels_ref = NULL;
    int red = 0;
    int green = 0;
    int blue = 0;
    if (!PyArg_ParseTuple(args, "O!iii",
                          &NcChannelsType, &nchannels_ref,
                          &red, &green, &blue))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncchannels_set_background_rgb arguments");
        return NULL;
    }

    if (nchannels_ref == NULL)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcChannelsObject");
        return NULL;
    }

    int return_code = channels_set_bg_rgb8(&(nchannels_ref->ncchannels_ptr), red, green, blue);
    if (return_code != 0)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set channel background colors");
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
_nc_channels_set_foreground_rgb(PyObject *self, PyObject *args)
{
    NcChannelsObject *nchannels_ref = NULL;
    int red = 0;
    int green = 0;
    int blue = 0;
    if (!PyArg_ParseTuple(args, "O!iii",
                          &NcChannelsType, &nchannels_ref,
                          &red, &green, &blue))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse _ncchannels_set_foreground_rgb arguments");
        return NULL;
    }

    if (nchannels_ref == NULL)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to acquire NcChannelsObject");
        return NULL;
    }

    int return_code = channels_set_fg_rgb8(&(nchannels_ref->ncchannels_ptr), red, green, blue);
    if (return_code != 0)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set channel foreground colors");
        return NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *
get_notcurses_version_str(PyObject *self, PyObject *args)
{
    const char *verstion_str = notcurses_version();
    return PyUnicode_FromString(verstion_str);
}

// Copy pasta
// {"_ncdirect_init", (PyCFunction)_ncdirect_init, METH_VARARGS, NULL},
static PyMethodDef NotcursesMethods[] = {
    {"_nc_direct_init", (PyCFunction)_nc_direct_init, METH_VARARGS, NULL},
    {"_nc_direct_putstr", (PyCFunction)_nc_direct_putstr, METH_VARARGS, NULL},
    {"_nc_direct_get_dim_x", (PyCFunction)_nc_direct_get_dim_x, METH_VARARGS, NULL},
    {"_nc_direct_get_dim_y", (PyCFunction)_nc_direct_get_dim_y, METH_VARARGS, NULL},
    {"_nc_direct_disable_cursor", (PyCFunction)_nc_direct_disable_cursor, METH_VARARGS, NULL},
    {"_nc_direct_enable_cursor", (PyCFunction)_nc_direct_enable_cursor, METH_VARARGS, NULL},
    {"_nc_channels_set_background_rgb", (PyCFunction)_nc_channels_set_background_rgb, METH_VARARGS, NULL},
    {"_nc_channels_set_foreground_rgb", (PyCFunction)_nc_channels_set_foreground_rgb, METH_VARARGS, NULL},
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
PyInit__notcurses(void)
{
    PyObject *py_module; // create the module
    if (PyType_Ready(&NotcursesContextType) < 0)
        return NULL;

    if (PyType_Ready(&NcPlaneType) < 0)
        return NULL;

    if (PyType_Ready(&NcDirectType) < 0)
        return NULL;

    if (PyType_Ready(&NcChannelsType) < 0)
        return NULL;

    py_module = PyModule_Create(&NotcursesModule);
    if (py_module == NULL)
        return NULL;

    Py_INCREF(&NotcursesContextType);
    if (PyModule_AddObject(py_module, "_NotcursesContext", (PyObject *)&NotcursesContextType) < 0)
    {
        Py_DECREF(&NotcursesContextType);
        Py_DECREF(py_module);
        return NULL;
    }

    Py_INCREF(&NcPlaneType);
    if (PyModule_AddObject(py_module, "_NcPlane", (PyObject *)&NcPlaneType) < 0)
    {
        Py_DECREF(&NcPlaneType);
        Py_DECREF(py_module);
        return NULL;
    }

    Py_INCREF(&NcDirectType);
    if (PyModule_AddObject(py_module, "_NcDirect", (PyObject *)&NcDirectType) < 0)
    {
        Py_DECREF(&NcDirectType);
        Py_DECREF(py_module);
        return NULL;
    }

    Py_INCREF(&NcChannelsType);
    if (PyModule_AddObject(py_module, "_NcChannels", (PyObject *)&NcChannelsType) < 0)
    {
        Py_DECREF(&NcChannelsType);
        Py_DECREF(py_module);
        return NULL;
    }

    return py_module;
}