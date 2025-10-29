import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository

REPO_ROOT = "../workspaces/scenario1"
PUBLISHER_DIR = Path(REPO_ROOT, "publisher")


def run():
    print("The publisher runs the updater with a flag that checks for all updates.")
    print("Even though the authentication repository was not updated, the malicious target commit is detected.")
    print("The publisher is informed that a validation issue has occurred.\n")

    namespace = find_namespace(PUBLISHER_DIR)
    publisher_repo_path = Path(PUBLISHER_DIR, namespace, "law")
    publisher_repo = AuthenticationRepository(path=publisher_repo_path)

    run_updater(publisher_repo, no_upstream=False)
