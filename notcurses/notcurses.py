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

from typing import Dict, Optional, Tuple

from . import _notcurses
from ._notcurses import (_nc_channels_set_background_rgb,
                         _nc_channels_set_foreground_rgb,
                         _nc_direct_disable_cursor, _nc_direct_enable_cursor,
                         _nc_direct_get_dim_x, _nc_direct_get_dim_y,
                         _nc_direct_init, _nc_direct_putstr, _nc_direct_stop,
                         _nc_plane_create, _nc_plane_dimensions_yx,
                         _nc_plane_erase, _nc_plane_putstr,
                         _nc_plane_set_background_rgb,
                         _nc_plane_set_foreground_rgb, _NcChannels, _NcDirect,
                         _NcInput, _NcPlane, _notcurses_context_cursor_disable,
                         _notcurses_context_cursor_enable,
                         _notcurses_context_get_input_blocking,
                         _notcurses_context_get_std_plane,
                         _notcurses_context_init,
                         _notcurses_context_mouse_disable,
                         _notcurses_context_mouse_enable,
                         _notcurses_context_render, _notcurses_context_stop,
                         _NotcursesContext)


class NotcursesContext:
    def __init__(self,
                 start_immideatly: bool = True):
        self._nc_context = _NotcursesContext()
        self._has_started = False
        if start_immideatly:
            self.start()

    def render(self) -> None:
        _notcurses_context_render(self._nc_context)

    def start(self) -> None:
        _notcurses_context_init(self._nc_context)
        self._has_started = True

    def stop(self) -> None:
        _notcurses_context_stop(self._nc_context)
        self._has_started = False

    def get_input_blocking(self) -> NcInput:
        return NcInput(
            _notcurses_context_get_input_blocking(self._nc_context)
        )

    def enable_mouse(self) -> None:
        _notcurses_context_mouse_enable(self._nc_context)

    def disable_mouse(self) -> None:
        _notcurses_context_mouse_disable(self._nc_context)

    def enable_cursor(self) -> None:
        _notcurses_context_cursor_enable(self._nc_context, 0, 0)

    def disable_cursor(self) -> None:
        _notcurses_context_cursor_disable(self._nc_context)

    def __del__(self) -> None:
        if self._has_started:
            self.stop()


class NcInput:
    def __init__(self, nc_input: _NcInput):
        self._nc_input = nc_input

    @property
    def code(self) -> str:
        try:
            return NC_INPUT_CODES[self._nc_input.codepoint]
        except KeyError:
            return chr(self._nc_input.codepoint)

    @property
    def y_pos(self) -> int:
        return self._nc_input.y_pos

    @property
    def x_pos(self) -> int:
        return self._nc_input.x_pos

    @property
    def is_alt(self) -> bool:
        return self._nc_input.is_alt

    @property
    def is_shift(self) -> bool:
        return self._nc_input.is_shift

    @property
    def is_ctrl(self) -> bool:
        return self._nc_input.is_ctrl

    @property
    def seqnum(self) -> int:
        return self._nc_input.seqnum


class NcPlane:
    def __init__(self, plane: _NcPlane, context: NotcursesContext) -> None:
        self._nc_plane = plane
        self.context = context

    @property
    def dimensions_yx(self) -> Tuple[int, int]:
        return _nc_plane_dimensions_yx(self._nc_plane)

    def putstr(
            self,
            string: str,
            y_pos: int = -1, x_pos: int = -1) -> None:
        _nc_plane_putstr(
            self._nc_plane,
            string,
            y_pos,
            x_pos,
        )

    def erase(self) -> None:
        return _nc_plane_erase(self._nc_plane)

    def set_background_rgb(
            self, red: int, green: int, blue: int) -> None:
        _nc_plane_set_background_rgb(self._nc_plane, red, green, blue)

    def set_foreground_rgb(
            self, red: int, green: int, blue: int) -> None:
        _nc_plane_set_foreground_rgb(self._nc_plane, red, green, blue)

    def create_sub_plane(
        self,
        y_pos: int = 0,
        x_pos: int = 0,
        rows_num: Optional[int] = None,
        cols_num: Optional[int] = None
    ) -> NcPlane:

        if cols_num is None:
            y_dim, _ = self.dimensions_yx
            cols_num = y_dim // 2

        if rows_num is None:
            _, x_dim = self.dimensions_yx
            rows_num = x_dim

        new_plane = _nc_plane_create(
            self._nc_plane,
            y_pos, x_pos, rows_num, cols_num
        )

        return NcPlane(new_plane, self.context)


_default_context: Optional[NotcursesContext] = None


def get_std_plane() -> NcPlane:
    global _default_context
    if _default_context is None:
        _default_context = NotcursesContext()

    std_plane_ref = _notcurses_context_get_std_plane(
        _default_context._nc_context)
    return NcPlane(std_plane_ref, _default_context)


