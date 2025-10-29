
DESCRIPTION = """An attacker compromises the credentials of a target repository, gaining commit and push access but not control over the authentication repository. They push a malicious update to law-xml.

When the user runs the updater with default settings, no new commits are fetched because the authentication repository remains unchanged. The publisher runs the updater with a full check and detects the malicious commit, receiving a validation error.
"""
