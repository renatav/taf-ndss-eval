import importlib
import sys
import argparse

from scenario_setup import setup_scenario

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", "-s", required=True, help="Scenario number (1-7)")
    args = parser.parse_args()

    num = str(args.scenario).lower()
    name = f"scenario{num}"
    module_name = f"scripts.{name}"

    setup_scenario(int(num))

    try:
        scenario = importlib.import_module(name)
    except ModuleNotFoundError as e:
        print(f"Invalid scenario name")
        sys.exit(1)

    try:
        attacker = importlib.import_module(f"{name}.attacker")
        publisher = importlib.import_module(f"{name}.publisher")
        user = importlib.import_module(f"{name}.user")
    except ModuleNotFoundError as e:
        print(e)

    if not hasattr(scenario, "run"):
        print(f"Scenario module '{module_name}' has no run() function.")
        sys.exit(1)


    print("Running attacker script")
    attacker.run()
    input("Press any key to continue")
    print("Running user script")
    user.run()
    input("Press any key to continue")
    print("Running publisher script")
    publisher.run()
    input("Press any key to continue")

if __name__ == "__main__":
    main()