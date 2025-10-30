import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository

REPO_ROOT = "../workspaces/scenario2"
USER_DIR = Path(REPO_ROOT, "user")


def run():
    print("The user runs the updater with default settings.")
    print("The updater detects that the authentication repository has been updated and fetches the incoming changes for validation.")
    print("Validation fails because the target file containing the new commit is invalid according to TUF metadata.")
    print("The user's local repository remains unchanged.\n")

    namespace = find_namespace(USER_DIR)
    user_repo_path = Path(USER_DIR, namespace, "law")
    user_repo = AuthenticationRepository(path=user_repo_path)

    run_updater(user_repo)
