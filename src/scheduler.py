from auto_convert_collection_to_skos import parse_collection_id
from base_logger import logger
from git_pusher import push_to_github
from housekeeping import housekeeping


def job():
    parse_collection_id()
    push_to_github()
    housekeeping()
    logger.info("Finished")


def run_scheduler():
    # job cycle is done via external infrastructure
    job()
