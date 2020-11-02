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

from typing import Optional, Tuple


class _NcChannels:
    ...


class _NcPlane:
    ...


class _NotcursesContext:
    ...


class _NcDirect:
    ...


class _NcInput:
    @property
    def codepoint(self) -> int:
        ...

    @property
    def y_pos(self) -> int:
        ...

    @property
    def x_pos(self) -> int:
        ...

    @property
    def is_alt(self) -> bool:
        ...

    @property
    def is_shift(self) -> bool:
        ...

    @property
    def is_ctrl(self) -> bool:
        ...

    @property
    def seqnum(self) -> int:
        ...


def _nc_direct_init(ncdirect: _NcDirect, /) -> None:
    ...


def _nc_direct_stop(ncdirect: _NcDirect, /) -> None:
    ...


def _nc_direct_putstr(nc_direct: _NcDirect,
                      string: str,
                      nc_channels: Optional[_NcChannels], /) -> int:
    ...


def _nc_direct_get_dim_x(nc_direct: _NcDirect, /) -> int:
    ...


def _nc_direct_get_dim_y(nc_direct: _NcDirect, /) -> int:
    ...


def _nc_direct_disable_cursor(nc_direct: _NcDirect, /) -> None:
    ...


def _nc_direct_enable_cursor(nc_direct: _NcDirect, /) -> None:
    ...


def _nc_channels_set_background_rgb(
        nc_channels: _NcChannels,
        red: int, green: int, blue: int, /) -> None:
    ...


def _nc_channels_set_foreground_rgb(
        nc_channels: _NcChannels,
        red: int, green: int, blue: int, /) -> None:
    ...


def _notcurses_context_init(nc_context: _NotcursesContext, /) -> None:
    ...


def _notcurses_context_stop(nc_context: _NotcursesContext, /) -> None:
    ...


def _notcurses_context_render(nc_context: _NotcursesContext, /) -> None:
    ...


def _notcurses_context_mouse_disable(nc_context: _NotcursesContext, /) -> None:
    ...


def _notcurses_context_mouse_enable(nc_context: _NotcursesContext, /) -> None:
    ...


def _notcurses_context_cursor_disable(
        nc_context: _NotcursesContext, /) -> None:
    ...


def _notcurses_context_cursor_enable(
        nc_context: _NotcursesContext,
        y_pos: int, x_pos: int, /) -> None:
    ...


def _notcurses_context_get_std_plane(
        nc_context: _NotcursesContext, /) -> _NcPlane:
    ...


def _notcurses_context_get_input_blocking(
        nc_context: _NotcursesContext, /) -> _NcInput:
    ...


def _nc_plane_set_background_rgb(
        nc_plane: _NcPlane,
        red: int, green: int, blue: int, /) -> None:
    ...


def _nc_plane_set_foreground_rgb(
        nc_plane: _NcPlane,
        red: int, green: int, blue: int, /) -> None:
    ...


def _nc_plane_putstr(
        nc_plane: _NcPlane, string: str,
        y_pos: int, x_pos: int, /) -> int:
    ...


def _nc_plane_putstr_alligned(
        nc_plane: _NcPlane, string: str,
        y_pos: int, allign: int, /) -> int:
    ...


def _nc_plane_dimensions_yx(nc_plane: _NcPlane, /) -> Tuple[int, int]:
    ...


def _nc_plane_polyfill_yx(
        nc_plane: _NcPlane,
        y_pos: int, x_pos: int, cell_str: str, /) -> int:
    ...


def _nc_plane_erase(nc_plane: _NcPlane, /) -> None:
    ...


def _nc_plane_create(
        nc_plane: _NcPlane,
        y_pos: int, x_pos: int,
        rows_num: int, cols_num: int, /) -> _NcPlane:
    ...


def get_notcurses_version() -> str:
    """Returns notcurses version from library"""
    ...


NCKEY_INVALID: int
NCKEY_UP: int
NCKEY_RESIZE: int
NCKEY_RIGHT: int
NCKEY_DOWN: int
NCKEY_LEFT: int
NCKEY_INS: int
NCKEY_DEL: int
NCKEY_BACKSPACE: int
NCKEY_PGDOWN: int
NCKEY_PGUP: int
NCKEY_HOME: int
NCKEY_END: int
NCKEY_F00: int
NCKEY_F01: int
NCKEY_F02: int
NCKEY_F03: int
NCKEY_F04: int
NCKEY_F05: int
NCKEY_F06: int
NCKEY_F07: int
NCKEY_F08: int
NCKEY_F09: int
NCKEY_F10: int
NCKEY_F11: int
NCKEY_F12: int
NCKEY_ENTER: int
NCKEY_CLS: int
NCKEY_DLEFT: int
NCKEY_DRIGHT: int
NCKEY_ULEFT: int
NCKEY_URIGHT: int
NCKEY_CENTER: int
NCKEY_BEGIN: int
NCKEY_CANCEL: int
NCKEY_CLOSE: int
NCKEY_COMMAND: int
NCKEY_COPY: int
NCKEY_EXIT: int
NCKEY_PRINT: int
NCKEY_REFRESH: int
NCKEY_BUTTON1: int
NCKEY_BUTTON2: int
NCKEY_BUTTON3: int
NCKEY_SCROLL_UP: int
NCKEY_SCROLL_DOWN: int
NCKEY_BUTTON6: int
NCKEY_RELEASE: int

NCALIGN_UNALIGNED: int
NCALIGN_LEFT: int
NCALIGN_CENTER: int
NCALIGN_RIGHT: int

NCSCALE_NONE: int
NCSCALE_SCALE: int
NCSCALE_STRETCH: int
