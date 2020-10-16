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

from ctypes import (CDLL, POINTER, Structure, c_char_p, c_int, c_size_t,
                    c_uint, c_uint8, c_uint16, c_uint32, c_uint64, c_void_p,
                    c_wchar_p, pointer, c_int64)
from ctypes.util import find_library
from typing import Any, Callable, NewType, Optional, Tuple, Type, cast
from enum import IntEnum, auto

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

NCPALETTESIZE = 256


class NcStats(Structure):
    _fields_ = [
        ('renders', c_uint64),
        ('failed_renders', c_uint64),
        ('render_bytes', c_uint64),
        ('render_max_bytes', c_int64),
        ('render_min_bytes', c_int64),
        ('render_ns', c_uint64),
        ('render_max_ns', c_int64),
        ('render_min_ns', c_int64),
        ('writeout_ns', c_uint64),
        ('writeout_max_ns', c_int64),
        ('writeout_min_ns', c_int64),
        ('cellelisions', c_uint64),
        ('cellemissions', c_uint64),
        ('fgelisions', c_uint64),
        ('fgemissions', c_uint64),
        ('bgelisions', c_uint64),
        ('bgemissions', c_uint64),
        ('defaultelisions', c_uint64),
        ('defaultemissions', c_uint64),
    ]


NcStatsPointer = POINTER(NcStats)


class NotcursesOptions(Structure):
    _fields_ = [
        ('termtype', c_char_p),
        ('renderfp', c_int),
        ('loglevel', c_int),
        ('margin_t', c_int),
        ('margin_r', c_int),
        ('margin_b', c_int),
        ('margin_l', c_int),
        ('flags', c_uint64),
    ]


class Palette256(Structure):
    _fields_ = [
        ('chans', c_uint32 * NCPALETTESIZE),
    ]


Palette256Pointer = POINTER(Palette256)
# region NewType


NotcursesContext = NewType('NotcursesContext', c_void_p)
NcPlane = NewType('NcPlane', c_void_p)


# endregion NewType

class NcBlitterEnum(IntEnum):
    NCBLIT_DEFAULT = 0
    NCBLIT_1x1 = auto()
    NCBLIT_2x1 = auto()
    NCBLIT_1x1x4 = auto()
    NCBLIT_2x2 = auto()
    NCBLIT_4x1 = auto()
    NCBLIT_BRAILLE = auto()
    NCBLIT_8x1 = auto()
    NCBLIT_SIXEL = auto()


class NcScaleEnum(IntEnum):
    NCSCALE_NONE = 0
    NCSCALE_SCALE = auto()
    NCSCALE_STRETCH = auto()


class NcLogLevelEnum(IntEnum):
    NCLOGLEVEL_SILENT = 0
    NCLOGLEVEL_PANIC = auto()
    NCLOGLEVEL_FATAL = auto()
    NCLOGLEVEL_ERROR = auto()
    NCLOGLEVEL_WARNING = auto()
    NCLOGLEVEL_INFO = auto()
    NCLOGLEVEL_VERBOSE = auto()
    NCLOGLEVEL_DEBUG = auto()
    NCLOGLEVEL_TRACE = auto()

# endregion Types


# region Functions


ncplane_putc_yx: Callable[
    [NcPlane, int, int, pointer[NotcursesCell]],
    int
] = import_from_cdll(
    func_name='ncplane_putc_yx',
    arg_types_tuple=(c_void_p, c_int, c_int, NotcursesCellPointer),
    return_type=c_int
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

# region notcurses_

# notcurses_getc

notcurses_getc: Callable[
    [NotcursesContext],
    NcPlane
] = import_from_cdll(
    func_name='notcurses_getc',
    arg_types_tuple=(c_void_p, c_void_p,),
    return_type=c_void_p,
)

notcurses_init: Callable[
    [Optional[pointer[NotcursesInitOptions]], int],
    NotcursesContext
] = import_from_cdll(
    func_name='notcurses_init',
    arg_types_tuple=(NotcursesInitOptionsPointer, c_void_p),
    return_type=c_void_p,
)

notcurses_inputready_fd: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_inputready_fd',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_lex_blitter: Callable[
    [bytes, NcScaleEnum],
    int
] = import_from_cdll(
    func_name='notcurses_lex_blitter',
    arg_types_tuple=(c_char_p, c_int),
    return_type=c_int,
)


notcurses_lex_margins: Callable[
    [bytes, pointer[NotcursesOptions]],
    int
] = import_from_cdll(
    func_name='notcurses_lex_margins',
    arg_types_tuple=(c_char_p, c_void_p),
    return_type=c_int,
)


