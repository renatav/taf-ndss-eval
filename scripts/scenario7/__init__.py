DESCRIPTION = """The attacker gains commit and push access to the authentication repository and compromises the snapshot and timestamp keys, both of which have a signing threshold of 1, as well as one of the root keys.
They add their own targets signing key and use the compromised root key to sign the root, snapshot, and timestamp metadata. Root, however, has a signing threshold greater than one.

When the user runs the updater with default settings, validation fails because the root metadata is signed with only one key.
This prevents the partially compromised root from being accepted and blocks the malicious update.
"""
