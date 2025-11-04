import json
import os
from pathlib import Path
import shutil
import stat
import sys
from taf.tuf.repository import MetadataRepository
from taf.updater.updater import update_repository, UpdateConfig
from taf.updater.types.update import OperationType
from taf.utils import run


def find_namespace(dir_path):
    for entry in os.listdir(dir_path):
        path = os.path.join(dir_path, entry)
        if os.path.isdir(path):
            return entry
    print("ERROR: No namespace directory found in attacker/")
    sys.exit(1)


def ensure_exists(path, label):
    if not os.path.exists(path):
        print(f"ERROR: {label} does not exist. Please run init first.")
        sys.exit(1)

def copy_dir(src, dest):
    print(f"Restoring {dest} from {src}...")
    shutil.copytree(src, dest)


def delete_dir(path):
    if path.is_dir():
        print(f"Removing {path}...")
        shutil.rmtree(path, onerror=on_rm_error)


def on_rm_error(_func, path, _exc_info):
    """Used by when calling rmtree to ensure that readonly files and folders
    are deleted.
    """
    try:
        os.chmod(path, stat.S_IWRITE)
    except OSError as e:
        return
    try:
        os.unlink(path)
    except (OSError, PermissionError) as e:
        pass


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

