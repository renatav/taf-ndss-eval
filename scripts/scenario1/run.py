import subprocess
import time
import sys
import os

from scripts.scenario_setup import setup_scenario

SCRIPT_DIR = os.path.dirname(__file__)
SCRIPTS = [
    ("../scenario_setup.py", 0),
    ("attacker.py", 3),
    ("user.py", 0),
    ("publisher.py", 0),
]

def run_script(path, delay_seconds):
    full_path = os.path.abspath(os.path.join(SCRIPT_DIR, path))
    print(f"\n=== Running {path} ===\n")
    result = subprocess.run([sys.executable, full_path])
    if result.returncode != 0:
        print(f"ERROR: {path} exited with status {result.returncode}")
        sys.exit(result.returncode)
    if delay_seconds > 0:
        time.sleep(delay_seconds)

def main():
    print("Running scenario 1")
    setup_scenario(1)
    # for script_path, pause in SCRIPTS:
    #     run_script(script_path, pause)
    # print("\n=== Scenario completed ===")

if __name__ == "__main__":
    main()
