import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository

REPO_ROOT = "../workspaces/scenario6"
USER_DIR = Path(REPO_ROOT, "user")


def run():
    print("The user runs the updater with default settings.")
    print("The updater detects new commits and begins validation from the oldest one.")
    print("Validation fails, even though the newest commit is valid.")

    namespace = find_namespace(USER_DIR)
    user_repo_path = Path(USER_DIR, namespace, "law")
    user_repo = AuthenticationRepository(path=user_repo_path)

    run_updater(user_repo)
