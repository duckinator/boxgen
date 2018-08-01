#!/usr/bin/env python3

from boxgen.card_box import CardBox
from boxgen.grid import Point
import enforce
import inspect
from svgwrite import shapes, Drawing
import sys

@enforce.runtime_validation
class Boxgen:
    def __init__(self, height, width, depth):
        height = int(height)
        width  = int(width)
        depth  = int(depth)
        dimensions = (height, width, depth)
        self.filename = 'box-%.3ix%.3ix%.3i.svg' % dimensions
        self.drawing = self.generate(self.filename, *dimensions)

    @classmethod
    def line(self, a: Point, b: Point, dashed: bool = False) -> shapes.Line:
        kwargs = {"stroke": "black"}
        if dashed:
            kwargs["stroke_dasharray"] = "3,4"
        return shapes.Line(a, b, **kwargs)

    @classmethod
    def generate(self, filename, height, width, depth) -> Drawing:
        svg = Drawing(filename, profile='tiny')
        card_box = CardBox(height, width, depth)

        lines = [self.line(*line) for line in card_box.lines]
        for line in lines:
            svg.add(line)

        return svg

    def save(self):
        return self.drawing.save()

def main(args = None) -> int:
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
        print(inspect.getdoc(main), file=sys.stderr)
        return 1

    Boxgen(*args).save()
    return 0

if __name__ == '__main__':
    exit(main())
