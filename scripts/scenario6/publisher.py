import os
from pathlib import Path
import sys
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from taf.api.metadata import update_metadata_expiration_date


AUTH_REPO_NAME = "cityofsanmateo/law"


def run(lib_path):
    print("The publisher recklessly pulls changes without using TAF for validation.")
    print("They then create and push a new valid, signed update.")

    auth_repo_path = Path(lib_path, "publisher", AUTH_REPO_NAME)
    auth_repo = AuthenticationRepository(path=auth_repo_path)
    auth_repo.pull()

    update_metadata_expiration_date(str(auth_repo_path), None, roles=["timestamp"], interval=1, keystore="../keystore", push=False)
    auth_repo.push(no_verify=True)
