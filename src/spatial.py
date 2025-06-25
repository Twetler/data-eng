import numpy as np
import logging as log

class RectanglePolygonIterator: 
    """
    Iterator that yields smaller rectangles (as 4 lat/lon points: SW, SE, NE, NW)
    inside a big axis-aligned rectangle, dividing it into a grid of polygons.
    """
    def __init__(self, rect_points: list[tuple[float]], n_polygons: int):
        assert len(rect_points) == 4, "Rectangle must have 4 points [SW, SE, NE, NW], in this order"
        self.rect_points = rect_points

        assert isinstance(n_polygons, int), "Hmm, that's not int" 
        
        n_rows: int = int(np.sqrt(n_polygons))
        n_cols: int = int(np.ceil(n_polygons / n_rows))
        self.n_rows: int = n_rows
        self.n_cols: int = n_cols


        self._setup_grid()

    def _setup_grid(self):
        SW, SE, NE, NW = self.rect_points
        # Linspace for lat
        self.row_lats = np.linspace(SW[0], NW[0], self.n_rows + 1)
        # Linspace for long
        self.col_lons = np.linspace(SW[1], SE[1], self.n_cols + 1)

    def __iter__(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                # Rectangle corners for this cell
                sw = [self.row_lats[i], self.col_lons[j]]
                se = [self.row_lats[i],self.col_lons[j+1]]
                ne = [self.row_lats[i+1],self.col_lons[j+1]]
                nw = [self.row_lats[i+1],self.col_lons[j]]
                yield [sw, se, ne, nw]
