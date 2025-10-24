import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import commit_and_push, find_namespace, force_remove_last_n_commits, push_with_upstream, run, update_commit_in_target_file, update_target_repo

REPO_ROOT = "../repositories"
ATTACKER_DIR = os.path.join(REPO_ROOT, "attacker")

def reset_repos_to_target_commits(auth_repo_path, namespace):
    targets_dir = os.path.join(auth_repo_path, "targets", namespace)


    commit_map = {}

    print(targets_dir)
    for filename in os.listdir(targets_dir):
        path = os.path.join(targets_dir, filename)
        with open(path, 'r') as f:
            data = json.load(f)
            commit = data.get("commit")
            if commit:
                commit_map[filename] = commit

    for repo_name, commit in commit_map.items():
        repo_path = os.path.join(ATTACKER_DIR, namespace, repo_name)
        if not os.path.isdir(repo_path):
            print(f"Skipping {repo_name}: repo not found at {repo_path}")
            continue

        print(f"\n== Resetting {namespace}/{repo_name} to {commit} ==")
        try:
            run(['git', 'fetch'], cwd=repo_path)
            run(['git', 'reset', '--hard', commit], cwd=repo_path)
            # Get the current branch
            branch = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=repo_path)
            run(['git', 'push', 'origin', f'+HEAD:{branch}'], cwd=repo_path)
        except RuntimeError as e:
            print(f"Error processing {repo_name}: {e}")


def main():
    print("Running attacker scenario logic...")

    namespace = find_namespace(ATTACKER_DIR)

    auth_repo_path = os.path.join(ATTACKER_DIR, namespace, "law")
    force_remove_last_n_commits(auth_repo_path, 20)
    reset_repos_to_target_commits(auth_repo_path, namespace)


    print("=== Malicious push complete ===")

if __name__ == "__main__":
    main()
