#!/usr/bin/env python3

from boxgen.grid import Grid, Point
import enforce
import inspect
from svgwrite import shapes, Drawing
import sys
from typing import List

@enforce.runtime_validation
class Boxgen:
    def __init__(self, height: int, width: int, depth: int):
        self.height = height
        self.width  = width
        self.depth  = depth

    def get_file_path(self) -> str:
        dimensions = (self.height, self.width, self.depth)
        return 'box-%.3ix%.3ix%.3i.svg' % dimensions

    @classmethod
    def line(self, a: Point, b: Point, dashed: bool = False) -> shapes.Line:
        kwargs = {"stroke": "black"}
        if dashed:
            kwargs["stroke_dasharray"] = "3,4"
        return shapes.Line(a, b, **kwargs)

    def generate(self) -> Drawing:
        svg = Drawing(self.get_file_path(), profile='tiny')

        depth:  int = self.depth
        width:  int = self.width
        height: int = self.height

        grid = Grid(cols=[depth, width, depth, width, depth],
                    rows=[depth, depth, height, depth],
                    layout=
                    '-    flap -    -    -    '
                    'tiny flap tiny -    -    '
                    'side face side face side '
                    'tiny flap tiny flap -    ',
                    dashed={
                        # Row 0.
                        (0, 1): (False, False, True,  False),
                        # Row 1.
                        (1, 0): (False, False, True,  False),
                        (1, 1): (True,  False, True,  False),
                        (1, 2): (False, False, True,  False),
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
                        (3, 3): (True,  False, False, True),
                    })

        for (a, b, dashed) in grid.lines:
            line = self.line(a, b, dashed)
            svg.add(line)

        return svg

@enforce.runtime_validation
def main(argv: List[str] = None) -> int:
    """Usage: boxgen HEIGHT WIDTH DEPTH
    Where:
        HEIGHT     is the height of a card.
        WIDTH      is the width of a card.
        DEPTH      is the thickness of the entire deck.
    All measurements are in millimeters.
    """

    if argv == None:
        argv = sys.argv

    args = argv[1:]

    if len(args) != 3:
        print(inspect.getdoc(main), file=sys.stderr)
        return 1

    args = [int(arg) for arg in args]

    box = Boxgen(*args)
    box.generate().save()
    return 0

if __name__ == '__main__':
    exit(main())
