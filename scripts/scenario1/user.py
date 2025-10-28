import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run as run1

REPO_ROOT = "../workspaces/scenario1"
USER_DIR = os.path.join(REPO_ROOT, "user")


def run():
    print("Running user scenario logic...")

    # Find namespace folder inside user/
    if not os.path.exists(USER_DIR):
        print(f"ERROR: Directory not found: {USER_DIR}")
        sys.exit(1)

    namespace = find_namespace(USER_DIR)
    user_repo_path = os.path.join(USER_DIR, namespace)

    # Run updater
    run1(["taf", "repo", "update"], cwd=user_repo_path)

    print("User scenario complete.")

