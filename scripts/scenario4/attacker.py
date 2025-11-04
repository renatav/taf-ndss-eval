import json
import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from taf.git import GitRepository
from taf.models.types import Commitish
from taf.auth_repo import AuthenticationRepository


REPO_NAME = "cityofsanmateo/law-html"
AUTH_REPO_NAME = "cityofsanmateo/law"


def reset_repos_to_target_commits(lib_path, auth_repo_path):
    targets_dir = Path(auth_repo_path, "targets", "cityofsanmateo")

    commit_map = {}

    for target_file in targets_dir.iterdir():
        data = json.loads(target_file.read_text())
        commit = data.get("commit")
        if commit:
            commit_map[target_file.name] = Commitish(commit)

    for repo_name, commit in commit_map.items():
        repo_path = lib_path / "attacker" / "cityofsanmateo" / repo_name
        target_repo = GitRepository(path=repo_path)
        target_repo.reset_to_commit(commit=commit, hard=True)
        # branch = target_repo.get_current_branch()
        target_repo.push(force=True)


def run(lib_path):
    print("The attacker has obtained credentials that grant commit and push access to both the target and authentication repositories.")
    print("They have not compromised any metadata signing keys.")
    print("They revert all repositories to a previous commit and force-push the branches, attempting to make users believe an older version is the current one.\n")

    auth_repo_path = Path(lib_path, "attacker", AUTH_REPO_NAME)
    auth_repo = AuthenticationRepository(path=auth_repo_path)
    auth_repo.reset_num_of_commits(2, hard=True)
    reset_repos_to_target_commits(lib_path, auth_repo_path)
    auth_repo.push(force=True, no_verify=True)

