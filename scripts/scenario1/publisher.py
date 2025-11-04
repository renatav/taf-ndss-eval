import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run_updater
from taf.auth_repo import AuthenticationRepository


REPO_NAME = "cityofsanmateo/law"

def run(lib_path):
    print("The publisher runs the updater with a flag that checks for all updates.")
    print("Even though the authentication repository was not updated, the malicious target commit is detected.")
    print("The publisher is informed that a validation issue has occurred.\n")

    repo_path = Path(lib_path, "publisher", REPO_NAME)
    publisher_repo = AuthenticationRepository(path=repo_path)

    run_updater(publisher_repo, no_upstream=False)
