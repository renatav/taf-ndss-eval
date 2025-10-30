import os
from pathlib import Path
import sys
from taf.git import GitRepository
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import push_no_verify, find_namespace, update_commit_in_target_file, update_target_repo

REPO_ROOT = "../workspaces/scenario2"
ATTACKER_DIR = Path(REPO_ROOT, "attacker")
REPO_NAME = "law-html"


def run():
    print("The attacker has obtained credentials that grant commit and push access to both a target and the authentication repository.")
    print("They have not compromised any metadata signing keys.")
    print("They alter law-html and push a malicious update.\n")
    print("The attacker then manually updates the file storing last valid commit for that target repository in the authentication repository and pushes the change.")
    print("They do not update and sign TUF metadata.\n")

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
