import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from taf.auth_repo import AuthenticationRepository
from taf.utils import run as run_cmd


AUTH_REPO_NAME = "cityofsanmateo/law"


def create_rollback_commit(repo_path, commit_hash):

    changed_files = run_cmd(
        f"git diff-tree --no-commit-id --name-only -r {commit_hash}",
        cwd=repo_path,
    ).splitlines()

    print("Reapplying files from old commit:")
    for f in changed_files:
        print(" -", f)
        run_cmd(f"git checkout {commit_hash} -- {f}", cwd=repo_path)


def run(lib_path):
    print("The attacker has obtained credentials that grant commit and push access to the authentication repository.")
    print("They have not compromised any metadata signing keys.")
    print("They reapply metadata from a previous commit in an attempt to make users accept an older repository state as current.\n")

    auth_repo_path = Path(lib_path, "attacker", AUTH_REPO_NAME)
    auth_repo = AuthenticationRepository(path=auth_repo_path)
    old_commit = auth_repo.commit_before_commit(auth_repo.head_commit())
    create_rollback_commit(auth_repo_path, old_commit.hash)
    auth_repo.commit("Reapplying old metadata")
    auth_repo.push(no_verify=True)
