import os
from pathlib import Path
import sys
from typing import List, Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from taf.git import GitRepository


REPO_ROOT = Path("../repositories")
ORIGIN_DIR = REPO_ROOT / "origin"
WORKSPACES_DIR = Path("../workspaces")
NAMESPACE = f"cityofsanmateo"
repos = (f"{NAMESPACE}/law", f"{NAMESPACE}/law-xml", f"{NAMESPACE}/law-xml-codified", f"{NAMESPACE}/law-html")


def setup_scenario(origin_path: Path, workspace_path, actors: Optional[List]=None):
    print("\n=== Starting scenario ===\n")

    if actors is None:
        actos = ["user", "attacker", "publisher"]

    origin_path.mkdir(parents=True)
    workspace_path.mkdir(parents=True)

    # initialize origin
    for repo_name in repos:
        repo_path = REPO_ROOT / repo_name
        git_dir = repo_path / "git"
        if git_dir.is_dir():
            new_dir = git_dir.with_name(".git")
            git_dir.rename(new_dir)

        origin_repo_path = origin_path / repo_name
        origin_repo = GitRepository(path=origin_repo_path)
        origin_repo.clone_from_disk(repo_path, is_bare=True)


        for actor in actos:
            actor_dir = workspace_path / actor / repo_name
            actor_repo = GitRepository(path=actor_dir)
            actor_repo.clone_from_disk(origin_repo_path, keep_remote=True)

        # config = UpdateConfig(
        #     library_dir = workspace_path,
        #     remote_url=str((origin_path / f"{NAMESPACE}/law").resolve().absolute()),
        #     path=str(actor_dir / f"{NAMESPACE}/law"),
        #     update_from_filesystem=True,
        # )

        # clone_repository(config)

    print("\n=== Scenario setup complete ===\n")
