from pprint import pprint
import json
from esconverter import ESConverter

esc = ESConverter()
appendix = esc.appendix
base_url = esc.base_url

def read_ids() -> list:
    with open("ids.json") as f:
        ids = list(json.load(f).values())
        return ids


def parse_collection_id(_id):
    start_id = _id
    collection_name = main_ids[start_id]
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
ids = read_ids()

# get all collections
start_url = base_url + esc.main_collection_id + appendix
main_ids = esc.getMainCollections(start_url, esc.main_collection)

# add Main collection to main ids
main_ids.update({esc.main_collection_id: "Main-Collection (All)"})

for _id in ids:
    parse_collection_id(_id)
