import os
import logging

from dotenv import load_dotenv


load_dotenv()

def get_log_level():
    log_level = os.environ.get("log_level", logging.INFO)

    if log_level == "debug":
        return logging.DEBUG
    return logging.INFO

START_COLLECTION_ID = os.environ.get("start_collection_id", None)
START_COLLECTION_NAME = os.environ.get("default_name_for_start_collection", "")
GITHUB_TOKEN = os.environ.get("github_token", "")
GIT_REPO = os.environ.get("git_repo", "")
FILENAME_FOR_PUSH = os.environ.get("filename_for_push", "oehTopics.ttl")
LOG_LEVEL = get_log_level()
DRY_RUN = eval(os.environ.get("dry_run", "True"))

errors = []

if GITHUB_TOKEN == "":
    errors.append("github_token is empty, please add token with push permissions")

if GIT_REPO == "":
    errors.append("git_repo is empty, please add a repo to push to")

if len(errors) != 0:
    for err in errors:
        print(err)
    raise Exception("Necessary environment variables are missing")

def show_configs():
    print(f"START_COLLECTION_ID: {START_COLLECTION_ID}")
    print(f"START_COLLECTION_NAME: {START_COLLECTION_NAME}")
    print(f"GITHUB_TOKEN: {GITHUB_TOKEN}")
    print(f"GIT_REPO: {GIT_REPO}")
    print(f"FILENAME_FOR_PUSH: {FILENAME_FOR_PUSH}")
    print(f"LOG_LEVEL: {LOG_LEVEL}")
    print(f"DRY_RUN: {DRY_RUN}")


show_configs()
