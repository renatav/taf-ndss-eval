import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import find_namespace, run

REPO_ROOT = "../repositories"
USER_DIR = os.path.join(REPO_ROOT, "user")


def main():
    print("Running user scenario logic...")

    # Find namespace folder inside user/
    if not os.path.exists(USER_DIR):
        print(f"ERROR: Directory not found: {USER_DIR}")
        sys.exit(1)

    namespace = find_namespace(USER_DIR)
    user_repo_path = os.path.join(USER_DIR, namespace)

    # Run updater
    run(["taf", "repo", "update", "--upstream"], cwd=user_repo_path)

    print("User scenario complete.")

if __name__ == "__main__":
    main()
