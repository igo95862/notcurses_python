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
from typing import Optional


class _NcChannels:
    ...


class _NcPlane:
    ...


class _NotcursesContext:
    ...


class _NcDirect:
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


def get_notcurses_version() -> str:
    """Returns notcurses version from library"""
    ...
