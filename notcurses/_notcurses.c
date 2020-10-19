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
    uint64_t nc_channels;
} NcChannelsObject;

static PyObject *
NcChannels_set_background_rgb(NcChannelsObject *self, PyObject *args)
{
    int red = 0;
    int green = 0;
    int blue = 0;
    if (!PyArg_ParseTuple(args, "iii", &red, &green, &blue))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }
    channels_set_fg_rgb8_clipped(&(self->nc_channels), red, green, blue);
    Py_RETURN_NONE;
}

static PyObject *
NcChannels_set_foreground_rgb(NcChannelsObject *self, PyObject *args)
{
    int red = 0;
    int green = 0;
    int blue = 0;
    if (!PyArg_ParseTuple(args, "iii", &red, &green, &blue))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }
    channels_set_bg_rgb8_clipped(&(self->nc_channels), red, green, blue);
    Py_RETURN_NONE;
}

static PyMethodDef NcChannels_methods[] = {
    {"set_background_color", (PyCFunction)NcChannels_set_background_rgb, METH_VARARGS, "Set background color to RGB"},
    {"set_foreground_color", (PyCFunction)NcChannels_set_foreground_rgb, METH_VARARGS, "Set foreground color to RGB"},
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

static PyObject *
NcPlane_get_dimensions(NcPlaneObject *self, PyObject *args)
{
    int x_dimension = 0;
    int y_dimension = 0;
    ncplane_dim_yx(self->ncplane_ptr, &y_dimension, &x_dimension);

    return PyTuple_Pack(2, PyLong_FromLong(y_dimension), PyLong_FromLong(x_dimension));
}

static PyObject *
NcPlane_set_background_rgb(NcPlaneObject *self, PyObject *args)
{
    int red = 0;
    int green = 0;
    int blue = 0;
    if (!PyArg_ParseTuple(args, "iii", &red, &green, &blue))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }
    ncplane_set_bg_rgb8_clipped(self->ncplane_ptr, red, green, blue);
    Py_RETURN_NONE;
}

static PyObject *
NcPlane_set_foreground_rgb(NcPlaneObject *self, PyObject *args)
{
    int red = 0;
    int green = 0;
    int blue = 0;
    if (!PyArg_ParseTuple(args, "iii", &red, &green, &blue))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse arguments");
        return NULL;
    }
    ncplane_set_fg_rgb8_clipped(self->ncplane_ptr, red, green, blue);
    Py_RETURN_NONE;
}

static PyObject *
NcPlane_put_str(NcPlaneObject *self, PyObject *args, PyObject *kwargs)
{
    static char *keywords[] = {"string", "y_pos", "x_pos", NULL};
    const char *string = "Hello, World!";
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
    {"get_dimensions", (PyCFunction)NcPlane_get_dimensions, METH_NOARGS, "Get plane y,x dimenstions"},
    {"set_background_color", (PyCFunction)NcPlane_set_background_rgb, METH_VARARGS, "Set background color to RGB"},
    {"set_foreground_color", (PyCFunction)NcPlane_set_foreground_rgb, METH_VARARGS, "Set foreground color to RGB"},
    {"putstr", (PyCFunctionWithKeywords)NcPlane_put_str, METH_VARARGS | METH_KEYWORDS, "Put string at y,x"},
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

static void
NotcursesContext_dealloc(NotcursesContextObject *self)
{
    notcurses_stop(self->notcurses_context_ptr);
}

static int
NotcursesContext_init(NotcursesContextObject *self, PyObject *args, PyObject *kwargs)
{
    static char *keywords[] = {"fileno", NULL};
    int file_descriptor = -1;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i", keywords,
                                     &file_descriptor))
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

    FILE *file_to_notcurses = NULL;
    if (file_descriptor > -1)
    {
        file_to_notcurses = fdopen(file_descriptor, "w");
    }

    self->notcurses_context_ptr = notcurses_init(&(self->options), file_to_notcurses);
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
    Py_RETURN_NONE;
}

static PyMethodDef NotcursesContext_methods[] = {
    {"get_std_plane", (PyCFunction)NotcursesContext_get_stdplane, METH_VARARGS, "Get stardard plane of the context"},
    {"render", (PyCFunction)NotcursesContext_render, METH_VARARGS, "Make the physical screen match the virtual screen."},
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
    .tp_init = (initproc)NotcursesContext_init,
    .tp_dealloc = (destructor)NotcursesContext_dealloc,
    .tp_methods = NotcursesContext_methods,
};

typedef struct
{
    PyObject_HEAD;
    struct ncdirect *ncdirect_ptr;
} NcDirectObject;

static void
NcDirect_dealloc(NcDirectObject *self)
{
    ncdirect_stop(self->ncdirect_ptr);
}

static PyObject *
NcDirect_putstr(NcDirectObject *self, PyObject *args)
{
    const char *string = NULL;
    const NcChannelsObject *channels_object = NULL;
    if (!PyArg_ParseTuple(args, "s|O!", &string, &NcChannelsType, &channels_object))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse NcDirect_putstr arguments");
        return NULL;
    }
    uint64_t channels = 0;
    if (channels_object != NULL)
    {
        channels = channels_object->nc_channels;
    }
    int return_code = ncdirect_putstr(self->ncdirect_ptr, channels, string);
    if (return_code >= 0)
    {
        return PyLong_FromLong(return_code);
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to put string on NcDirect");
        return NULL;
    }
}

static PyObject *
NcDirect_disable_cursor(NcDirectObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse NcDirect_disable_cursor arguments");
        return NULL;
    }

    if (!ncdirect_cursor_disable(self->ncdirect_ptr))
    {
        Py_RETURN_NONE;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to disable cursor");
        return NULL;
    }
}

static PyObject *
NcDirect_enable_cursor(NcDirectObject *self, PyObject *args)
{
    if (!PyArg_ParseTuple(args, ""))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse NcDirect_disable_cursor arguments");
        return NULL;
    }

    if (!ncdirect_cursor_enable(self->ncdirect_ptr))
    {
        Py_RETURN_NONE;
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to disable cursor");
        return NULL;
    }
}

static int
NcDirect_init(NcDirectObject *self, PyObject *args, PyObject *kwargs)
{
    static char *keywords[] = {NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", keywords))
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to parse init arguments");
        return -1;
    }
    self->ncdirect_ptr = ncdirect_init(NULL, NULL, 0);
    if (self->ncdirect_ptr == NULL)
    {
        PyErr_SetString(PyExc_RuntimeError, "Failed to initialize NcDirect");
        return -1;
    }
    else
    {
        return 0;
    }
}

static PyMethodDef NcDirect_methods[] = {
    {"putstr", (PyCFunction)NcDirect_putstr, METH_VARARGS, "Put string on the direct plane."},
    {"disable_cursor", (PyCFunction)NcDirect_disable_cursor, METH_VARARGS, "Disable cursor of the direct plane."},
    {"enable_cursor", (PyCFunction)NcDirect_enable_cursor, METH_VARARGS, "Enable cursor of the direct plane."},
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
    .tp_init = (initproc)NcDirect_init,
    .tp_dealloc = (destructor)NcDirect_dealloc,
    .tp_methods = NcDirect_methods,
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