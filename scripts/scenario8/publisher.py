import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository

REPO_ROOT = "../workspaces/scenario1"
PUBLISHER_DIR = os.path.join(REPO_ROOT, "publisher")


def run():
    print("Running publisher scenario logic...")

    namespace = find_namespace(PUBLISHER_DIR)
    publisher_repo_path = Path(PUBLISHER_DIR, namespace, "law")
    publisher_repo = AuthenticationRepository(path=publisher_repo_path)

    run_updater(publisher_repo, no_upstream=False)

    print("Publisher scenario complete.")

