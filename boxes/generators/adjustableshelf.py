#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *

class AdjustableShelf(Boxes):
    """An adjustable shelf"""

    description = """An adjustable shelf system vaguely similar to
    DividerTray.  It creates a shelving system with dividers shelves
    that are fully supported on 3 sides, so they can take a bit of
    weight."""

    ui_group = "Shelf"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings, space=4,
                             finger=4)
        self.buildArgParser("sx", "y", "sh");
        self.argparser.add_argument(
            "--slop", action="store", type=float, default=0.5,
            help="""Extra slop in the slot width to allow for easy
            insertion and removal of the shelves""")
        self.argparser.add_argument(
            "--attach", action="store", type=float, default=25,
            help="""Amount of margin to leave at the rear of each
            shelf, so that the inner sidewalls can be placed and are
            not cut apart entirely""")
        

    def create_back_wall_holes(self):
        h = self.inner_h
        nx = len(self.sx)
        nh = len(self.sh)
        w = self.inner_x / nx
        for i in range(nx-1):
            self.fingerHolesAt((i+1)*w, 0, h, angle=90)
        
    def create_top_wall_holes(self):
        nx = len(self.sx)
        y = self.y
        w = self.inner_x / nx
        for i in range(nx-1):
            self.fingerHolesAt((i+1)*w, 0, y, angle=90)

    def slider_cutout(self):
        sh = self.sh
        nh = len(sh)
        t = self.thickness
        y = self.y
        pos = 0
        
        for h in sh[:-1]:
            pos += h + t
            self.rectangularHole(0, pos, y-self.attach, t+self.slop, center_x = False)

    def shelf_cutout(self):
        sh = self.sh
        nh = len(sh)
        t = self.thickness
        y = self.y
        pos = 0
        for z in [0, self.sx[0]]:
            self.rectangularHole(y-self.attach, z, self.attach, t+self.slop, center_x = False)
    def create_outer_box(self):
        sx, y, sh, t = self.sx, self.y, self.sh, self.thickness

        # outer vertical walls are 2 thicknesses, i.e. 1 *extra*
        #      thickness for left and 1 *extra* for right

        # inner vertical walls are 3 thicknesses, i.e. 3 *extra*
        #      thicknesses for every interior vertical walls.

        n_internal_vert_walls = len(sx)-1
        x = sum(sx) + 2*t + 3*t*n_internal_vert_walls
        h = sum(sh) + (len(sh)-1)*t
        self.inner_h = h
        self.inner_x = x
        # print(f"{sx}, {sh}, {h}, {t}, {x}, {h}")

        # Create the rear of the box
        # Create the sidewalls of the outer box

        self.rectangularWall(
            y, h, move="right", edges="FFFe")
        self.rectangularWall(
            x, h, move="right", edges="ffff",
            callback=[self.create_back_wall_holes])
        self.rectangularWall(
        y, h, move="up", edges="FeFF")
        # Create the top and bottom of the outer box
        self.rectangularWall(
            x, y, move="left up", edges="Ffef", callback=[self.create_top_wall_holes])
        self.rectangularWall(
            x, y, move="up",      edges="efFf", callback=[self.create_top_wall_holes])

        # Create the inner walls
        nx = len(sx)
        for i in range(nx-1):
            move = "right"
            if i == 0:
                move = "left right"
            self.rectangularWall(
                y, h, move=move, edges="fffe")

        # Create the inner shelf sliders
        for i in range(2+(nx-1)*2):
            move = "right"
            self.rectangularWall(
                y, h, move=move, edges="eeee", callback=[self.slider_cutout])

        # And finally, create a sample shelf of each width
        sizes = {}
        for x in sx:
            if x not in sizes:
                sizes[x] = True
                self.rectangularWall(y, x, move="up", callback=[self.shelf_cutout])
        return

    def create_tray(self):
        pitch = self.pitch
        nx, ny = self.x, self.y
        margin = self.m
        x, y, h = nx*pitch, ny*pitch, self.h
        t = self.thickness
        x += 2*margin
        y += 2*margin
        t1, t2, t3, t4 = "eeee"
        b = self.edges.get(self.bottom_edge, self.edges["F"])
        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"

        with self.saved_context():
            self.rectangularWall(x, h, [b, sideedge, t1, sideedge],
                                 ignore_widths=[1, 6], move="up")
            self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                                 ignore_widths=[1, 6], move="up")

            if self.bottom_edge != "e":
                self.rectangularWall(x, y, "ffff", move="up")

        self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                             ignore_widths=[1, 6], move="right only")
        self.rectangularWall(y, h, [b, "f", t2, "f"],
                             ignore_widths=[1, 6], move="up")
        self.rectangularWall(y, h, [b, "f", t4, "f"],
                             ignore_widths=[1, 6], move="up")
        return

    def render(self):
        self.create_outer_box()
