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
from ctypes import pointer
from time import sleep

from notcurses.notcurses_api import (NotcursesCell, NotcursesInitOptions,
                                     ncplane_putc_yx,
                                     ncplane_channels,
                                     ncplane_set_bg_rgb8_clipped,
                                     notcurses_init, notcurses_mouse_disable,
                                     notcurses_render, notcurses_stop,
                                     notcurses_top)

# Very simple example. Print Hello world!

# Generate Init options. Not required as None can be passed as NULL pointer.
test_options = NotcursesInitOptions()

# Initialize  notcurses. i is the void pointer to notcurses handle
i = notcurses_init(pointer(test_options), 0)

notcurses_mouse_disable(i)
# Get top plane
top_plane = notcurses_top(i)

ncplane_set_bg_rgb8_clipped(top_plane, 255, 0, 0)
channel_color = ncplane_channels(top_plane)

for character in 'Hello, world!':
    # For every character in Hello World create a new cell
    test_cell = NotcursesCell(
        gcluster=ord(character),
        channels=channel_color,
    )
    # And put it to current cursor
    ncplane_putc_yx(top_plane, -1, -1, pointer(test_cell))

# Render
notcurses_render(i)

sleep(5)


notcurses_stop(i)
