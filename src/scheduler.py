import time
from datetime import datetime, timedelta

import schedule

from auto_convert_collection_to_skos import parse_collection_id
from base_logger import logger
from git_pusher import push_to_github
from housekeeping import housekeeping


def job():
    start_time = datetime.now()
    parse_collection_id()
    push_to_github()
    housekeeping()
    logger.info(f"Next job will start at: {start_time + timedelta(hours=1)}")


def run_scheduler():
    # execute job every second hour
    job_start_time = datetime.now() + timedelta(minutes=1)
    logger.info(f"Job will start at: {job_start_time.strftime('%I:%M%p')}")
    schedule.every().hour.at(":" + job_start_time.strftime('%M')).do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
