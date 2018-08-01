#!/usr/bin/env python3

from boxgen.card_box import CardBox
from boxgen.grid import Point
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
        self.filename = 'box-%.3ix%.3ix%.3i.svg' % (height, width, depth)

    @classmethod
    def line(self, a: Point, b: Point, dashed: bool = False) -> shapes.Line:
        kwargs = {"stroke": "black"}
        if dashed:
            kwargs["stroke_dasharray"] = "3,4"
        return shapes.Line(a, b, **kwargs)

    def _generate(self) -> Drawing:
        svg = Drawing(self.filename, profile='tiny')
        card_box = CardBox(self.height, self.width, self.depth)

        lines = [self.line(*line) for line in card_box.lines]
        for line in lines:
            svg.add(line)

        return svg

    def save(self):
        return self._generate().save()

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

    Boxgen(*args).save()
    return 0

if __name__ == '__main__':
    exit(main())
