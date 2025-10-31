DESCRIPTION = """An attacker obtains credentials that grant commit and push access to both the target and authentication repositories, but does not possess any metadata signing keys.
The attacker reverts all repositories to a previous commit and force-pushes the branches, attempting to make an outdated version appear current.

When the user or publisher runs the updater with default settings, the updater detects that the top commit of the remote authentication repository is not present in the local history and halts the update.
This prevents the rollback attack from being accepted as a valid state.
"""
