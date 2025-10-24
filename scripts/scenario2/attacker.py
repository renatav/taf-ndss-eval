import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import commit_and_push, find_namespace, push_with_upstream, update_commit_in_target_file, update_target_repo

REPO_ROOT = "../repositories"
ATTACKER_DIR = os.path.join(REPO_ROOT, "attacker")
REPO_NAME = "law-html"


def main():
    print("Running attacker scenario logic...")

    namespace = find_namespace(ATTACKER_DIR)
    target_repo_path = os.path.join(ATTACKER_DIR, namespace, REPO_NAME)

    auth_repo_path = os.path.join(ATTACKER_DIR, namespace, "law")
    target_file_path = os.path.join(auth_repo_path, "targets", namespace, REPO_NAME)
    commit = update_target_repo(target_repo_path)
    update_commit_in_target_file(target_file_path, commit)

    try:
        commit_and_push(auth_repo_path, "update matadata with bad commit", set_upstream=True)
    except subprocess.CalledProcessError:
        pass
    push_with_upstream(auth_repo_path, bypass_hook=True)

    print("=== Malicious push complete ===")

if __name__ == "__main__":
    main()
