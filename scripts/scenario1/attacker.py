import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, update_target_repo
from taf.git import GitRepository

REPO_ROOT = "../workspaces/scenario1"
ATTACKER_DIR = Path(REPO_ROOT, "attacker")
REPO_NAME = "law-xml"


def run():
    print("The attacker has obtained credentials that allow commit and push access to the target repository.")
    print("They cannot modify the authentication repository.")
    print("They now alter law-xml and push a malicious update.\n")

    namespace = find_namespace(ATTACKER_DIR)
    repo_path = Path(ATTACKER_DIR, namespace, REPO_NAME)
    target_repo = GitRepository(path=repo_path)
    update_target_repo(target_repo)