notcurses_lex_scalemode: Callable[
    [bytes, NcScaleEnum],
    int
] = import_from_cdll(
    func_name='notcurses_lex_scalemode',
    arg_types_tuple=(c_char_p, c_int),
    return_type=c_int,
)

notcurses_mouse_disable: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_mouse_disable',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_mouse_enable: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_mouse_enable',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_palette_size: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_palette_size',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_refresh: Callable[
    [NotcursesContext, pointer[c_int], pointer[c_int]],
    int
] = import_from_cdll(
    func_name='notcurses_refresh',
    arg_types_tuple=(c_void_p, c_void_p, c_void_p),
    return_type=c_int
)

notcurses_render: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_render',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int
)

notcurses_render_to_buffer: Callable[
    [NotcursesContext, pointer[c_char_p], pointer[c_size_t]],
    int
] = import_from_cdll(
    func_name='notcurses_render_to_buffer',
    arg_types_tuple=(c_void_p, c_void_p, c_void_p),
    return_type=c_int,
)

notcurses_render_to_file: Callable[
    [NotcursesContext, int],
    int
] = import_from_cdll(
    func_name='notcurses_render_to_file',
    arg_types_tuple=(c_void_p, c_int),
    return_type=c_int,
)

notcurses_stats: Callable[
    [NotcursesContext, pointer[NcStats]],
    None
] = import_from_cdll(
    func_name='notcurses_stats',
    arg_types_tuple=(c_void_p, c_void_p),
)

notcurses_stats_alloc: Callable[
    [NotcursesContext],
    pointer[NcStats]
] = import_from_cdll(
    func_name='notcurses_stats_alloc',
    arg_types_tuple=(c_void_p, ),
    return_type=c_void_p,
)

notcurses_stats_reset: Callable[
    [NotcursesContext, pointer[NcStats]],
    None
] = import_from_cdll(
    func_name='notcurses_stats_reset',
    arg_types_tuple=(c_void_p, c_void_p),
)

notcurses_stdplane: Callable[
    [NotcursesContext],
    NcPlane
] = import_from_cdll(
    func_name='notcurses_stdplane',
    arg_types_tuple=(c_void_p, ),
    return_type=c_void_p,
)

# notcurses_stdplane_const not ported as it is redundant

notcurses_stop: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_stop',
    arg_types_tuple=(c_void_p, ),
    return_type=c_int,
)

notcurses_str_blitter: Callable[
    [NcBlitterEnum],
    bytes
] = import_from_cdll(
    func_name='notcurses_str_blitter',
    arg_types_tuple=(c_int, ),
    return_type=c_char_p,
)

notcurses_str_scalemode: Callable[
    [NcScaleEnum],
    bytes
] = import_from_cdll(
    func_name='notcurses_str_scalemode',
    arg_types_tuple=(c_int, ),
    return_type=c_char_p,
)

notcurses_supported_styles: Callable[
    [NotcursesContext],
    int
] = import_from_cdll(
    func_name='notcurses_supported_styles',
    arg_types_tuple=(c_void_p, ),
    return_type=c_uint,
)

notcurses_top: Callable[
    [NotcursesContext],
    NcPlane
] = import_from_cdll(
    func_name='notcurses_top',
    arg_types_tuple=(c_void_p, ),
    return_type=c_void_p,
)

notcurses_ucs32_to_utf8: Callable[
    [c_wchar_p, int, c_char_p, int],
    int
] = import_from_cdll(
    func_name='notcurses_ucs32_to_utf8',
    arg_types_tuple=(c_wchar_p, c_uint, c_char_p, c_size_t),
    return_type=c_int,
)

notcurses_version: Callable[
    [],
    bytes
] = import_from_cdll(
    func_name='notcurses_version',
    arg_types_tuple=(),
    return_type=c_char_p,
)

notcurses_version_components: Callable[
    [pointer[c_int], pointer[c_int], pointer[c_int], pointer[c_int]],
    None
] = import_from_cdll(
    func_name='notcurses_version_components',
    arg_types_tuple=(c_void_p, c_void_p, c_void_p, c_void_p),
)

# endregion notcurses_

# region palette256

palette256_free: Callable[
    [pointer[Palette256]],
    None
] = import_from_cdll(
    func_name='palette256_free',
    arg_types_tuple=(c_void_p, ),
)

palette256_new: Callable[
    [NotcursesContext],
    pointer[Palette256]
] = import_from_cdll(
    func_name='palette256_new',
    arg_types_tuple=(c_void_p, ),
    return_type=Palette256Pointer,
)

palette256_use: Callable[
    [NotcursesContext, pointer[Palette256]],
    int
] = import_from_cdll(
    func_name='palette256_use',
    arg_types_tuple=(c_void_p, Palette256Pointer),
    return_type=c_int,
)

# endregion palette256

# endregion Functions
