import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import run_updater
from taf.auth_repo import AuthenticationRepository


REPO_NAME = "cityofsanmateo/law"

def run(lib_path):
    print("The user/publisher runs the updater with default settings.")
    print("The updater detects that the authentication repository has been updated and fetches the incoming changes for validation.")
    print("Validation fails because the target file containing the new commit is invalid according to TUF metadata.")
    print("The user's local repository remains unchanged.\n")

    repo_path = Path(lib_path, "user", REPO_NAME)
    user_repo = AuthenticationRepository(path=repo_path)

    run_updater(user_repo)
