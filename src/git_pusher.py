from github import Github
from github import InputGitTreeElement

from base_logger import logger
from settings import GITHUB_TOKEN, GIT_REPO

from pathlib import Path


def latest_file(path: Path, pattern: str = "*"):
    files = path.glob(pattern)
    return max(files, key=lambda x: x.stat().st_ctime)

def push_to_github():

    latest_graph = latest_file(path=Path("data/"), pattern="graph_Taxonomie*")

    # using an access token
    g = Github(GITHUB_TOKEN)

    repo = g.get_repo(GIT_REPO) # repo name

    file_list = list()
    file_list.append(str(latest_graph.absolute()))
    file_names = [
        'oehTopics.ttl'
    ]

    commit_message = 'python commit'
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = []

    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)

    logger.info("Push successful")

if __name__ == "__main__":
    push_to_github()
