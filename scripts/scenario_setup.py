import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.shared import copy_dir, delete_dir, ensure_exists, rewire_remote

REPO_ROOT = "../repositories"



def main():
    print("=== Starting scenario ===")

    os.chdir(REPO_ROOT)

    # Delete previous runs
    delete_dir("origin")
    delete_dir("user")
    delete_dir("attacker")

    # Ensure backups exist
    ensure_exists("origin-bare", "origin-bare")
    ensure_exists("origin-full", "origin-full")

    # Restore everything
    copy_dir("origin-bare", "origin")
    copy_dir("origin-full", "attacker")
    copy_dir("origin-full", "user")

    # Rewire remote for each namespace/repo pair
    for namespace in os.listdir("origin"):
        origin_ns_path = os.path.join("origin", namespace)
        attacker_ns_path = os.path.join("attacker", namespace)
        user_ns_path = os.path.join("user", namespace)

        if not os.path.isdir(origin_ns_path):
            continue

        for repo in os.listdir(origin_ns_path):
            origin_repo = os.path.abspath(os.path.join(origin_ns_path, repo))

            attacker_repo = os.path.join(attacker_ns_path, repo)
            user_repo = os.path.join(user_ns_path, repo)

            if os.path.isdir(attacker_repo):
                rewire_remote(attacker_repo, origin_repo)

            if os.path.isdir(user_repo):
                rewire_remote(user_repo, origin_repo)

    print("=== Scenario setup complete ===")

if __name__ == "__main__":
    main()
