#!/usr/bin/env python3

import inspect
import sys

class Boxgen:
    def __init__(self, height, width, thickness):
        pass

def main(args):
    """Usage: boxgen HEIGHT WIDTH THICKNESS
    Where:
        HEIGHT     is the height of a card.
        WIDTH      is the width of a card.
        THICKNESS  is the thickness of the entire deck.
    All measurements are in millimeters.
    """

    if args[0] == __file__:
        args = args[1:]

    if len(args) != 3:
        print(inspect.getdoc(main), file=sys.stderr)
        return 1

    Boxgen(*args)
    return 0

if __name__ == '__main__':
    exit(main(sys.argv))
