import os
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.shared import copy_dir, delete_dir, ensure_exists, rewire_remote
from taf.git import GitRepository
from taf.updater.updater import clone_repository, UpdateConfig
from taf.updater.types.update import OperationType

REPO_ROOT = Path("../repositories")
ORIGIN_DIR = REPO_ROOT / "origin"
WORKSPACES_DIR = Path("../workspaces")


def main():
    print("=== Starting scenario ===")

    # initialize origin if it does not exist
    for repo_name in ("cityofsanmateo/law", "cityofsanmateo/law-xml"):
        repo_path = REPO_ROOT / repo_name
        git_dir = repo_path / "git"
        if git_dir.is_dir():
            new_dir = git_dir.with_name(".git")
            git_dir.rename(new_dir)

        origin_repo_path = ORIGIN_DIR / repo_name
        origin_repo = GitRepository(path=origin_repo_path)
        if not origin_repo.is_git_repository:
            origin_repo.clone_from_disk(repo_path, is_bare=True)

    current_scenario = "scenario1"

    scenario_dir = WORKSPACES_DIR / current_scenario
    if not scenario_dir.is_dir():
        scenario_dir.mkdir(parents=True)

    for actor in ("user", "attacker", "publisher"):
        actor_dir = scenario_dir / actor
        # clean if already exists
        if actor_dir.is_dir():
            delete_dir(actor_dir)
            actor_dir.mkdir()

        config = UpdateConfig(
            operation=OperationType.CLONE,
            remote_url=str((ORIGIN_DIR / "cityofsanmateo/law").resolve().absolute()),
            path=str(actor_dir / "cityofsanmateo/law"),
            update_from_filesystem=True,
        )

        clone_repository(config)

    # os.chdir(REPO_ROOT)

    # # Delete previous runs
    # delete_dir("origin")
    # delete_dir("user")
    # delete_dir("attacker")

    # # Ensure backups exist
    # ensure_exists("origin-bare", "origin-bare")
    # ensure_exists("origin-full", "origin-full")

    # # Restore everything
    # copy_dir("origin-bare", "origin")
    # copy_dir("origin-full", "attacker")
    # copy_dir("origin-full", "user")

    # # Rewire remote for each namespace/repo pair
    # for namespace in os.listdir("origin"):
    #     origin_ns_path = os.path.join("origin", namespace)
    #     attacker_ns_path = os.path.join("attacker", namespace)
    #     user_ns_path = os.path.join("user", namespace)

    #     if not os.path.isdir(origin_ns_path):
    #         continue

    #     for repo in os.listdir(origin_ns_path):
    #         origin_repo = os.path.abspath(os.path.join(origin_ns_path, repo))

    #         attacker_repo = os.path.join(attacker_ns_path, repo)
    #         user_repo = os.path.join(user_ns_path, repo)

    #         if os.path.isdir(attacker_repo):
    #             rewire_remote(attacker_repo, origin_repo)

    #         if os.path.isdir(user_repo):
    #             rewire_remote(user_repo, origin_repo)

    print("=== Scenario setup complete ===")

if __name__ == "__main__":
    main()
