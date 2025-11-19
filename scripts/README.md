# Repository Security Scenarios

This artifact provides seven reproducible scenarios that demonstrate how the update validation logic protects against repository compromise and metadata manipulation.

To run these scenarios, navigate to the `scripts` directory and run:

```
python run.py --scenario <number>
```

To see an overview of the scenarios, run:

```
python run.py --list
```

Each scenario automatically sets up fresh repositories and simulates attacker, user, and, if relevant, publisher actions.
**User** refers to any person or entity with an interest in having local copies of legal repositories. They are not responsible for updating them or acting in case of compromises.
**Publisher** is an actor with those responsibilities.

After executing each actor's scenario, the script pauses, allowing inspection of the current state of the relevant actor's repositories.


The shared origin repositories are cloned from a reference copy included in this artifact (under `repositories/cityofsanmateo/`) into a new timestamped directory:
`repositories/origin/scenario<N>_<timestamp>/`. These are bare Git repositories simulating a hosting platform. From these origin repositories, the script clones working copies for each actor (`attacker`, `user`, and `publisher`) under `workspaces/scenario<N>_<timestamp>/<actor>`.
The `<timestamp>` ensures uniqueness on each run (e.g., `scenario7_20251105_003627`) and helps avoid permission-related cleanup issues on some systems.

All of these repositories are regular Git repositories and can be inspected with any tool (e.g., `git gui`, `tig`, or the command line).
Both the origin repositories and the actor workspaces are regenerated on every scenario run, ensuring full reproducibility and isolation across runs.


## Overview

Scenarios 1–6 simulate attacks without compromising any metadata signing keys.
They explore what an attacker can do with just repository access (e.g., compromising a publisher’s machine or GitHub/GitLab account), and how validation logic and signed metadata block those malicious attempts. When signing keys are stored on hardware devices, such remote compromises do not grant access to those keys.

Scenario 7 introduces partial key compromise, illustrating how signature thresholds maintain trust.

Together, the scenarios show that:

- Unauthorized repository updates are insufficient to deceive clients.
- Unsigned, outdated, or rollback metadata is detected and rejected.
- Rollback and replay attacks are prevented through version checks.
- Even partial key compromise cannot bypass threshold signing requirements.


**Note:**

We do not include scenarios where attackers use valid snapshot and timestamp keys to set the current version to an older value (e.g., attempting a replay attack). This leads to the same end state as rewriting Git history or reapplying older commits. Likewise, if an attacker compromises a threshold of targets keys in addition to timestamp and snapshot, TAF cannot flag this as an invalid update. These risks are inherited from TUF and are not specific to TAF. For stronger guarantees, deployments should rely on archival redundancy and inter-institutional verification.

---
## Scenario Descriptions

This artifact provides seven reproducible scenarios that demonstrate how the update validation logic protects against repository compromise and metadata manipulation.

---

### Scenario 1: Malicious Update to Target Repository Only

An attacker compromises the credentials of a target repository, gaining commit and push access but not control over the authentication repository. They push a malicious update to `law-html`.

When the user runs the updater with default settings, no new commits are fetched because the authentication repository remains unchanged. The publisher runs the updater with a full check and detects the malicious commit, receiving a validation error.

---

### Scenario 2: Malicious Commit + Authentication Repo Modified (No Signatures)

An attacker obtains credentials that allow commit and push access to both a target and the authentication repository, but does not have access to any metadata signing keys.
The attacker modifies `law-html` and pushes a malicious update, then manually updates the file recording the last valid commit for that target repository in the authentication repository and pushes the change.
They do not update or sign the corresponding TUF metadata.

When the user or publisher later runs the updater, it detects that the authentication repository has changed and fetches the new metadata. Validation fails because the updates are unsigned, and the user's local repository remains unchanged.

---

### Scenario 3: Malicious Commit + Metadata Modified (Unsigned)

An attacker obtains credentials that grant commit and push access to both the target and authentication repositories, but has not compromised any metadata signing keys.
The attacker modifies `law-html` and pushes a malicious update. They then update the file recording the last valid commit for that target and correctly update the TUF metadata (the attacker is familiar with TUF), but cannot produce valid signatures of those updates.
The attacker pushes these unsigned changes to the authentication repository.

When the user or publisher runs the updater with default settings, the updater detects the authentication repository update and fetches the incoming changes for validation. Validation fails because the metadata updates are unsigned, and the user's local repository remains unchanged.

---

### Scenario 4: Repository Rollback via Force Push

An attacker obtains credentials that grant commit and push access to both the target and authentication repositories, but does not possess any metadata signing keys.
The attacker reverts all repositories to a previous commit and force-pushes the branches, attempting to make an outdated version appear current.

When the user or publisher runs the updater with default settings, the updater detects that the top commit of the remote authentication repository is not present in the local history and halts the update.
This prevents the rollback attack from being accepted as a valid state.

---

### Scenario 5: Metadata Reuse from Older Signed Commit

The attacker gains push access to the authentication repository but does not have access to any metadata signing keys.
Instead of creating new unsigned metadata, the attacker restores metadata from a previous commit that still contains valid signatures, attempting to make an older repository state appear current.

When the user or publisher runs the updater with default settings, the updater detects that the fetched metadata has a lower version number than the previously validated metadata.
The update is rejected, and the rollback to an older repository state is successfully prevented.

---

### Scenario 6: Publisher Pulls Invalid Update, Then Publishes Signed Metadata

An attacker pushes a malicious but invalid update, similar to the one in Scenario 2.
The publisher, without using TAF for validation, recklessly pulls these changes and subsequently creates and pushes a new valid, signed update.

When the user later runs the updater with default settings, the updater detects the new commits and begins validation from the oldest one.
Because validation fails on the earlier invalid commit, the process halts even though the newest commit is valid.

---

### Scenario 7: Compromised Snapshot + Timestamp Keys and Partial Root

The attacker gains commit and push access to the authentication repository and compromises the snapshot and timestamp keys, both of which have a signing threshold of 1, as well as one of the root keys.
They add their own targets signing key and use the compromised root key to sign the root, snapshot, and timestamp metadata. Root, however, has a signing threshold greater than one.

When the user runs the updater with default settings, validation fails because the root metadata is signed with only one key.
This prevents the partially compromised root from being accepted and blocks the malicious update.
