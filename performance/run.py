import pstats
import re
import subprocess
import sys
import time
import os
import traceback
from clone_repos import clone_repos

def run(cmd, cwd=None):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def extract_updater_times(prof_files):
    results = {}
    # Regex matches both `run_tuf_updater` and `_run_tuf_updater`
    pattern = re.compile(r"updater_pipeline\.py:(880|2097)\((?:_)?run_tuf_updater\)$")

    for prof_file in prof_files:
        try:
            stats = pstats.Stats(prof_file)
            found = None

            for func_desc, values in stats.stats.items():
                filename, lineno, funcname = func_desc
                key_str = f"{filename}:{lineno}({funcname})"

                if pattern.search(key_str):
                    cc, nc, tt, ct, callers = values
                    found = {
                        "function": funcname,
                        "lineno": lineno,
                        "file": filename,
                        "self_time": tt,
                        "cumulative_time": ct,
                    }
                    break

            results[prof_file] = found or None

        except Exception as e:
            results[prof_file] = f"Error: {e}"

    return results


def run_updater():
    """
    - for each partner (cityofsanmateo, mohicanlaw, sanipueblo, tmchippewa)
       - go to that directory (performance/<partner>)
       - rename 'git' to '.git'
    - run `taf repo validate` with cwd under <partner>/law directory under cProfile
    - collect .prof files
    - extract cumulative times for `run_tuf_updater`/_run_tuf_updater
    - rename .git back to git (even in case where any errors occurred previously) for reproducibility
    """

    partners = [
        # skip DC since it has a huge law repo and takes too long to process
        "cityofsanmateo",
        "mohicanlaw",
        "sanipueblo",
        "tmchippewa",
    ]
    subdirs = [
        "law",
        "law-html",
        "law-xml-codified",
        "law-xml",
        "law-static-assets",
        "law-rdf",
        "law-docs",
    ]

    results = {}

    for partner in partners:
        base_dir = os.path.join(partner)
        if not os.path.isdir(base_dir):
            print(f"Skipping {partner}: directory not found ({base_dir})")
            continue

        print(f"\n=== Running updater for {partner} ===  This may take a while...")

        renamed_paths = []
        prof_path = os.path.join(base_dir, f"{partner}-validate.prof")
        law_dir = os.path.join(base_dir, "law")

        try:
            for sub in subdirs:
                path = os.path.join(base_dir, sub)
                git_path = os.path.join(path, "git")
                dotgit_path = os.path.join(path, ".git")
                if os.path.exists(git_path):
                    os.rename(git_path, dotgit_path)
                    renamed_paths.append((dotgit_path, git_path))

            if not os.path.isdir(law_dir):
                print(f"  Missing {law_dir}, skipping {partner}")
                continue

            prof_path = os.path.join(law_dir, "updater.prof")

            if os.path.exists(prof_path):
                os.remove(prof_path)
                # print(f"  Removed existing profiler file {prof_path}")

            if os.path.exists(os.path.join(base_dir, "_law")):
                try:
                    os.rmdir(os.path.join(base_dir, "_law"))
                except Exception as e:
                    print(f"  Failed to remove existing _law directory: {e}")

            cmd = [
                "taf",
                "repo",
                "validate",
                "--profile",
            ]

            start = time.time()
            result = subprocess.run(cmd, cwd=law_dir)
            elapsed = time.time() - start
            print(f"  Finished in {elapsed:.2f}s")

            if result.returncode != 0:
                print(
                    f"  ERROR: taf repo validate failed with code {result.returncode}"
                )
                results[partner] = f"Error: exit code {result.returncode}"
                continue

            prof_path = os.path.join(law_dir, "updater.prof")
            result_data = extract_updater_times([prof_path])
            info = result_data.get(prof_path)
            results[partner] = info

        except Exception as e:
            print(f"  ERROR while processing {partner}: {e}")
            traceback.print_exc()
            results[partner] = f"Error: {e}"

        finally:
            for dotgit_path, git_path in renamed_paths:
                if os.path.exists(dotgit_path):
                    try:
                        os.rename(dotgit_path, git_path)
                        # print(f"  Restored {dotgit_path} to {git_path}")
                    except Exception as e:
                        print(f"  Failed to restore {dotgit_path}: {e}")

    print("\n=== Summary ===")
    for partner, info in results.items():
        if isinstance(info, dict) and "cumulative_time" in info:
            print(f"{partner}: {info['cumulative_time']:.4f}s ({info['function']})")
        else:
            print(f"{partner}: {info}")

    return results


def extract_commit_counts():
    partners = ["cityofsanmateo", "mohicanlaw", "sanipueblo", "tmchippewa"]

    commit_counts = {}

    for partner in partners:
        base_dir = os.path.join(partner)
        commits_file = os.path.join(base_dir, "commits")
        try:
            with open(commits_file, "r") as f:
                content = f.read().strip()
                count = int(content)
                commit_counts[partner] = count
        except Exception as e:
            commit_counts[partner] = f"Error: {e}"

    return commit_counts


def main():

    ext = "windows" if os.name == "nt" else "unix"
    if os.name == "nt":
        print("Running on Windows, evaluation will use Windows prof files.")

    print("=== Set up: Cloning Repositories ===")

    clone_repos()

    prof_files = [
        f"mohicanlaw-{ext}.prof",
        f"sanipueblo-{ext}.prof",
        f"cityofsanmateo-{ext}.prof",
        f"tmchippewa-{ext}.prof",
    ]

    expected_times = extract_updater_times(prof_files)

    print("=== Expected Times ===")

    for prof_file in prof_files:
        expected = expected_times.get(prof_file)
        if isinstance(expected, dict):
            print(
                f"{prof_file}: {expected['cumulative_time']:.4f}s ({expected['function']})"
            )
        else:
            print(f"{prof_file}: {expected}")

    print("\n=== Running Tests ===")

    actual_times = run_updater()

    commits_per_jurisdiction = extract_commit_counts()

    print("\n=== Comparison ===")
    for partner in actual_times:
        expected = expected_times.get(f"{partner}-{ext}.prof")
        actual = actual_times.get(partner)

        if isinstance(expected, dict) and isinstance(actual, dict):
            exp_time = expected.get("cumulative_time")
            act_time = actual.get("cumulative_time")
            if exp_time is not None and act_time is not None:
                diff = act_time - exp_time
                print(
                    f"{partner}: Expected {exp_time:.4f}s, Actual {act_time:.4f}s, Diff {diff:.4f}s"
                )
                if exp_time > 0:
                    perc = (diff / exp_time) * 100
                    print(f"    Percentage difference: {perc:.2f}%")
                # Optionally, include commits info
                commits = commits_per_jurisdiction.get(partner)
                if isinstance(commits, int):
                    print(f"    Commits in repo: {commits}")

                if commits and isinstance(commits, int) and commits > 0:
                    time_per_commit = act_time / commits
                    print(f"    Time per commit: {time_per_commit:.6f}s")
            else:
                print(f"{partner}: Missing cumulative time in expected or actual data")
        else:
            print(f"{partner}: Cannot compare, expected or actual data is not valid")


if __name__ == "__main__":
    main()
