import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository

REPO_ROOT = "../workspaces/scenario5"
USER_DIR = Path(REPO_ROOT, "user")


def run():
    print("The user/publisher runs the updater with default settings.")
    print("The updater detects that the fetched commits contain metadata with a version number lower than that of the previous commit.")
    print("The update is rejected and rollback to an older repository state is prevented.\n")

    namespace = find_namespace(USER_DIR)
    user_repo_path = Path(USER_DIR, namespace, "law")
    user_repo = AuthenticationRepository(path=user_repo_path)

    run_updater(user_repo)
