import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, update_target_repo
from taf.git import GitRepository

REPO_NAME = "cityofsanmateo/law-html"


def run(lib_path):
    print("The attacker has obtained credentials that allow commit and push access to a target repository.")
    print("They cannot modify the authentication repository.")
    print("They now alter law-html and push a malicious update.\n")

    repo_path = Path(lib_path, "attacker", REPO_NAME)
    target_repo = GitRepository(path=repo_path)
    update_target_repo(target_repo)
