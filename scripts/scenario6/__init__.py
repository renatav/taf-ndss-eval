DESCRIPTION = """An attacker pushes a malicious but invalid update, similar to the one in Scenario 2.
The publisher, without using TAF for validation, recklessly pulls these changes and subsequently creates and pushes a new valid, signed update.

When the user later runs the updater with default settings, the updater detects the new commits and begins validation from the oldest one.
Because validation fails on the earlier invalid commit, the process halts even though the newest commit is valid."""
