import os

from dotenv import load_dotenv

from base_logger import logger

load_dotenv()

START_COLLECTION_ID = os.environ.get("start_collection_id", None)
START_COLLECTION_NAME = os.environ.get("default_name_for_start_collection", "")
GITHUB_TOKEN = os.environ.get("github_token", "")
GIT_REPO = os.environ.get("git_repo", "")
FILENAME_FOR_PUSH = os.environ.get("filename_for_push", "oehTopics.ttl")

errors = []

if GITHUB_TOKEN == "":
    errors.append("github_token is empty, please add token with push permissions")

if GIT_REPO == "":
    errors.append("git_repo is empty, please add a repo to push to")

if len(errors) != 0:
    for err in errors:
        logger.error(err)
    raise Exception("Necessary environment variables are missing")