class NcChannels:
    def __init__(self) -> None:
        self._nc_channels = _NcChannels()

    def set_background_rgb(self, red: int, green: int, blue: int) -> None:
        _nc_channels_set_background_rgb(
            self._nc_channels,
            red, green, blue,
        )

    def set_foreground_rgb(self, red: int, green: int, blue: int) -> None:
        _nc_channels_set_foreground_rgb(
            self._nc_channels,
            red, green, blue,
        )


class NcDirect:
    def __init__(self,
                 start_immideatly: bool = True):
        self._nc_direct = _NcDirect()
        self._is_cursor_enabled: Optional[bool] = None
        self._has_started = False
        if start_immideatly:
            self.start()

    def __del__(self) -> None:
        if self._has_started:
            self.stop()

    def start(self) -> None:
        _nc_direct_init(self._nc_direct)
        self._has_started = True

    def stop(self) -> None:
        _nc_direct_stop(self._nc_direct)

    def putstr(
            self, string: str,
            nc_channels: Optional[NcChannels] = None) -> int:

        return _nc_direct_putstr(
            self._nc_direct,
            string,
            nc_channels._nc_channels
            if nc_channels is not None else nc_channels,
        )

    @property
    def dimensions_yx(self) -> Tuple[int, int]:
        return (_nc_direct_get_dim_y(self._nc_direct),
                _nc_direct_get_dim_x(self._nc_direct))

    @property
    def cursor_enabled(self) -> Optional[bool]:
        return self._is_cursor_enabled

    @cursor_enabled.setter
    def cursor_enabled(self, set_to_what: Optional[bool]) -> None:
        self._is_cursor_enabled = set_to_what
        if set_to_what:
            _nc_direct_enable_cursor(self._nc_direct)
        else:
            _nc_direct_disable_cursor(self._nc_direct)


NC_INPUT_KEYS: Dict[str, int] = {
    'invalid': _notcurses.NCKEY_INVALID,
    'up': _notcurses.NCKEY_UP,
    'resize': _notcurses.NCKEY_RESIZE,
    'right': _notcurses.NCKEY_RIGHT,
    'down': _notcurses.NCKEY_DOWN,
    'left': _notcurses.NCKEY_LEFT,
    'insert': _notcurses.NCKEY_INS,
    'delete': _notcurses.NCKEY_DEL,
    'backspace': _notcurses.NCKEY_BACKSPACE,
    'page_down': _notcurses.NCKEY_PGDOWN,
    'page_up': _notcurses.NCKEY_PGUP,
    'home': _notcurses.NCKEY_HOME,
    'ebd': _notcurses.NCKEY_END,
    'f0': _notcurses.NCKEY_F00,
    'f1': _notcurses.NCKEY_F01,
    'f2': _notcurses.NCKEY_F02,
    'f3': _notcurses.NCKEY_F03,
    'f4': _notcurses.NCKEY_F04,
    'f5': _notcurses.NCKEY_F05,
    'f6': _notcurses.NCKEY_F06,
    'f7': _notcurses.NCKEY_F07,
    'f8': _notcurses.NCKEY_F08,
    'f9': _notcurses.NCKEY_F09,
    'f10': _notcurses.NCKEY_F10,
    'f11': _notcurses.NCKEY_F11,
    'f12': _notcurses.NCKEY_F12,
    'enter': _notcurses.NCKEY_ENTER,
    'caps_locl': _notcurses.NCKEY_CLS,
    'down_left': _notcurses.NCKEY_DLEFT,
    'down_right': _notcurses.NCKEY_DRIGHT,
    'up_left': _notcurses.NCKEY_ULEFT,
    'up_right': _notcurses.NCKEY_URIGHT,
    'center': _notcurses.NCKEY_CENTER,
    'begin': _notcurses.NCKEY_BEGIN,
    'cancel': _notcurses.NCKEY_CANCEL,
    'close': _notcurses.NCKEY_CLOSE,
    'command': _notcurses.NCKEY_COMMAND,
    'copy': _notcurses.NCKEY_COPY,
    'exit': _notcurses.NCKEY_EXIT,
    'print': _notcurses.NCKEY_PRINT,
    'refresh': _notcurses.NCKEY_REFRESH,
    'mouse_left_button': _notcurses.NCKEY_BUTTON1,
    'mouse_middle_button': _notcurses.NCKEY_BUTTON2,
    'mouse_right_button': _notcurses.NCKEY_BUTTON3,
    'mouse_scroll_up': _notcurses.NCKEY_SCROLL_UP,
    'mouse_scroll_down': _notcurses.NCKEY_SCROLL_DOWN,
    'mouse_6': _notcurses.NCKEY_BUTTON6,
    'mouse_release': _notcurses.NCKEY_RELEASE,
}

NC_INPUT_CODES: Dict[int, str] = {
    value: key for key, value in NC_INPUT_KEYS.items()
}
