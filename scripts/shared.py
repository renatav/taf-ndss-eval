import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from taf.tuf.repository import MetadataRepository
from taf.updater.updater import update_repository, UpdateConfig
from taf.updater.types.update import OperationType
from taf.utils import run

def commit(repo_path, commit_msg):
    run(["git", "add", "-A"], cwd=repo_path)
    run(["git", "commit", "-m", commit_msg], cwd=repo_path, capture=True)


def push_no_verify(repo):
    run("git push --no-verify", cwd=repo.path)
    print(f"Repo {repo.name}: Successfully pushed to remote")


def find_namespace(dir_path):
    for entry in os.listdir(dir_path):
        path = os.path.join(dir_path, entry)
        if os.path.isdir(path):
            return entry
    print("ERROR: No namespace directory found in attacker/")
    sys.exit(1)


def get_current_branch(repo_path):
    return run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo_path,
        capture=True
    )

def push_with_upstream(repo_path, bypass_hook=False):
    branch = get_current_branch(repo_path)
    print(f"Pushing branch '{branch}' with upstream set")
    cmd = ["git", "push", "--set-upstream", "origin", branch]
    if bypass_hook:
        cmd.append("--no-verify")
    run(cmd, cwd=repo_path)

def ensure_exists(path, label):
    if not os.path.exists(path):
        print(f"ERROR: {label} does not exist. Please run init first.")
        sys.exit(1)

def copy_dir(src, dest):
    print(f"Restoring {dest} from {src}...")
    shutil.copytree(src, dest)

def delete_dir(path):
    if os.path.exists(path):
        print(f"Removing {path}...")
        shutil.rmtree(path)


def run_updater(auth_repo, no_upstream=True):
    config = UpdateConfig(
        operation=OperationType.UPDATE,
        path=auth_repo.path,
        update_from_filesystem=True,
        no_upstream=no_upstream,
        strict=True,
    )
    try:
        update_repository(config)
    except Exception as e:
        pass


def get_head_commit(repo_path):
    """Get the HEAD commit hash of a Git repo"""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def update_commit_in_target_file(target_file_path: Path, new_commit_hash):
    """Overwrite the 'commit' key in the metadata JSON file"""
    print(f"Modifying metadata at {target_file_path} with commit {new_commit_hash}")
    data = json.loads(target_file_path.read_text())
    data["commit"] = str(new_commit_hash)
    target_file_path.write_text(json.dumps(data))
    print("Metadata modified.")


def update_target_repo(target_repo):
    """
    Update a file in the target repository and commit, simulating an attackers
    attemps at a malicious update
    """
    # Simulate malicious commit
    readme_path = target_repo.path / "README.md"
    readme_path.write_text("malicious\n")
    commit = target_repo.commit("malicious update")
    print(f"Modifying {readme_path} and committing.")
    target_repo.push()
    return commit


def compute_hashes_and_length(repo_path, target_file_path):

    repo = MetadataRepository(repo_path)
    target = repo._create_target_object(target_file_path, target_file_path, None)
    return {
        "hashes": target.hashes,
        "length": target.length
    }


def update_target_metadata(repo_path, target_name):
    print(f"Updating metadata for target: {target_name}")

    meta = compute_hashes_and_length(repo_path, os.path.join(repo_path, "targets", target_name))

    targets_json_path = os.path.join(repo_path, "metadata", "targets.json")
    with open(targets_json_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    metadata["signed"]["targets"][target_name] = meta
    version =  metadata["signed"]["version"]
    metadata["signed"]["version"] = version + 1

    with open(targets_json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return version

def force_remove_last_n_commits(repo_path, n):
    # Reset hard to that commit
    run(['git', 'reset', '--hard', f"HEAD~{n}"], cwd=repo_path)

    # Force push to remote
    run(['git', 'push', "--force", "--no-verify"], cwd=repo_path)

