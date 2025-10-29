DESCRIPTION = """An attacker obtains credentials that allow commit and push access to both the target and authentication repositories, but does not have access to any metadata signing keys.
The attacker modifies law-xml and pushes a malicious update, then manually updates the corresponding metadata in the authentication repository and pushes it without applying a valid signature.

When the user later runs the updater, it detects that the authentication repository has changed and fetches the new metadata. Validation fails because the updates are unsigned, and the user's local repository remains unchanged.
"""
