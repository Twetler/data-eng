import yaml
from src.spatial import RectanglePolygonIterator

def load_config_yaml(file_path):
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config