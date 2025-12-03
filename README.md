# TAF Artifact Evaluation

This repository contains the artifact evaluation materials for the NDSS 2026
submitted paper "Enhancing Legal Document Security and Accessibility with TAF".

The artifact includes two categories of evaluation scripts:

- **Security evaluation scenarios** that demonstrate how TAF prevents a range of attacks, especially those involving attacker control over a publisher’s Git account or key material.
- **Performance assessment scripts** that benchmark profiling results that assess TAF's performance under realistic workloads.

The evaluation uses the pre-built TAF hosted on PyPI, but you may download the
source code for TAF `v0.36.0` at
https://github.com/openlawlibrary/taf/releases/tag/v0.36.0.

## Requirements

To run the included scripts:

1. **Python version**: Supported versions are **Python 3.8 through 3.12**.
2. **Python venv**: To make installation smoother, we recommend setting up a new Python virtual environment:
   1. Configure it by running `python -m venv taf-venv` in the root directory of this repository.
   2. Activate it by running `source taf-venv/bin/activate` or the command appropriate for your OS.
3. **Install TAF** from PyPI: `pip install taf==0.36.0`

For reference, `pip list` in an environment initialized with Python 3.12 should return the following after installing TAF 0.36.0:

```
Package            Version
------------------ ----------
attrs              25.4.0
cattrs             25.3.0
certifi            2025.11.12
cffi               2.0.0
charset-normalizer 3.4.4
click              8.3.1
colorama           0.4.6
cryptography       43.0.3
idna               3.11
logdecorator       2.5
loguru             0.7.3
pip                24.0
pycparser          2.23
pygit2             1.14.1
pyOpenSSL          24.2.1
requests           2.32.5
securesystemslib   1.3.1
setuptools         80.9.0
taf                0.36.0
tomli              2.0.2
tuf                5.1.0
typing_extensions  4.15.0
urllib3            2.5.0
```

4. **Git**: Git must be installed and configured with a committer name and email.
You can verify or set this using:
```
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com
```

The security evaluation scripts invoke `git commit`, so these settings are
required.

## Running the Security Scenarios

Detailed instructions for running and inspecting the security evaluation
scenarios can be found in [scripts/README.md](scripts/README.md).

## Running the Performance Tests

Detailed instructions for running performance tests can be found in
[performance/README.md](performance/README.md).
