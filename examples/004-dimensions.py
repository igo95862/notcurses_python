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
from time import sleep

from notcurses import get_std_plane

std_plane = get_std_plane()

red = 0x80
green = 0x80
blue = 0x80

y_dimension, x_dimension = std_plane.dimensions

for y in range(y_dimension):
    for x in range(x_dimension):
        std_plane.set_foreground_color(red, green, blue)
        std_plane.set_background_color(red, green, blue)
        std_plane.putstr('X', y_pos=y, x_pos=x)
        blue = (blue + 2) % 256
        green = (green + 2) % 256
        red = (red + 2) % 256

std_plane.render()

sleep(5)
