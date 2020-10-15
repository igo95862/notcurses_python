# SPDX-License-Identifier: Apache-2.0

# Copyright 2020 igo95862

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from ctypes import (CDLL, POINTER, Structure, c_char_p, c_int, c_uint8,
                    c_uint16, c_uint32, c_uint64, c_void_p, pointer)
from ctypes.util import find_library
from typing import Any, Callable, NewType, Optional, Tuple, Type, cast

libnotcurses = CDLL(find_library('notcurses'))

# region Typing helper functions


def import_from_cdll(
    func_name: str,
    arg_types_tuple: Tuple[Type[Any], ...],
    return_type: Optional[Type[Any]] = None,
) -> Callable[..., Any]:
    c_function = getattr(libnotcurses, func_name)
    c_function.argtypes = arg_types_tuple
    c_function.restype = return_type
    return cast(Callable[..., Any], c_function)


# endregion Typing helper functions

# region Types


class NotcursesInitOptions(Structure):
    _fields_ = [
        ('termtype', c_char_p),
        ('renderfp', c_void_p),
        ('ncloglevel_e', c_int),
        ('margin_t', c_int),
        ('margin_r', c_int),
        ('margin_b', c_int),
        ('margin_l', c_int),
        ('flags', c_uint64),
    ]


NotcursesInitOptionsPointer = POINTER(NotcursesInitOptions)


class NotcursesCell(Structure):
    _fields_ = [
        ('gcluster', c_uint32),
        ('gcluster_backstop', c_uint8),
        ('reserved', c_uint8),
        ('stylemask', c_uint16),
        ('channels', c_uint64),
    ]


NotcursesCellPointer = POINTER(NotcursesCell)
# region NewType


NotcursesContext = NewType('NotcursesContext', c_void_p)
NcPlane = NewType('NcPlane', c_void_p)


# endregion NewType

# endregion Types


# region Functions

notcurses_init: Callable[
    [Optional[pointer[NotcursesInitOptions]], int],
    NotcursesContext
] = import_from_cdll(
    func_name='notcurses_init',
    arg_types_tuple=(NotcursesInitOptionsPointer, c_int),
    return_type=c_void_p,
)

notcurses_render: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_render',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int
)

notcurses_top: Callable[
    [NotcursesContext],
    NcPlane
] = import_from_cdll(
    func_name='notcurses_top',
    arg_types_tuple=(c_void_p, ),
    return_type=c_void_p,
)

ncplane_putc_yx: Callable[
    [NcPlane, int, int, pointer[NotcursesCell]],
    int
] = import_from_cdll(
    func_name='ncplane_putc_yx',
    arg_types_tuple=(c_void_p, c_int, c_int, NotcursesCellPointer),
    return_type=c_int
)

notcurses_mouse_disable: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_mouse_disable',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_stop: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_stop',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_version = import_from_cdll(
    func_name='notcurses_version',
    arg_types_tuple=(),
    return_type=c_char_p,
)

ncplane_set_bg_rgb8_clipped: Callable[
    [NcPlane, int, int, int],
    None
] = import_from_cdll(
    func_name='ncplane_set_bg_rgb8_clipped',
    arg_types_tuple=(c_void_p, c_int, c_int, c_int),
)

ncplane_set_fg_rgb8_clipped: Callable[
    [NcPlane, int, int, int],
    None
] = import_from_cdll(
    func_name='ncplane_set_fg_rgb8_clipped',
    arg_types_tuple=(c_void_p, c_int, c_int, c_int),
)

ncplane_set_fg_rgb8: Callable[
    [NcPlane, int, int, int],
    None
] = import_from_cdll(
    func_name='ncplane_set_fg_rgb8',
    arg_types_tuple=(c_void_p, c_int, c_int, c_int),
    return_type=c_int,
)

ncplane_channels: Callable[
    [NcPlane],
    int
] = import_from_cdll(
    func_name='ncplane_channels',
    arg_types_tuple=(c_void_p, ),
    return_type=c_uint64,
)
# endregion Functions
