import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository

REPO_ROOT = "../workspaces/scenario1"
USER_DIR = os.path.join(REPO_ROOT, "user")


def run():
    print("Running user scenario logic...")

    namespace = find_namespace(USER_DIR)
    user_repo_path = Path(USER_DIR, namespace, "law")
    user_repo = AuthenticationRepository(path=user_repo_path)

    run_updater(user_repo)

    print("User scenario complete.")

