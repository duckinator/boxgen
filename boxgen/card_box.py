import boxgen.grid

class CardBox(boxgen.grid.Grid):
    def __init__(self, height, width, depth):
        height = int(height)
        width  = int(width)
        depth  = int(depth)

        super().__init__(
            cols=[depth, width, depth, width, depth],
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

