import os
from pathlib import Path
import sys
from taf.git import GitRepository
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import update_commit_in_target_file, update_target_repo


REPO_NAME = "cityofsanmateo/law-html"
AUTH_REPO_NAME = "cityofsanmateo/law"


def run(lib_path):
    print("The attacker has obtained credentials that grant commit and push access to both a target and the authentication repository.")
    print("They have not compromised any metadata signing keys.")
    print("They alter law-html and push a malicious update.\n")
    print("The attacker then manually updates the file storing last valid commit for that target repository in the authentication repository and pushes the change.")
    print("They do not update and sign TUF metadata.\n")

    target_repo_path = Path(lib_path, "attacker", REPO_NAME)
    target_repo = GitRepository(path=target_repo_path)
    auth_repo_path = Path(lib_path, "attacker", AUTH_REPO_NAME)
    print()
    target_commit = update_target_repo(target_repo)
    auth_repo = AuthenticationRepository(path=auth_repo_path)

    target_file_path = auth_repo_path / "targets" / REPO_NAME

    update_commit_in_target_file(target_file_path, target_commit)
    auth_repo.commit("Update target commit without signing")
    auth_repo.push(no_verify=True)
