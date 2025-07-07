import yaml
import os
import json
import pandas as pd
import itertools

def load_config_yaml(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        config: dict = yaml.safe_load(file)
    return config

def unpack_results(filepath: str) -> list:
    with open(filepath) as f:   
        loaded_var: dict = json.load(f)
        results: list[dict] = loaded_var["results"]
        if len(results) >= 50:
            raise Exception(f"Maximum limit of 50 reached, you may be losing data: {len(results)}")
    return results

def load_tmp_data(path: str) -> pd.DataFrame:
    samples: list = list()
    for _,_, files in os.walk(path):
        for file in files:
            if not os.path.isdir(file):
                fullpath = os.path.join(path, file)
                with open(fullpath) as f:
                    loaded_var: dict = json.load(f)
                results: list[dict] = loaded_var['results']
                samples.append(results)
            else: 
                pass
    unpacked_samples = list(itertools.chain(*samples))
    return pd.DataFrame(unpacked_samples)

def unpack_credit_card(obj: dict) -> bool:
    if isinstance(obj, float):
        return None
    else:
        try:
            var: bool = bool(obj.get("payment").get("credit_cards").get("accepts_credit_cards"))
        except Exception as e:
            var: float = None
        return var
    
def unpack_social_media(obj:dict, media: str) -> bool:
    medias_obj = {
        "facebook" : "facebook_id",
        "instagram" :  "instagram",
        "twitter" : "twitter"
    }
    assert media in medias_obj.keys(), "Wrong media."
    
    if isinstance(obj, float) or obj == {}:
        return None
    else:
        key: str = medias_obj[media]
        return obj.get(key)

def convert_columns(df):
    dtype_mapping = {
        'fsq_id': str,
        'name': str,
        'venue_reality_bucket': str,
        'website': str,
        'price': str,
        'description': str,
        'address': str,
        'country': str,
        'locality': str,
        'region': str,
        'facebook_id': str,
        'instagram': str,
        'twitter': str,
        'hours_display': str,
        'rating': float,
        'latitude': float,
        'longitude': float,
        'postcode': 'Int64',  # Nullable integer type
        'accepts_pinpas': bool,
        'hours_popular': object,  # Will keep as list[dict]
        'hours_regular': object   # Will keep as list[dict]
    }
    
    # Apply type conversions
    for col, dtype in dtype_mapping.items():
        if col in df.columns:
            if dtype == str:
                df[col] = df[col].astype(str)
            elif dtype in [float, int]:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif dtype == 'Int64':
                df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    
    return df
    
def get_places_etl(df: pd.DataFrame) -> pd.DataFrame:
    """
    Proceeds to run all the transformation pipelines
    """
    # Treats categories
    df.loc[:, "categories"] = df['categories'].apply(lambda cats: cats[0]['short_name'] if cats and 'short_name' in cats[0] else None)
    df.drop(columns = ["categories"], inplace = True)
    # Treats geocoding
    df.loc[:, "latitude"] = df.geocodes.apply(lambda dic: dic['main']['latitude'])
    df.loc[:, "longitude"] = df.geocodes.apply(lambda dic: dic['main']['longitude'])
    df.drop(columns = ["geocodes"], inplace = True)
    # Treats location
    df.loc[:, "address"] = df.location.apply(lambda dic: dic.get("address"))
    df.loc[:, "country"] = df.location.apply(lambda dic: dic.get('country'))
    df.loc[:, "locality"] = df.location.apply(lambda dic: dic.get('locality'))
    df.loc[:, "postcode"] = df.location.apply(lambda dic: dic.get('postcode'))
    df.loc[:, "region"] = df.location.apply(lambda dic: dic.get('region'))
    df.drop(columns = ["location"], inplace = True)
    # Treats features
    df.loc[:, "accepts_pinpas"] = df.features.apply(lambda obj: unpack_credit_card(obj))
    df.drop(columns = ["features"], inplace = True)
    # Treats social media
    df.loc[:, "facebook_id"] = df.social_media.apply(lambda obj: unpack_social_media(obj, "facebook"))
    df.loc[:, "instagram"] = df.social_media.apply(lambda obj: unpack_social_media(obj, "instagram"))      
    df.loc[:, "twitter"] = df.social_media.apply(lambda obj: unpack_social_media(obj, "twitter"))
    df.drop(columns = ['social_media'], inplace = True)

    # Enforces column types
    df = convert_columns(df)
    return df
