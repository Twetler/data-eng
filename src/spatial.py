import numpy as np

class RectangleGridIterator:
    """
    Iterator that yields lat/lon points inside a rectangle (defined by 4 lat/lon pairs)
    spaced by approximately the given distance (in meters).
    The rectangle should be axis-aligned (edges parallel to lat/lon axes) and specified as:
    [SW, SE, NE, NW], where each corner is [lat, lon].
    """
    def __init__(self, rect_points, distance_m):
        assert len(rect_points) == 4, "Rectangle must have 4 points [SW, SE, NE, NW]"
        self.rect_points = rect_points
        self.distance_m = distance_m
        self._setup_grid()

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        # Returns distance in meters between two lat/lon points
        R = 6371000  # Earth radius in meters
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi/2.0)**2 + \
            np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2.0)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        return R * c

    def _latlon_steps(self, start, end, distance):
        # Returns number of steps and array of linearly spaced coords
        dist = self._haversine_distance(start[0], start[1], end[0], end[1])
        steps = max(2, int(np.ceil(dist / distance)) + 1)
        lats = np.linspace(start[0], end[0], steps)
        lons = np.linspace(start[1], end[1], steps)
        return steps, lats, lons

    def _setup_grid(self):
        # Rectangle corners: SW, SE, NE, NW
        SW, SE, NE, NW = self.rect_points
        # Along latitude (vertical lines from SW to NW), and longitude (horizontal lines from SW to SE)
        self.n_rows, start_lats, _ = self._latlon_steps(SW, NW, self.distance_m)
        self.n_cols, _, start_lons = self._latlon_steps(SW, SE, self.distance_m)
        # Prepare meshgrid
        self.grid_lats = np.linspace(SW[0], NW[0], self.n_rows)[:, None] * np.ones(self.n_cols)[None, :]
        self.grid_lons = np.linspace(SW[1], SE[1], self.n_cols)[None, :] * np.ones(self.n_rows)[:, None]
        # If rectangle is not aligned, could do bilinear interpolation, but this assumes axis-aligned rectangles

    def __iter__(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                yield [float(self.grid_lats[i, j]), float(self.grid_lons[i, j])]

# Example Usage:
if __name__ == "__main__":
    # Rectangle: SW, SE, NE, NW
    rect = [
        [37.0, -122.0],  # SW
        [37.0, -121.99], # SE
        [37.01, -121.99],# NE
        [37.01, -122.0]  # NW
    ]
    distance = 100  # meters
    for latlon in RectangleGridIterator(rect, distance):
        print(latlon)