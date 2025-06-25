from src.spatial import RectanglePolygonIterator
from src.api import fetch_places_api
from src.utils import load_config_yaml
from src.gcp import upload_blob
import logging as log
import matplotlib.pyplot as plt
import webbrowser
import folium
import os

from dotenv import load_dotenv

log.basicConfig(level=log.INFO)
load_dotenv()

FOURSQUARE_KEY: str = os.getenv("FOURSQUARE_API_KEY")
BUCKET_NAME: str = os.getenv("GOOGLE_CLOUD_BUCKET")



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
        
def city_bounding_boxes():

    config: dict = load_config_yaml("config.yaml")
    # Center the map on the first city
    first_city: dict = config['cities'][0]
    center: tuple[float] = first_city['rectangle_coords'][0]

    m = folium.Map(location=center, zoom_start=10)

    for city in config['cities']:
        # Draws city boundaries
        folium.Polygon(
            locations=city['rectangle_coords'],
            popup=city['name'],
            color='blue',
            fill=True,
            fill_opacity=0.2
        ).add_to(m)
        # Inside this city we also want to draw the mini boxes
        for poly in RectanglePolygonIterator(
            rect_points=city['rectangle_coords'],
            n_polygons = 64):

            folium.Polygon(
                locations = poly,
                popup=str(poly),
                color = 'red',
                fill = True,
                fill_opacity = 0.1
            ).add_to(m)

    # Save and open the map
    m.save('city_polygons_map.html')
    webbrowser.open('city_polygons_map.html')

def get_places() -> dict:
    config: dict = load_config_yaml("config.yaml")
    first_city: dict = config['cities'][0]
    city_name: str = first_city['name'].lower()
    poly_idx: int = 0
    for poly in RectanglePolygonIterator(rect_points=first_city['rectangle_coords'], n_polygons=4):
        log.info(f"Fetching Polygon : {poly_idx}")
        file_path: str = f"tmp/{city_name}-poly-{poly_idx}.json"
        places_raw: dict = fetch_places_api(file_path, FOURSQUARE_KEY, polygon = poly)
        destination_path: str = os.path.join(
            city_name, f"{city_name}-poly-{poly_idx}.json"
        )
        upload_blob(BUCKET_NAME, file_path, destination_path)
        poly_idx += 1
    return places_raw





    