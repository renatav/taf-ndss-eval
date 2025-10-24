import json
import os
import sys
from taf.tuf.repository import MetadataRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import commit_and_push, find_namespace, update_commit_in_target_file, update_target_metadata, update_target_repo

REPO_ROOT = "../repositories"
ATTACKER_DIR = os.path.join(REPO_ROOT, "attacker")
REPO_NAME = "law-html"


def update_snapshot_metadata(auth_repo_path, file_versions):
    snapshot_path = os.path.join(auth_repo_path, "metadata", "snapshot.json")
    with open(snapshot_path, "r", encoding="utf-8") as f:
        snapshot = json.load(f)

    for filename, new_version in file_versions.items():
        if filename in snapshot["signed"]["meta"]:
            snapshot["signed"]["meta"][filename]["version"] = new_version
        else:
            snapshot["signed"]["meta"][filename] = {"version": new_version}

    # Optionally increment snapshot version too
    version = snapshot["signed"]["version"]
    snapshot["signed"]["version"] = version + 1

    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print("Snapshot metadata updated (unsigned).")
    return version


def update_timestamp_metadata(auth_repo_path, snapshot_version):
    print(f"Updating timestamp metadata to reflect snapshot version {snapshot_version}")

    timestamp_path = os.path.join(auth_repo_path, "metadata", "timestamp.json")
    with open(timestamp_path, "r", encoding="utf-8") as f:
        timestamp = json.load(f)

    timestamp["signed"]["meta"]["snapshot.json"]["version"] = snapshot_version

    repo = MetadataRepository(auth_repo_path)
    md = repo.open("snapshot")
    length = repo.calculate_length(md)
    hashes = repo.calculate_hashes(md, ["sha256", "sha512"])

    timestamp["signed"]["meta"]["snapshot.json"]["length"] = length
    timestamp["signed"]["meta"]["snapshot.json"]["hashes"] = hashes

    # You can optionally increment timestamp version if needed
    timestamp["signed"]["version"] += 1

    with open(timestamp_path, "w", encoding="utf-8") as f:
        json.dump(timestamp, f, indent=2)

    print("Timestamp metadata updated (unsigned).")

def main():
    print("Running attacker scenario logic...")

    namespace = find_namespace(ATTACKER_DIR)
    target_repo_path = os.path.join(ATTACKER_DIR, namespace, REPO_NAME)

    auth_repo_path = os.path.join(ATTACKER_DIR, namespace, "law")
    target_file_path = os.path.join(auth_repo_path, "targets", namespace, REPO_NAME)
    commit = update_target_repo(target_repo_path)
    update_commit_in_target_file(target_file_path, commit)
    version = update_target_metadata(auth_repo_path, f"{namespace}/{REPO_NAME}")

    version = update_snapshot_metadata(auth_repo_path, {"law.json": version})
    update_timestamp_metadata(auth_repo_path, version)

    commit_and_push(auth_repo_path, "bad commit", set_upstream=True, bypass_hook=True)

    print("=== Malicious push complete ===")

if __name__ == "__main__":
    main()
