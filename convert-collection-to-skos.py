from pprint import pprint
from esconverter import ESConverter

esc = ESConverter()

start_url = esc.base_url + esc.main_collection_id + esc.appendix

# get all collections
esc.topic_identifier = [
    "activated",
    ""
]
main_ids = esc.getMainCollections(start_url, esc.main_collection)

esc.topic_identifier = [
    "activated",
    # ""
]

# add Main collection to main ids
main_ids.update({esc.main_collection_id: "Main-Collection (All)"})

pprint(main_ids)

start_id = input("Which id to convert? ") or esc.main_collection_id
collection_name = main_ids[start_id]
print(f"converting: {collection_name}")

esc.main_collection["id"] = start_id
collection_name = input(
    f"Name of collection (default: {collection_name}): ") or collection_name
print(f"Name: {collection_name}")

url = esc.base_url + start_id + esc.appendix

result_collection: dict = {
    "id": start_id,
    "prefLabel": collection_name,
    "children": []
}

result = esc.get_all_collections(url, result_collection)

esc.buildGraph(data=result, start_id=start_id,
           collection_name=collection_name)
