import os
import shutil
import subprocess
import sys

# Repository config
REPO_NAMESPACE = "mohicanlaw"
REPO_NAME = "law"
FULL_NAME = f"{REPO_NAMESPACE}/{REPO_NAME}"
REMOTE_URL = f"https://github.com/oll-test-repos/{REPO_NAMESPACE}-{REPO_NAME}"

# Base working dir
REPO_ROOT = "repositories"
ORIGIN_BARE = os.path.join(REPO_ROOT, "origin-bare")
ORIGIN_FULL = os.path.join(REPO_ROOT, "origin-full")

def run(cmd, cwd=None):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main():
    # Create base dir
    if not os.path.exists(REPO_ROOT):
        os.makedirs(REPO_ROOT)

    # Safety checks
    if os.path.exists(ORIGIN_BARE):
        print("ERROR: The 'origin-bare' directory already exists. Please remove or rename it.")
        sys.exit(1)
    if os.path.exists(ORIGIN_FULL):
        print("ERROR: The 'origin-full' directory already exists. Please remove or rename it.")
        sys.exit(1)

    os.makedirs(ORIGIN_BARE)
    os.makedirs(ORIGIN_FULL)

    # Clone into origin-bare
    run(["taf", "repo", "clone", "--bare", REMOTE_URL], cwd=ORIGIN_BARE)

    # Clone into origin-full
    run(["taf", "repo", "clone", REMOTE_URL], cwd=ORIGIN_FULL)

    print("=== Init done ===")

if __name__ == "__main__":
    main()
