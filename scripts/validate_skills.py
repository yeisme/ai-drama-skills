#!/usr/bin/env python3
"""Validate the portable AI Drama Skills collection without host dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_METADATA = ("display_name:", "short_description:", "default_prompt:")
FORBIDDEN_PORTABILITY_MARKERS = ("/workspaces/yeisme-agent", "/home/yeisme")


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip("\"'") if match else None


def main() -> int:
    errors: list[str] = []
    names: dict[str, Path] = {}
    skill_files = sorted(ROOT.glob("*/SKILL.md"))

    if not skill_files:
        errors.append("no top-level Skills found")

    for skill_file in skill_files:
        skill_dir = skill_file.parent
        text = skill_file.read_text(encoding="utf-8")
        name = frontmatter_value(text, "name")
        description = frontmatter_value(text, "description")

        if name != skill_dir.name:
            errors.append(f"{skill_file}: name must equal directory {skill_dir.name}")
        if not description:
            errors.append(f"{skill_file}: missing description")
        if name:
            if name in names:
                errors.append(f"duplicate skill name {name}: {names[name]} and {skill_file}")
            names[name] = skill_file

        metadata = skill_dir / "agents" / "openai.yaml"
        if not metadata.is_file():
            errors.append(f"{skill_dir}: missing agents/openai.yaml")
        else:
            metadata_text = metadata.read_text(encoding="utf-8")
            for field in REQUIRED_METADATA:
                if field not in metadata_text:
                    errors.append(f"{metadata}: missing {field[:-1]}")

        for marker in FORBIDDEN_PORTABILITY_MARKERS:
            if marker in text:
                errors.append(f"{skill_file}: contains host-specific path {marker}")

    if errors:
        print("FAIL: AI Drama Skills validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: validated {len(skill_files)} portable AI Drama Skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
