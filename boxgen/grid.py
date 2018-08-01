import enforce
from typing import Any, Dict, Iterable, List, Tuple, Union

# point = (x, y, dashed?)
Point  = Tuple[int, int, bool]
# line = (pt1, pt2)
Line   = Tuple[Point, Point]
# offset = (x, y)
Offset = Tuple[int, int]
# shape = [pt1, pt2, pt3, ..., ptN]
Shape  = List[Point]

@enforce.runtime_validation
class Grid:
    DashedSpecPos   = Tuple[int, int]
    DashedSpecValue = Tuple[bool, bool, bool, bool]
    DashedSpec      = Dict[DashedSpecPos, DashedSpecValue]

    def __init__(self, cols: List[int], rows: List[int],
            layout: str, dashed: DashedSpec = []):
        self.cols  = cols
        self.rows  = rows
        self.items = self._parse_layout(layout)
        self.dashed = dashed

    @classmethod
    def rect(self, size: Point, offset: Offset, dashed=None) -> Shape:
        if dashed is None:
            dashed = (False, False, False, False)
        a: Line = (offset[0],             offset[1])
        b: Line = (offset[0] + size[0],   offset[1])
        c: Line = (offset[0] + size[0],   offset[1] + size[1])
        d: Line = (offset[0],             offset[1] + size[1])
        return [(a, b, dashed[0]),
                (b, c, dashed[1]),
                (c, d, dashed[2]),
                (d, a, dashed[3])]

    @property
    def lines(self) -> Iterable[Line]:
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

    def _parse_layout(self, layout: str) -> List[List[str]]:
        items = layout.strip().split()
        chunks = list(self._chunk(items, len(self.cols)))
        assert len(chunks) == len(self.rows)
        return chunks

    def _chunk(self, lst: List[Any], chunk_size: int):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

