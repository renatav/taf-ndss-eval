# TAF Evaluation

This document accompanies the TAF evaluation artifacts submitted for review. It provides a reproducible framework for verifying both the security and performance aspects of TAF's repository validation system. The first section demonstrates security guarantees through controlled attack scenarios, while the second presents profiling results that assess TAF’s performance under realistic workloads.

## Repository Security Scenarios

This artifact provides seven reproducible scenarios that demonstrate how the update validation logic protects against repository compromise and metadata manipulation.

To run these scenarios, navigate to the `scripts` directory and run:

```
python run.py --scenario <number>
```

To see an overview of the scenarios, run:

```
python run.py list
```

Each scenario automatically sets up fresh repositories and simulates attacker, user, and, if relevant, publisher actions.
**User** refers to any person or entity with an interest in having local copies of legal repositories. They are not responsible for updating them or acting in case of compromises.
**Publisher** is an actor with those responsibilities.

After executing each actor's scenario, the script pauses, allowing inspection of the current state of the relevant actor's repositories.
The shared origin repositories can be found in `repositories/origin`. These are bare repositories simulating a hosting platform.
At the start of each scenario, these repositories are cloned for each actor, creating their local copies under:

```
workspaces/scenario<N>/<actor>/
```

All of these repositories are regular Git repositories and can be inspected using any tool of choice (e.g., git gui).



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

## Performance Artifacts

This section evaluates TAF’s repository validation performance across multiple representative partners. The goal is to measure how efficiently TAF processes and verifies large versioned legal repositories under realistic conditions.  

We focus exclusively on validation performance, excluding clone times, since cloning is primarily dependent on external factors such as network throughput and local disk performance, which vary significantly between machines.  

Each test case profiles the execution of `taf repo validate` under controlled conditions. The profiling data is collected using Python’s `cProfile` and analyzed through custom scripts that extract cumulative runtime for the core updater routine (`run_tuf_updater`). These measurements provide a direct indication of TAF's internal efficiency during repository validation.

Due to underlying differences in the `pygit2` library, TAF exhibits different runtime characteristics on Windows versus Unix-based systems. To ensure reproducibility, we provide both `*-windows.prof` and `*-unix.prof` baseline profiles. Users may compare their local results against the corresponding reference for their operating system.  

Please note that performance will naturally vary with hardware specifications (CPU, disk speed, etc.). Our provided numbers serve as indicative baselines rather than fixed benchmarks.

### Running the Performance Evaluation

1. Navigate to the `./performance` directory.  
2. Run the following command:

   ```bash
   python -m run.py
   ```

3. The script will:

   - Execute taf repo validate under profiling for several sample partner repositories.
   - Collect .prof files containing detailed timing statistics.
   - Extract cumulative times for TAF’s updater routine.
   - Compare results against provided baseline profiles (*-unix.prof or *-windows.prof).
   - Output total validation time, difference, and per-commit performance insights.

The results summarize how each partner repository performs relative to the baseline, allowing evaluators to observe scaling behavior and performance consistency across jurisdictions.
