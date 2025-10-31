import os
from pathlib import Path
import sys
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace
from taf.api.metadata import update_metadata_expiration_date

REPO_ROOT = "../workspaces/scenario6"
PUBLISHER_DIR = Path(REPO_ROOT, "publisher")


def run():
    print("The publisher recklessly pulls changes without using TAF for validation.")
    print("They then create and push a new valid, signed update.")

    namespace = find_namespace(PUBLISHER_DIR)
    auth_repo_path = Path(PUBLISHER_DIR, namespace, "law")
    auth_repo = AuthenticationRepository(path=auth_repo_path)
    auth_repo.pull()

    update_metadata_expiration_date(str(auth_repo_path), None, roles=["timestamp"], interval=1, keystore="../keystore", push=False)
    auth_repo.push(no_verify=True)
