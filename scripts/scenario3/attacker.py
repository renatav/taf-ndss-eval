import json
import os
from pathlib import Path
import sys
from taf.tuf.repository import MetadataRepository
from taf.git import GitRepository
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.shared import update_commit_in_target_file, update_target_metadata, update_target_repo

REPO_NAME = "cityofsanmateo/law-html"
AUTH_REPO_NAME = "cityofsanmateo/law"


def update_snapshot_metadata(auth_repo_path, file_versions):
    snapshot_path = Path(auth_repo_path, "metadata", "snapshot.json")
    snapshot = json.loads(snapshot_path.read_text())

    for filename, new_version in file_versions.items():
        if filename in snapshot["signed"]["meta"]:
            snapshot["signed"]["meta"][filename]["version"] = new_version
        else:
            snapshot["signed"]["meta"][filename] = {"version": new_version}

    # Optionally increment snapshot version too
    version = snapshot["signed"]["version"]
    snapshot["signed"]["version"] = version + 1

    snapshot_path.write_text(json.dumps(snapshot, indent=2))

    print("Snapshot metadata updated (unsigned).")
    return version


def update_timestamp_metadata(auth_repo_path, snapshot_version):
    print(f"Updating timestamp metadata to reflect snapshot version {snapshot_version}")

    timestamp_path = Path(auth_repo_path, "metadata", "timestamp.json")
    timestamp = json.loads(timestamp_path.read_text())

    timestamp["signed"]["meta"]["snapshot.json"]["version"] = snapshot_version

    repo = MetadataRepository(auth_repo_path)
    md = repo.open("snapshot")
    length = repo.calculate_length(md)
    hashes = repo.calculate_hashes(md, ["sha256", "sha512"])

    timestamp["signed"]["meta"]["snapshot.json"]["length"] = length
    timestamp["signed"]["meta"]["snapshot.json"]["hashes"] = hashes

    # You can optionally increment timestamp version if needed
    timestamp["signed"]["version"] += 1

    timestamp_path.write_text(json.dumps(timestamp, indent=2))

    print("Timestamp metadata updated (unsigned).")


def run(lib_path):
    print("The attacker has obtained credentials that grant commit and push access to both the target and authentication repositories.")
    print("They have not compromised any metadata signing keys.")
    print("They modify law-xml and push a malicious update.\n")
    print("The attacker then manually updates the file that records the last valid commit for that target.")
    print("They update the TUF metadata correctly (the attacker is familiar with TUF), but they cannot produce valid signatures of the metadata files")
    print("They push the changes\n")

    target_repo_path = Path(lib_path, "attacker", REPO_NAME)
    target_repo = GitRepository(path=target_repo_path)
    auth_repo_path = Path(lib_path, "attacker", AUTH_REPO_NAME)
    print()
    target_commit = update_target_repo(target_repo)
    auth_repo = AuthenticationRepository(path=auth_repo_path)

    target_file_path = auth_repo_path / "targets" / REPO_NAME

    update_commit_in_target_file(target_file_path, target_commit)
    version = update_target_metadata(auth_repo_path, REPO_NAME)
    version = update_snapshot_metadata(auth_repo_path, {"targets.json": version})
    update_timestamp_metadata(auth_repo_path, version)
    auth_repo.commit("Update target commit and metadata without signing")
    auth_repo.push(no_verify=True)
