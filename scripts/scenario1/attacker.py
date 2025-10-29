import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import commit_and_push, find_namespace, push_with_upstream, run, update_target_repo
from taf.git import GitRepository

REPO_ROOT = "../workspaces/scenario1"
ATTACKER_DIR = os.path.join(REPO_ROOT, "attacker")
REPO_NAME = "law-xml"


def run():
    print("=== Running attacker scenario===")
    print("An attacker has gained access to a target repository and can commit and push, but cannot update the authentication repository")
    print("They make a modification to law-xml and push that change")

    namespace = find_namespace(ATTACKER_DIR)
    repo_path = Path(ATTACKER_DIR, namespace)
    target_repo = GitRepository(path=repo_path)

    update_target_repo(target_repo)

    print("=== Malicious push complete ===")
