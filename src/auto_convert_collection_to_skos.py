from base_logger import logger
from datetime import datetime

from esconverter import ESConverter

from settings import START_COLLECTION_ID, START_COLLECTION_NAME

esc = ESConverter()
appendix = esc.appendix
base_url = esc.base_url


def parse_collection_id():
    start_id = START_COLLECTION_ID
    logger.info(f"Starting skos-converter with id {start_id}")
    start_time = datetime.now()
    print(f"converting id: {start_id}")
    url = base_url + start_id + appendix

    result_collection: dict = {
        "id": start_id,
        "prefLabel": START_COLLECTION_NAME,
        "children": []
    }
    result = esc.get_all_collections(url, result_collection)
    end_time = datetime.now()
    logger.info(f"Crawling collections took: {end_time - start_time}")
    esc.buildGraph(data=result, start_id=start_id,
               collection_name=START_COLLECTION_NAME)

if __name__ == "__main__":
    parse_collection_id()
