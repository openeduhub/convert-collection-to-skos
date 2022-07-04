from pathlib import Path

from github import Github, InputGitTreeElement

from base_logger import logger
from settings import DRY_RUN, FILENAME_FOR_PUSH, GIT_REPO, GITHUB_TOKEN
from rdf_compare import same_graphs


def latest_file(path: Path, pattern: str = "*"):
    files = path.glob(pattern)
    sorted_files = sorted(files, key=lambda x: x.stat().st_ctime, reverse=True)
    return sorted_files

def push_to_github():
    """
    Pushes the latest files to GitHub
    Before the push it checks if the grahphs changed.
    If not they will not be pushed.
    """

    latest_files = latest_file(path=Path("data/"), pattern="graph_Taxonomie*")

    if len(latest_files) > 1:
        if same_graphs(latest_files[0], latest_files[1]):
            return

    if DRY_RUN:
        logger.info("dry_run is true, not pushing")
        return

    latest_graph = latest_files[0]

    # using an access token
    g = Github(GITHUB_TOKEN)

    repo = g.get_repo(GIT_REPO) # repo name

    file_list = []
    file_list.append(str(latest_graph.absolute()))
    file_names = []
    file_names.append(FILENAME_FOR_PUSH)

    commit_message = 'auto-update oehTopics'
    master_ref = repo.get_git_ref('heads/master')
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

    logger.info(f"Push of {FILENAME_FOR_PUSH} to {GIT_REPO} successful")

if __name__ == "__main__":
    push_to_github()
