import json
import os
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace
from taf.git import GitRepository
from taf.models.types import Commitish

REPO_ROOT = "../workspaces/scenario4"
ATTACKER_DIR = Path(REPO_ROOT, "attacker")
REPO_NAME = "law-xml"

def reset_repos_to_target_commits(auth_repo_path, namespace):
    targets_dir = Path(auth_repo_path, "targets", namespace)

    commit_map = {}

    for target_file in targets_dir.iterdir():
        data = json.loads(target_file.read_text())
        commit = data.get("commit")
        if commit:
            commit_map[target_file.name] = Commitish(commit)

    for repo_name, commit in commit_map.items():
        repo_path = ATTACKER_DIR / namespace / repo_name
        target_repo = GitRepository(path=repo_path)
        target_repo.reset_to_commit(commit=commit, hard=True)
        # branch = target_repo.get_current_branch()
        target_repo.push(force=True)


def run():

    namespace = find_namespace(ATTACKER_DIR)

    auth_repo_path = os.path.join(ATTACKER_DIR, namespace, "law")
    # force_remove_last_n_commits(auth_repo_path, 20)
    reset_repos_to_target_commits(auth_repo_path, namespace)

