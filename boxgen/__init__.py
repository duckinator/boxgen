#!/usr/bin/env python3

import inspect
import svgwrite
#from svgwrite.shapes import Line, Rect, Circle, Ellipse, Polygon
import sys

class Boxgen:
    def __init__(self, height, width, thickness):
        # 72mm height, 47mm width, 10mm thickness.
        self.height     = int(height)
        self.width      = int(width)
        self.depth      = int(thickness)

    def get_file_path(self):
        return "box-%.3ix%.3ix%.3i.svg" % (self.height, self.width, self.depth)

    @staticmethod
    def _build_side_shape(offset, size):
        if len(size) == 2:
            return svgwrite.shapes.Rect(insert=offset, size=size)
        else:
            return None

    @staticmethod
    def build_side(x_offset, parts):
        shapes = []
        y_offset = 0
        for part in parts:
            if part[0] is not None:
                offset = (x_offset, y_offset)
                shapes.append(Boxgen._build_side_shape(offset, part))
            y_offset += part[1]

        return shapes

    def generate(self):
        svg = svgwrite.Drawing(self.get_file_path(), profile='tiny')
        black = svgwrite.rgb(0, 0, 0)

        height = self.height
        width  = self.width
        depth  = self.depth

        tiny = (depth, depth)
        flap = (width, depth)
        side = (depth, height)
        face = (width, height)

        tiny_off = (None, tiny[1])

        x_offset = 0

        left_side_outer = self.build_side(x_offset,
                (tiny_off, tiny, side, tiny))
        x_offset += tiny[0]

        back = self.build_side(x_offset,
                (flap, flap, face, flap))
        x_offset += flap[0]

        right_side = self.build_side(x_offset,
                (tiny_off, tiny, side, tiny))
        x_offset += tiny[0]

        front = self.build_side(x_offset,
                (tiny_off, tiny_off, face, flap))
        x_offset += face[0]

        left_side_inner = self.build_side(x_offset,
                (tiny_off, tiny_off, side, tiny_off))
        x_offset += side[0]

        shapes = [
            *left_side_outer,
            *back,
            *right_side,
            *front,
            *left_side_inner,
        ]

        for shape in shapes:
            svg.add(shape)#, stroke=black)
        return svg

    def save(self):
        svg.save()

def main(args):
    """Usage: boxgen HEIGHT WIDTH THICKNESS
    Where:
        HEIGHT     is the height of a card.
        WIDTH      is the width of a card.
        THICKNESS  is the thickness of the entire deck.
    All measurements are in millimeters.
    """

    if len(args) != 3:
        return inspect.getdoc(main)

    box = Boxgen(*args)
    box.generate().save()
    return 0

if __name__ == '__main__':
    exit(main(sys.argv[1:]))
