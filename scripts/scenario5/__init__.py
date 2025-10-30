DESCRIPTION = """The attacker gains push access to the authentication repository but does not have access to any metadata signing keys.
Instead of creating new unsigned metadata, the attacker restores metadata from a previous commit that still contains valid signatures, attempting to make an older repository state appear current.

When the user or publisher runs the updater with default settings, the updater detects that the fetched metadata has a lower version number than the previously validated metadata.
The update is rejected, and the rollback to an older repository state is successfully prevented."""
