#!/usr/bin/env python3
"""Rewrite the PROJECTS block in README.md from the GitHub API.

Only public repos are visible to a visitor, so only public repos are indexed -
listing a private repo would render a dead link for everyone but the owner.

    python build_index.py            # rewrite README.md in place
    python build_index.py --dry-run  # print the generated block only
"""

import argparse
import json
import os
import pathlib
import urllib.request

OWNER = os.environ.get("GRIND_OWNER", "Ambhara")
README = pathlib.Path(__file__).parent / "README.md"
START = "<!-- PROJECTS:START -->"
END = "<!-- PROJECTS:END -->"

# Topic -> section heading, in the order they should appear.
TRACKS = [
    ("ai-engineering", "AI engineering"),
    ("data-engineering", "Data engineering"),
    ("web", "Web"),
]


def fetch_repos() -> list[dict]:
    url = f"https://api.github.com/users/{OWNER}/repos?per_page=100&sort=pushed"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "grind-profile-index",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        repos = json.load(response)

    # A private repo would render as a 404 for every visitor, so drop it.
    return [r for r in repos if not r.get("private") and "daily-project" in (r.get("topics") or [])]


def render(repos: list[dict]) -> str:
    if not repos:
        return (
            "_No public daily projects yet._\n\n"
            "The projects exist but are private, so they are omitted here rather "
            "than listed as links nobody else can open."
        )

    lines: list[str] = []
    for topic, heading in TRACKS:
        group = [r for r in repos if topic in (r.get("topics") or [])]
        if not group:
            continue

        group.sort(key=lambda r: r["pushed_at"], reverse=True)
        lines += [
            f"### {heading}",
            "",
            "| Project | What it does | Updated |",
            "| --- | --- | --- |",
        ]
        for repo in group:
            name = repo["name"]
            description = (repo.get("description") or "").replace("|", "\\|")
            updated = repo["pushed_at"][:10]
            lines.append(f"| [{name}]({repo['html_url']}) | {description} | {updated} |")
        lines.append("")

    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="print, don't write")
    args = parser.parse_args()

    block = render(fetch_repos())

    if args.dry_run:
        print(block)
        return 0

    text = README.read_text()
    if START not in text or END not in text:
        raise SystemExit(f"markers {START} / {END} not found in {README}")

    before = text.split(START)[0]
    after = text.split(END)[1]
    README.write_text(f"{before}{START}\n{block}\n{END}{after}")
    print(f"updated {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
