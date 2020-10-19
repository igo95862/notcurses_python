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
from typing import Tuple, Optional


class _NcPlane:
    def get_dimensions(self) -> Tuple[int, int]:
        ...

    def putstr(self, string: str, y_pos: int = -1, x_pos: int = -1) -> int:
        ...

    def set_background_color(self, red: int, green: int, blue: int) -> None:
        ...

    def set_foreground_color(self, red: int, green: int, blue: int) -> None:
        ...


class _NotcursesContext:
    def __init__(self, fileno: int = -1):
        ...

    def get_std_plane(self) -> _NcPlane:
        ...

    def render(self) -> None:
        ...


def get_notcurses_version() -> str:
    """Returns notcurses version from library"""
    ...


class _NcDirect:
    def putstr(self, string: str,
               channels: Optional[_NcChannels] = None) -> None:
        ...

    def disable_cursor(self) -> None:
        ...

    def enable_cursor(self) -> None:
        ...


class _NcChannels:
    def set_background_color(self, red: int, green: int, blue: int) -> None:
        ...

    def set_foreground_color(self, red: int, green: int, blue: int) -> None:
        ...
