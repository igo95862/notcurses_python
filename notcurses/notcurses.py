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

from ._notcurses import (_NcChannels, _nc_channels_set_background_rgb,
                         _nc_channels_set_foreground_rgb, _NcDirect,
                         _nc_direct_get_dim_x, _nc_direct_get_dim_y,
                         _nc_direct_init, _NcPlane, _NotcursesContext,
                         _nc_direct_putstr, _nc_direct_enable_cursor,
                         _nc_direct_disable_cursor)


class NcPlane:
    def __init__(self) -> None:
        self._nc_plane = _NcPlane()


_default_context: Optional[_NotcursesContext] = None


def get_std_plane() -> NcPlane:
    ...


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
        if start_immideatly:
            self.start()

    def start(self) -> None:
        _nc_direct_init(self._nc_direct)

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
