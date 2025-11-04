import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository


REPO_NAME = "cityofsanmateo/law"


def run(lib_path):
    print("The user/publisher runs the updater with default settings.")
    print("The updater detects that the remote authentication repository's top commit is not present locally and halts the update.")

    repo_path = Path(lib_path, "user", REPO_NAME)
    user_repo = AuthenticationRepository(path=repo_path)

    run_updater(user_repo)
