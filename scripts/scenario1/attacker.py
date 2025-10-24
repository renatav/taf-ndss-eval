import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import commit_and_push, find_namespace, push_with_upstream, run, update_target_repo

REPO_ROOT = "../repositories"
ATTACKER_DIR = os.path.join(REPO_ROOT, "attacker")
REPO_NAME = "law-html"


def main():
    print("Running attacker scenario logic...")

    namespace = find_namespace(ATTACKER_DIR)
    repo_path = os.path.join(ATTACKER_DIR, namespace, REPO_NAME)

    update_target_repo(repo_path)

    commit_and_push(repo_path, "bad stuff", set_upstream=True)

    print("=== Malicious push complete ===")

if __name__ == "__main__":
    main()
