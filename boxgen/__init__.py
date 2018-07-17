#!/usr/bin/env python3

from collections import namedtuple
import inspect
import svgwrite
import sys

GridItem = namedtuple('GridItem', ['offset', 'size'])

class Grid:
    def __init__(self, cols, rows, layout):
        self.cols   = cols
        self.rows   = rows
        self.items = self._parse_layout(layout)

    @property
    def items_with_offsets(self):
        y_offset = 0
        for row in range(0, len(self.rows)):
            x_offset = 0
            for col in range(0, len(self.cols)):
                item = self.items[row][col]
                if item != "-":
                    offset = (x_offset, y_offset)
                    size = (self.cols[col], self.rows[row])
                    yield GridItem(offset, size)
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
    def __init__(self, height, width, thickness):
        self.height     = int(height)
        self.width      = int(width)
        self.depth      = int(thickness)

    def get_file_path(self):
        return "box-%.3ix%.3ix%.3i.svg" % (self.height, self.width, self.depth)

    @classmethod
    def rect(self, size, offset, stroke="black"):
        return svgwrite.shapes.Rect(insert=offset, size=size, stroke=stroke,
                fill="white")

    def generate(self):
        svg = svgwrite.Drawing(self.get_file_path(), profile='tiny')

        depth = self.depth
        width = self.width
        height = self.height

        grid = Grid(cols=[depth, width, depth, width, depth],
                    rows=[depth, depth, height, depth],
                    layout=
                    "-    flap -    -    -    "
                    "tiny flap tiny -    -    "
                    "side face side face side "
                    "tiny flap tiny flap -    ")

        for item in grid.items_with_offsets:
            svg.add(self.rect(item.size, item.offset))

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
