import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.shared import commit_and_push, find_namespace, run


REPO_ROOT = "../repositories"
ATTACKER_DIR = os.path.join(REPO_ROOT, "attacker")

def find_old_commit(repo_path):
    # Find an old commit that touched the snapshot.json file
    cmd = ["git", "log", "--pretty=format:%H", "--", f"metadata/assets.json"]
    commits = run(cmd, cwd=repo_path, capture=True).splitlines()
    if not commits:
        raise Exception("No matching commits found.")
    return commits[1]

def create_rollback_commit(repo_path, commit_hash):
    # Checkout latest

    # Get list of all files changed in the old commit
    changed_files = run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash],
        cwd=repo_path,
        capture=True
    ).splitlines()


    print("Reapplying files from old commit:")
    for f in changed_files:
        print(" -", f)
        run(["git", "checkout", commit_hash, "--", f], cwd=repo_path)


def main():
    print("Running attacker scenario logic...")

    namespace = find_namespace(ATTACKER_DIR)

    auth_repo_path = os.path.join(ATTACKER_DIR, namespace, "law")
    commit = find_old_commit(auth_repo_path)
    create_rollback_commit(auth_repo_path, commit)
    commit_and_push(auth_repo_path, "Reapplying old snapshot metadata", set_upstream=True, bypass_hook=True)

    print("=== Malicious push complete ===")

if __name__ == "__main__":
    main()
