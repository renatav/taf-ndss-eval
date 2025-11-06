import json
from pathlib import Path
import subprocess
import sys
import os
from taf.git import GitRepository


def run(cmd, cwd=None):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

# Get total number of commits (on current branch)
def get_total_commits(org, repo):
    result = subprocess.run(["git", "-C", f"{org}/{repo}", "rev-list", "--count", "HEAD"], capture_output=True, text=True, check=True)
    return int(result.stdout.strip())

# Read previous commit count from file
def read_previous_commit_count(file_path):
    path = Path(file_path)
    if path.exists():
        with path.open() as f:
            return int(f.read().strip())
    else:
        return 0


def main():
    orgs = ["cityofsanmateo", "mohicanlaw", "sanipueblo", "tmchippewa"]
    repos = [
        "law",
        "law-xml",
        "law-xml-codified",
        "law-html",
        "law-static-assets",
        "law-rdf",
        "law-docs",
    ]

    for org in orgs:
        for repo in repos:
            # if already on disk skip
            if os.path.exists(os.path.join(org, repo)):
                print(f"Skipping {org}/{repo}, already cloned.")
                continue


            print(f"=== Cloning {org}/{repo} === This may take a while...")
            try:
                run(
                    [
                        "git",
                        "clone",
                        f"https://github.com/{org}/{repo}.git",
                        os.path.join(org, repo),
                    ]
                )

                if repo == "law":
                    repo_commit_count = get_total_commits(org, repo)
                    prev_commit_count = read_previous_commit_count(Path(org, "commits"))
                    difference = repo_commit_count - prev_commit_count
                    auth_repo = GitRepository(path=os.path.join(org, repo))
                    auth_repo.reset_num_of_commits(difference, hard=True)
                else:
                    repo_path = Path(org, repo)
                    target_repo = GitRepository(path=repo_path)
                    target_file_path = Path(org, "law", "targets", org, repo)
                    target_metadata = json.loads(target_file_path.read_text())
                    branch = target_metadata.get("branch", target_repo.get_default_branch())
                    commit = target_metadata["commit"]
                    target_repo.checkout_branch(branch)
                    target_repo.reset_to_commit(commit, branch, hard=True)

            except Exception as e:
                print(f"Failed to clone {org}/{repo}: {e}")

    import pdb; pdb.set_trace()
if __name__ == "__main__":
    main()
