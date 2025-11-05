import os
from pathlib import Path
import sys
from taf.auth_repo import AuthenticationRepository

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from taf.api.roles import _load_pub_key_from_file
from taf.keys import _load_signer_from_keystore


REPO_NAME = "cityofsanmateo/law-html"
AUTH_REPO_NAME = "cityofsanmateo/law"
KEYSTORE_PATH = Path("../keystore")


def run(lib_path):
    print("The attacker has obtained credentials that grant commit and push access to the authentication repository.")
    print("They have also compromised the snapshot and timestamp keys (these roles have a signing threshold of 1) and one root key.")
    print("They add their own targets signing key, and use the compromised keys to sign root, snapshot, and timestamp metadata.")

    auth_repo_path = Path(lib_path, "attacker", AUTH_REPO_NAME)
    auth_repo = AuthenticationRepository(path=auth_repo_path)

    pub_key_path = Path(KEYSTORE_PATH, "targets_attacker.pub")
    pub_key = _load_pub_key_from_file(pub_key_path, prompt_for_keys=False, scheme="rsa-pkcs1v15-sha256")

    roles_keys = {"targets": [pub_key]}

    pub_key = _load_pub_key_from_file(pub_key_path, prompt_for_keys=False, scheme="rsa-pkcs1v15-sha256")
    signer = _load_signer_from_keystore(
        auth_repo, KEYSTORE_PATH, "root1", 1, "rsa-pkcs1v15-sha256", "root"
    )
    auth_repo.add_signers_to_cache({"root": [signer]})

    for role in ("snapshot", "timestamp"):
        signer = _load_signer_from_keystore(
            auth_repo, KEYSTORE_PATH, role, 1, "rsa-pkcs1v15-sha256", role
        )
        auth_repo.add_signers_to_cache({role: [signer]})

    auth_repo.add_metadata_keys(
        roles_keys
    )
    auth_repo.update_snapshot_and_timestamp()

    auth_repo.commit("Add attackers signing key")
    auth_repo.push(no_verify=True)
