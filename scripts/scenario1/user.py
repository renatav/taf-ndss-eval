import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository


REPO_NAME = "cityofsanmateo/law"


def run(lib_path):
    print("The user runs the updater with default settings.")
    print("No new commits are fetched, since the authentication repository has not been updated.")
    print("The user is informed that there are no new updates available.\n")

    repo_path = Path(lib_path, "user", REPO_NAME)
    user_repo = AuthenticationRepository(path=repo_path)
    import pdb; pdb.set_trace()

    run_updater(user_repo)
