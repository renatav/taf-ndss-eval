import hashlib
import json
import os
import shutil
import subprocess
import sys
from taf.tuf.repository import MetadataRepository


def run(cmd, cwd=None, capture=False):
    print(f"$ {' '.join(cmd)} (in {cwd or os.getcwd()})")

    if capture:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True
        )
    else:
        result = subprocess.run(cmd, cwd=cwd, check=True)
    if result.returncode != 0:
        print(f"ERROR: command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    if capture:
        return result.stdout.strip()


def commit(repo_path, commit_msg):
    run(["git", "add", "-A"], cwd=repo_path)
    run(["git", "commit", "-m", commit_msg], cwd=repo_path, capture=True)


def commit_and_push(repo_path, commit_msg, set_upstream=False, bypass_hook=False):
    run(["git", "add", "-A"], cwd=repo_path)

    commit = run(["git", "commit", "-m", commit_msg], cwd=repo_path, capture=True)
    if set_upstream:
        push_with_upstream(repo_path, bypass_hook=bypass_hook)
    else:
        if bypass_hook:
            run(["git", "push", "--no-verify"], cwd=repo_path)
        else:
            run(["git", "push"], cwd=repo_path)


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

def rewire_remote(repo_path, origin_repo_path):
    """Replace the 'origin' remote with a local path"""
    git_path = os.path.join(repo_path, ".git")
    if not os.path.exists(git_path):
        return
    print(f"Rewiring remote in {repo_path} to local origin at {origin_repo_path}")

    # Remove old remote
    subprocess.run(["git", "remote", "remove", "origin"], cwd=repo_path, check=True)

    # Add new local remote
    subprocess.run(["git", "remote", "add", "origin", origin_repo_path], cwd=repo_path, check=True)

def get_head_commit(repo_path):
    """Get the HEAD commit hash of a Git repo"""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()

def update_commit_in_target_file(target_file_path, new_commit_hash):
    """Overwrite the 'commit' key in the metadata JSON file"""
    print(f"Modifying metadata at {target_file_path} with commit {new_commit_hash}")

    with open(target_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "commit" not in data:
        print("WARNING: No 'commit' key found, adding it.")

    data["commit"] = new_commit_hash

    with open(target_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Metadata modified.")


def update_target_repo(target_repo_path):
    if not os.path.exists(target_repo_path):
        raise FileNotFoundError(f"ERROR: Repo path does not exist: {target_repo_path}")

    # Simulate malicious commit
    readme_path = os.path.join(target_repo_path, "README.md")
    with open(readme_path, "a") as f:
        f.write("malicious1\n")

    commit_and_push(target_repo_path, "bad stuff", set_upstream=True)
    commit = get_head_commit(target_repo_path)
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

    targets_json_path = os.path.join(repo_path, "metadata", "law.json")
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

