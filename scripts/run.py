import importlib
import sys
import argparse

from scenario_setup import setup_scenario

SCENARIOS_NUM = 7

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
    setup_scenario(int(num))

    attacker = importlib.import_module(f"{name}.attacker")
    user = importlib.import_module(f"{name}.user")

    publisher = None
    try:
        publisher = importlib.import_module(f"{name}.publisher")
    except ModuleNotFoundError as e:
        pass

    print("\n=== Running attacker scenario ===\n")
    attacker.run()
    print("\n=== Attacker scenario complete ===\n")
    input("Press ENTER to continue")

    if publisher is not None:
        print("\n=== Running publisher scenario ===\n")
        publisher.run()
        print("\n=== Publisher scenario complete ===\n")
        input("Press ENTER to continue")

    print("\n=== Running user scenario ===\n")
    user.run()
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