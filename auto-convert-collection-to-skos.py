from pprint import pprint
import json
from esconverter import ESConverter

esc = ESConverter()
appendix = esc.appendix
base_url = esc.base_url

def read_ids():
    with open("ids.json") as f:
        dict_ids = json.load(f)
        list_ids = list(dict_ids.keys())
        return list_ids, dict_ids


def parse_collection_id(_id, dict_ids):
    start_id = _id
    collection_name = dict_ids[start_id]
    print(f"converting: {collection_name}")
    url = base_url + start_id + appendix

    result_collection: dict = {
        "id": start_id,
        "prefLabel": collection_name,
        "children": []
    }
    result = esc.get_all_collections(url, result_collection)
    esc.buildGraph(data=result, start_id=start_id,
               collection_name=collection_name)

# read ids
list_ids, dict_ids = read_ids()

for _id in list_ids:
    parse_collection_id(_id, dict_ids)
