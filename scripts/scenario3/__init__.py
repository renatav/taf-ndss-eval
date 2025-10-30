DESCRIPTION = """An attacker obtains credentials that grant commit and push access to both the target and authentication repositories, but has not compromised any metadata signing keys.
The attacker modifies law-xml and pushes a malicious update. They then update the file recording the last valid commit for that target and correctly update the TUF metadata (the attacker is familiar with TUF), but cannot produce valid signatures of those updates.
The attacker pushes these unsigned changes to the authentication repository.

When the user or publisher runs the updater with default settings, the updater detects the authentication repository update and fetches the incoming changes for validation. Validation fails because the metadata updates are unsigned, and the user's local repository remains unchanged.
"""
