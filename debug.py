from handleData.prepare import store_region_records
from handleData.utils import load_config
from pymongo import MongoClient

def debug(config_path="./handleData/config.json"):
    config = load_config(config_path)
    client = MongoClient()
    db = client['coronavirus_analysis']
    store_region_records(db, config)

if __name__ == "__main__":
    debug()