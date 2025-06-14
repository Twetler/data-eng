from src.spatial import RectanglePolygonIterator
import logging as log
import matplotlib.pyplot as plt

log.basicConfig(level=log.INFO)



def test_polygon_iterator(mini_rects: int = 8):
    """
    Use: https://www.keene.edu/campus/maps/tool/
    """

    log.info("Testing Polygon Iterator")
    # Rectangle covering Lisbon (approximate bounding box)
    rectangle_coords = [
        (38.6900, -9.2300),  # SW
        (38.6900, -9.0800),  # SE
        (38.8300, -9.0800),  # NE
        (38.8300, -9.2300),  # NW
    ]

    plt.figure()
    # Plot outer polygon in blue
    xs, ys = zip(*rectangle_coords)
    plt.plot(ys + (ys[0],), xs + (xs[0],), 'bo-')

    # Plot inner polygons in red
    for poly in RectanglePolygonIterator(rectangle_coords, n_polygons=mini_rects):
        log.info(f"Poly: {poly}")
        px, py = zip(*poly)
        plt.plot(py + (py[0],), px + (px[0],), 'ro-')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Polygon Iterator')
    plt.legend()
    plt.show()

    log.info("Polygon Iterator test ended")
    return True
        
