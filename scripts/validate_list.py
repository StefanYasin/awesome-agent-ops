#!/usr/bin/env python3
"""Validate the structure of README.md before publishing."""

from __future__ import annotations

import re
import sys
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"

SECTIONS = [
    "Observability and tracing",
    "Evaluation and testing",
    "Guardrails and safety",
    "Sandboxes and permissions",
    "MCP security and gateways",
    "Fleet management and orchestration",
    "Cost and usage tracking",
    "Incident response",
]

NON_LIST_SECTIONS = {
    "Contents",
    "What belongs here",
    "Maintained by",
    "Contributing",
    "License",
}

ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\((https://github\.com/[^)\s]+)\) - (.+)$")
REPO_RE = re.compile(r"^https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    text = README.read_text(encoding="utf-8")
    lines = text.splitlines()

    errors: list[str] = []
    sections: dict[str, list[dict[str, str]]] = {}
    order: list[str] = []
    current: str | None = None

    for number, line in enumerate(lines, 1):
        heading = re.match(r"^## (.+)$", line)
        if heading:
            name = heading.group(1).strip()
            current = name if name in SECTIONS else None
            if current:
                if current in sections:
                    fail(errors, f"line {number}: duplicate section {current!r}")
                sections[current] = []
                order.append(current)
            continue

        if current and line.startswith("- "):
            match = ENTRY_RE.match(line)
            if not match:
                fail(errors, f"line {number}: malformed entry, expected '- [Name](url) - description.'")
                continue
            name, url, description = match.groups()
            sections[current].append(
                {"name": name, "url": url, "description": description, "line": str(number)}
            )

    if order != SECTIONS:
        fail(errors, f"section order is {order!r}, expected {SECTIONS!r}")

    total = 0
    seen_urls: dict[str, str] = {}
    seen_names: dict[str, str] = {}

    for section in SECTIONS:
        items = sections.get(section, [])
        total += len(items)
        if not items:
            fail(errors, f"section {section!r} has no entries")
            continue

        names = [item["name"] for item in items]
        if names != sorted(names, key=str.casefold):
            fail(errors, f"section {section!r} is not alphabetical: {names}")

        for item in items:
            name = item["name"]
            url = item["url"]
            description = item["description"]
            line = item["line"]

            if not REPO_RE.match(url):
                fail(errors, f"line {line}: not a canonical GitHub repository URL: {url}")
            if url != url.rstrip("/"):
                fail(errors, f"line {line}: trailing slash in {url}")
            if url in seen_urls:
                fail(errors, f"line {line}: duplicate URL {url}, first seen on line {seen_urls[url]}")
            seen_urls[url] = line
            if name.casefold() in seen_names:
                fail(errors, f"line {line}: duplicate name {name!r}")
            seen_names[name.casefold()] = line

            if not (20 <= len(description) <= 240):
                fail(errors, f"line {line}: description length {len(description)} outside 20..240")
            if not description.endswith("."):
                fail(errors, f"line {line}: description must end with a period")
            if description != description.strip():
                fail(errors, f"line {line}: description has leading or trailing whitespace")

    if not (60 <= total <= 90):
        fail(errors, f"entry count {total} is outside the required 60..90 range")

    claimed = re.search(r"\*\*(\d+) entries across (\d+) sections", text)
    if not claimed:
        fail(errors, "missing entry count sentence")
    else:
        if int(claimed.group(1)) != total:
            fail(errors, f"README claims {claimed.group(1)} entries but parsed {total}")
        if int(claimed.group(2)) != len(SECTIONS):
            fail(errors, f"README claims {claimed.group(2)} sections but expected {len(SECTIONS)}")

    if "## Maintained by" not in text:
        fail(errors, "missing 'Maintained by' section")
    if "https://github.com/StefanYasin/agentpulse" not in text:
        fail(errors, "'Maintained by' must link to agentpulse")
    if "https://stefanyasin.github.io/" not in text:
        fail(errors, "missing footer link to https://stefanyasin.github.io/")
    if "\u2014" in text:
        fail(errors, "README contains an em dash")

    if errors:
        print("README validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"README OK: {total} entries in {len(SECTIONS)} sections")
    for section in SECTIONS:
        print(f"  {section}: {len(sections[section])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
