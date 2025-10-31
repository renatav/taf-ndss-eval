import os
from pathlib import Path
import sys
from taf.git import GitRepository
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, update_commit_in_target_file, update_target_repo

REPO_ROOT = "../workspaces/scenario6"
ATTACKER_DIR = Path(REPO_ROOT, "attacker")
REPO_NAME = "law-html"


def run():
    print("An attacker pushes a malicious but invalid update, like the one in Scenario 2.\n")


    namespace = find_namespace(ATTACKER_DIR)
    target_repo_path = Path(ATTACKER_DIR, namespace, REPO_NAME)
    auth_repo_path = Path(ATTACKER_DIR, namespace, "law")
    target_repo = GitRepository(path=target_repo_path)
    print()
    target_commit = update_target_repo(target_repo)
    auth_repo = AuthenticationRepository(path=auth_repo_path)

    target_file_path = auth_repo_path / "targets" / namespace / REPO_NAME

    update_commit_in_target_file(target_file_path, target_commit)
    auth_repo.commit("Update target commit without signing")
    auth_repo.push(no_verify=True)
