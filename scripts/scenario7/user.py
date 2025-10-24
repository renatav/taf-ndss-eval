import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import commit, find_namespace, run, update_target_repo

REPO_ROOT = "../repositories"
USER_DIR = os.path.join(REPO_ROOT, "user")
REPO_NAME = "law-html"

def main():
    print("Running user scenario logic...")

    namespace = find_namespace(USER_DIR)
    user_repo_path = os.path.join(USER_DIR, namespace, "law")

    readme_path = os.path.join(user_repo_path, "README.md")
    with open(readme_path, "a") as f:
        f.write("accidental\n")

    # Run updater
    run(["taf", "repo", "update", "--force", "-v"], cwd=user_repo_path)

    print("User scenario complete.")

if __name__ == "__main__":
    main()
