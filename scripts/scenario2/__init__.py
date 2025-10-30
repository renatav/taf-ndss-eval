DESCRIPTION = """An attacker obtains credentials that allow commit and push access to both a target and the authentication repository, but does not have access to any metadata signing keys.
The attacker modifies law-html and pushes a malicious update, then manually updates the file recording the last valid commit for that target repository in the authentication repository and pushes the change.
They do not update or sign the corresponding TUF metadata.

When the user or publisher later runs the updater, it detects that the authentication repository has changed and fetches the new metadata. Validation fails because the updates are unsigned, and the user's local repository remains unchanged.
"""
