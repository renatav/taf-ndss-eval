import os
from pathlib import Path
import sys
from typing import List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.shared import copy_dir, delete_dir, ensure_exists, rewire_remote
from taf.git import GitRepository
from taf.updater.updater import clone_repository, UpdateConfig
from taf.updater.types.update import OperationType

REPO_ROOT = Path("../repositories")
ORIGIN_DIR = REPO_ROOT / "origin"
WORKSPACES_DIR = Path("../workspaces")
NAMESPACE = f"cityofsanmateo"


def setup_scenario(scenario_num: int, actors: Optional[List]=None):
    print("=== Starting scenario ===")

    if actors is None:
        actos = ["user", "attacker", "publisher"]

    # initialize origin
    for repo_name in (f"{NAMESPACE}/law", f"{NAMESPACE}/law-xml"):
        repo_path = REPO_ROOT / repo_name
        git_dir = repo_path / "git"
        if git_dir.is_dir():
            new_dir = git_dir.with_name(".git")
            git_dir.rename(new_dir)

        origin_repo_path = ORIGIN_DIR / repo_name
        origin_repo = GitRepository(path=origin_repo_path)
        if origin_repo_path.is_dir():
            delete_dir(origin_repo_path)
        origin_repo.clone_from_disk(repo_path, is_bare=True)


    scenario_dir = WORKSPACES_DIR / f"scenario{scenario_num}"
    if not scenario_dir.is_dir():
        scenario_dir.mkdir(parents=True)

    for actor in actos:
        actor_dir = scenario_dir / actor
        # clean if already exists
        if actor_dir.is_dir():
            delete_dir(actor_dir)
            actor_dir.mkdir()

        config = UpdateConfig(
            operation=OperationType.CLONE,
            remote_url=str((ORIGIN_DIR / f"{NAMESPACE}/law").resolve().absolute()),
            path=str(actor_dir / f"{NAMESPACE}/law"),
            update_from_filesystem=True,
        )

        clone_repository(config)

    print("=== Scenario setup complete ===")


