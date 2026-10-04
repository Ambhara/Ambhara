#!/usr/bin/env python3
"""Safely refresh the optional public-project index in README.md.

The curated profile is authoritative. Automation only replaces the marked
PROJECTS block when at least one public repository is explicitly tagged
"daily-project". If none qualify, the existing curated block is preserved.
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
TRACKS = [
    ("ai-engineering", "AI engineering"),
    ("data-engineering", "Data engineering"),
    ("web", "Web"),
]


def fetch_repos() -> list[dict]:
    url = f"https://api.github.com/users/{OWNER}/repos?per_page=100&sort=pushed"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ambhara-profile-index",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        repos = json.load(response)

    return [
        repo
        for repo in repos
        if not repo.get("private") and "daily-project" in (repo.get("topics") or [])
    ]


def render(repos: list[dict]) -> str:
    lines: list[str] = []
    for topic, heading in TRACKS:
        group = [repo for repo in repos if topic in (repo.get("topics") or [])]
        if not group:
            continue

        group.sort(key=lambda repo: repo["pushed_at"], reverse=True)
        lines.extend(
            [
                f"### {heading}",
                "",
                "| Project | What it does | Updated |",
                "| --- | --- | --- |",
            ]
        )
        for repo in group:
            name = repo["name"]
            description = (repo.get("description") or "").replace("|", "\\|")
            updated = repo["pushed_at"][:10]
            lines.append(
                f"| [{name}]({repo['html_url']}) | {description} | {updated} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not README.exists():
        raise SystemExit(f"README not found: {README}")

    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"markers {START} / {END} not found in {README}")

    repos = fetch_repos()
    block = render(repos)

    if args.dry_run:
        print(block or "(no tagged public projects)")
        return 0

    if not block:
        print("no tagged public projects; preserving curated README block")
        return 0

    before, remainder = text.split(START, 1)
    _, after = remainder.split(END, 1)
    README.write_text(
        f"{before}{START}\n{block}\n{END}{after}",
        encoding="utf-8",
    )
    print(f"updated {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
