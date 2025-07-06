import yaml
import os
import json

def load_config_yaml(file_path):
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def unpack_results(filepath) -> list:
    with open(filepath) as f:   
        loaded_var: dict = json.load(f)
        results: list[dict] = loaded_var["results"]
        if len(results) >= 50:
            raise Exception(f"Maximum limit of 50 reached, you may be losing data: {len(results)}")
    return results


