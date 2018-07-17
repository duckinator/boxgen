#!/usr/bin/env python3

import inspect
import svgwrite
import sys

class Grid:
    def __init__(self, cols, rows, layout, dashed=[]):
        self.cols  = cols
        self.rows  = rows
        self.items = self._parse_layout(layout)
        self.dashed = dashed

    @classmethod
    def rect(self, size, offset, dashed=None):
        if dashed is None:
            dashed = (False, False, False, False)
        a = (offset[0],             offset[1])
        b = (offset[0] + size[0],   offset[1])
        c = (offset[0] + size[0],   offset[1] + size[1])
        d = (offset[0],             offset[1] + size[1])
        return [(a, b, dashed[0]),
                (b, c, dashed[1]),
                (c, d, dashed[2]),
                (d, a, dashed[3])]

    @property
    def lines(self):
        y_offset = 10
        for row in range(0, len(self.rows)):
            x_offset = 10
            for col in range(0, len(self.cols)):
                item = self.items[row][col]
                if item != '-':
                    offset = (x_offset, y_offset)
                    size = (self.cols[col], self.rows[row])
                    dashed = self.dashed.get((row, col), None)
                    for line in self.rect(size, offset, dashed):
                        yield line
                x_offset += self.cols[col]
            y_offset += self.rows[row]

    def _parse_layout(self, layout):
        items = layout.strip().split()
        chunks = list(self._chunk(items, len(self.cols)))
        assert len(chunks) == len(self.rows)
        return chunks

    def _chunk(self, lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

class Boxgen:
    def __init__(self, height, width, depth):
        self.height = int(height)
        self.width  = int(width)
        self.depth  = int(depth)

    def get_file_path(self):
        return 'box-%.3ix%.3ix%.3i.svg' % (self.height, self.width, self.depth)

    @classmethod
    def line(self, a, b, dashed=False):
        if dashed:
            stroke_dasharray = '3,4'
        else:
            stroke_dasharray = '0'
        return svgwrite.shapes.Line(a, b, stroke='black', stroke_width='2px',
                stroke_dasharray=stroke_dasharray)

    def generate(self):
        svg = svgwrite.Drawing(self.get_file_path(), profile='tiny')

        depth = self.depth
        width = self.width
        height = self.height

        grid = Grid(cols=[depth, width, depth, width, depth],
                    rows=[depth, depth, height, depth],
                    layout=
                    '-    flap -    -    -    '
                    'tiny flap tiny -    -    '
                    'side face side face side '
                    'tiny flap tiny flap -    ',
                    dashed={
                        # Row 0.
                        (0, 1): (False, False, True, False),
                        # Row 1.
                        (1, 0): (False, False, True, False),
                        (1, 1): (True,  False, True, False),
                        (1, 2): (False, False, True, False),
                        # Row 2.
                        (2, 0): (True,  True,  True,  False),
                        (2, 1): (True,  True,  True,  True),
                        (2, 2): (True,  True,  True,  True),
                        (2, 3): (False, True,  True,  True),
                        (2, 4): (False, False, False, True),
                        # Row 3.
                        (3, 0): (True,  False, False, False),
                        (3, 1): (True,  False, False, False),
                        (3, 2): (True,  False, False, True),
                        (3, 3): (True,  False,  False, True),
                    })

        for (a, b, dashed) in grid.lines:
            line = self.line(a, b, dashed)
            svg.add(line)

        return svg

def main(args=None):
    """Usage: boxgen HEIGHT WIDTH DEPTH
    Where:
        HEIGHT     is the height of a card.
        WIDTH      is the width of a card.
        DEPTH      is the thickness of the entire deck.
    All measurements are in millimeters.
    """

    if args == None:
        args = sys.argv[1:]

    if len(args) != 3:
        return inspect.getdoc(main)

    box = Boxgen(*args)
    box.generate().save()
    return 0

if __name__ == '__main__':
    exit(main())
