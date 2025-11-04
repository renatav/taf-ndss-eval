from contextlib import contextmanager
from datetime import datetime
import importlib
from pathlib import Path
import shutil
import sys
import argparse
import uuid

from scenario_setup import setup_scenario
from scripts.shared import delete_dir

SCENARIOS_NUM = 7

REPO_ROOT = Path("../repositories")
ORIGIN_DIR = REPO_ROOT / "origin"
WORKSPACES_DIR = Path("../workspaces")

@contextmanager
def scenario_dirs(origin_base: Path, workspace_base: Path, scenario_name: str):
    temp_name = datetime.now().strftime("scenario_%Y%m%d_%H%M%S")
    origin_scenario_path = origin_base / f"{scenario_name}_{temp_name}"
    workspace_scenario_path = workspace_base / f"{scenario_name}_{temp_name}"
    try:
        yield origin_scenario_path, workspace_scenario_path
    finally:
        # Try to clean up (ignore any failures)
        for path in (origin_scenario_path, workspace_scenario_path):
            try:
                delete_dir(path)
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", "-l", action="store_true", help="List available scenarios.")
    parser.add_argument("--scenario", "-s", help=f"Scenario number (1-{SCENARIOS_NUM})")
    args = parser.parse_args()

    if args.list or not args.scenario:
        list_scenarios()
        if not args.scenario:
            return

    num = str(args.scenario).lower()
    if not num.isdigit() or not (1 <= int(num) <= SCENARIOS_NUM):
        print(f"Invalid scenario number. Please choose scenario 1-{SCENARIOS_NUM}")
        sys.exit(1)

    name = f"scenario{num}"
    with scenario_dirs(ORIGIN_DIR, WORKSPACES_DIR, name) as (origin_path, workspace_path):
        setup_scenario(origin_path, workspace_path)

        attacker = importlib.import_module(f"{name}.attacker")
        user = importlib.import_module(f"{name}.user")

        publisher = None
        try:
            publisher = importlib.import_module(f"{name}.publisher")
        except ModuleNotFoundError as e:
            pass

        print("\n=== Running attacker scenario ===\n")
        attacker.run(workspace_path)
        print("\n=== Attacker scenario complete ===\n")
        input("Press ENTER to continue")

        if publisher is not None:
            print("\n=== Running publisher scenario ===\n")
            publisher.run(workspace_path)
            print("\n=== Publisher scenario complete ===\n")
            input("Press ENTER to continue")

        print("\n=== Running user scenario ===\n")
        user.run(workspace_path)
        print("\n=== User scenario complete ===\n")
        input("Press ENTER to continue")



def list_scenarios():
    print("Available scenarios:\n")
    for num in range(1, SCENARIOS_NUM + 1):
        module_name = f"scenario{num}"
        try:
            mod = importlib.import_module(module_name)
            desc = getattr(mod, "DESCRIPTION", "(no description provided)")
        except Exception as e:
            desc = f"(failed to import: {e})"
        print(f"  {num:<4}  {desc}")
    print("\nRun a scenario with:")
    print("  python run_scenario.py --scenario <number>\n")

if __name__ == "__main__":
    main()