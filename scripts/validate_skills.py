#!/usr/bin/env python3
"""Validate the portable AI Drama Skills collection without host dependencies."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
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

    router_dir = ROOT / "ai-drama-router"
    originality_ref = router_dir / "references" / "originality-and-reference-policy.md"
    if not originality_ref.is_file():
        errors.append(f"{originality_ref}: missing originality contract")
    else:
        originality_text = originality_ref.read_text(encoding="utf-8")
        for required in (
            "pure_original",
            "licensed_adaptation",
            "reference_constrained",
            "transformative_research",
            "similarity_review_required",
        ):
            if required not in originality_text:
                errors.append(f"{originality_ref}: missing {required}")

    orchestrator_dir = ROOT / "ai-drama-production-orchestrator"
    production_ref = (
        orchestrator_dir
        / "references"
        / "original-manga-drama-production-loop.md"
    )
    if not production_ref.is_file():
        errors.append(f"{production_ref}: missing original production loop")
    else:
        production_text = production_ref.read_text(encoding="utf-8")
        for required in (
            "auctra production handoff export",
            "scaena asset draw plan",
            "scaena video episode-preview",
            "scaena edit select",
            "openai/gpt-5.4-image-2",
            "workflow_goal_unavailable",
            "fixture-only",
        ):
            if required not in production_text:
                errors.append(f"{production_ref}: missing {required}")
        if "export package --dry-run" in production_text:
            errors.append(f"{production_ref}: uses unsupported export --dry-run flag")

    recipe_script = ROOT / "manga-drama-project-starter" / "scripts" / "generate_workspace_recipe.py"
    required_roles = {
        "screenplay_root",
        "planning_outline",
        "story_bible_characters",
        "story_bible_world",
        "story_continuity",
        "screenplay_episodes",
        "screenplay_scenes",
        "materials",
        "review_exports",
        "exports",
    }
    for locale in ("en-US", "zh-CN"):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "recipe.json"
            result = subprocess.run(
                [sys.executable, str(recipe_script), "--locale", locale, "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                errors.append(f"manga-drama recipe generation failed for {locale}: {result.stderr.strip()}")
                continue
            payload = json.loads(output.read_text(encoding="utf-8"))
            roles = set(payload.get("workspace_roles", []))
            if payload.get("schema_version") != "workspace_recipe.v1":
                errors.append(f"manga-drama recipe {locale}: invalid schema_version")
            if payload.get("profile") != "manga-drama" or payload.get("locale") != locale:
                errors.append(f"manga-drama recipe {locale}: profile/locale mismatch")
            if payload.get("materialization") != "on_demand":
                errors.append(f"manga-drama recipe {locale}: materialization must be on_demand")
            missing_roles = sorted(required_roles - roles)
            if missing_roles:
                errors.append(f"manga-drama recipe {locale}: missing roles {missing_roles}")
            if roles & {"manuscript_root", "manuscript_chapters"}:
                errors.append(f"manga-drama recipe {locale}: contains novel manuscript roles")

    if errors:
        print("FAIL: AI Drama Skills validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PASS: validated {len(skill_files)} portable AI Drama Skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
