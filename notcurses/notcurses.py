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
from typing import Tuple

from ._notcurses import _NcPlane, _NotcursesContext


class NcPlane:
    def __init__(self, _nc_plane: _NcPlane,
                 _notcurses_context: _NotcursesContext):
        self._nc_plane = _nc_plane
        self._notcurses_context = _notcurses_context

    def putstr(self, string: str, y_pos: int = -1, x_pos: int = -1) -> int:
        return self._nc_plane.putstr(string, y_pos, x_pos)

    def set_background_color(self, red: int, green: int, blue: int) -> None:
        self._nc_plane.set_background_color(red, green, blue)

    def set_foreground_color(self, red: int, green: int, blue: int) -> None:
        self._nc_plane.set_foreground_color(red, green, blue)

    def render(self) -> None:
        self._notcurses_context.render()

    @property
    def dimensions(self) -> Tuple[int, int]:
        return self._nc_plane.get_dimensions()


def get_std_plane() -> NcPlane:
    nctx = _NotcursesContext()
    return NcPlane(nctx.get_std_plane(), nctx)
