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

from ._notcurses import (_nc_channels_set_background_rgb,
                         _nc_channels_set_foreground_rgb,
                         _nc_direct_disable_cursor, _nc_direct_enable_cursor,
                         _nc_direct_get_dim_x, _nc_direct_get_dim_y,
                         _nc_direct_init, _nc_direct_putstr, _nc_direct_stop,
                         _nc_plane_dimensions_yx, _nc_plane_erase,
                         _nc_plane_putstr, _nc_plane_set_background_rgb,
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
    def __init__(self, plane: _NcPlane, parent: NotcursesContext) -> None:
        self._nc_plane = plane
        self.parent = parent

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

    def render(self) -> None:
        self.parent.render()


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
