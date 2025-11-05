import subprocess
import sys
import os


def run(cmd, cwd=None):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"ERROR: Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main():
    orgs = ["cityofsanmateo", "mohicanlaw", "sanipueblo", "tmchippewa"]
    repos = [
        "law",
        "law-html",
        "law-xml-codified",
        "law-xml",
        "law-static-assets",
        "law-rdf",
        "law-docs",
    ]

    for org in orgs:
        for repo in repos:
            # if already on disk skip
            if os.path.exists(os.path.join(org, repo)):
                print(f"Skipping {org}/{repo}, already cloned.")
                continue

            print(f"=== Cloning {org}/{repo} === This may take a while...")
            try:
                run(
                    [
                        "git",
                        "clone",
                        f"https://github.com/{org}/{repo}.git",
                        os.path.join(org, repo),
                    ]
                )
            except Exception as e:
                print(f"Failed to clone {org}/{repo}: {e}")


if __name__ == "__main__":
    main()
