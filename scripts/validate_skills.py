#!/usr/bin/env python3
"""Validate portable AI Drama Skills and their resolved source contracts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PORTABILITY_MARKERS = ("/workspaces/yeisme-agent", "/home/yeisme")
RETIRED_ROLE_NAMES = (
    "ai-drama-format-strategist",
    "ai-drama-story-architecture",
    "ai-drama-character-engine",
    "ai-drama-showrunner",
    "ai-drama-critic-panel",
    "screenplay-scene-writer",
)
REQUIRED_METADATA = ("display_name", "short_description", "default_prompt")
errors: list[str] = []


def value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    return match.group(1).strip("\"'") if match else None


def links(path: Path, text: str) -> list[Path]:
    result: list[Path] = []
    for target in re.findall(r"\[[^]]+\]\(([^)#]+)", text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        result.append((path.parent / target).resolve())
    return result


skill_files = sorted(ROOT.glob("*/SKILL.md"))
if not skill_files:
    errors.append("no top-level Skills found")

for skill_file in skill_files:
    skill_dir = skill_file.parent
    text = skill_file.read_text(encoding="utf-8")
    name = value(text, "name")
    if name != skill_dir.name:
        errors.append(f"{skill_file}: name must equal directory {skill_dir.name}")
    if not value(text, "description"):
        errors.append(f"{skill_file}: missing description")
    metadata = skill_dir / "agents" / "openai.yaml"
    if not metadata.is_file():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")
    else:
        metadata_text = metadata.read_text(encoding="utf-8")
        for field in REQUIRED_METADATA:
            if not value(metadata_text, field):
                errors.append(f"{metadata}: missing or empty {field}")
    for marker in FORBIDDEN_PORTABILITY_MARKERS:
        if marker in text:
            errors.append(f"{skill_file}: contains host-specific path {marker}")
    for link in links(skill_file, text):
        if not link.is_file():
            errors.append(f"{skill_file}: unresolved local reference {link}")

router = ROOT / "ai-drama-router"
router_skill = router / "SKILL.md"
router_refs = router / "references"
for required in (router_skill, router_refs / "routing-matrix.md", router_refs / "drama-route-plan-contract.md"):
    if not required.is_file():
        errors.append(f"missing router contract: {required}")

if router_skill.is_file():
    router_text = router_skill.read_text(encoding="utf-8")
    for section in ("## 目标", "## 参考资料", "## 路由流程", "## 核心路由", "## 输出"):
        if section not in router_text:
            errors.append(f"{router_skill}: missing section {section}")
    for field in ("goal", "medium", "phase", "artifact", "primary_skill", "compatible_skill", "input_refs", "missing_inputs", "canonical_owner", "gates", "owner_action", "next_action", "status"):
        if f"`{field}`" not in router_text:
            errors.append(f"{router_skill}: missing route field {field}")
    for role in RETIRED_ROLE_NAMES:
        if role in router_text and f"`{role}`" in router_text:
            errors.append(f"{router_skill}: retired role remains active {role}")

if (router_refs / "routing-matrix.md").is_file():
    matrix_text = (router_refs / "routing-matrix.md").read_text(encoding="utf-8")
    for section in ("## 全局原创性门禁", "| `intake`", "| `scene_draft`", "| `generation`", "| `delivery_review`"):
        if section not in matrix_text:
            errors.append(f"{router_refs / 'routing-matrix.md'}: missing structural route {section}")
    for role in RETIRED_ROLE_NAMES:
        if f"`{role}`" in matrix_text:
            errors.append(f"{router_refs / 'routing-matrix.md'}: retired role remains active {role}")

assessment = ROOT / "ai-drama-assessment" / "references" / "assessment-contract.md"
production = ROOT / "ai-drama-production-orchestrator" / "references" / "original-manga-drama-production-loop.md"
for path, markers in (
    (assessment, ("dialogue_liveability", "narrative_naturalness", "structural_formula_risk", "naturalness_score", "author_source_inference_forbidden")),
    (production, ("auctra production handoff export", "scaena asset draw plan", "workflow_goal_unavailable", "fixture-only")),
):
    if not path.is_file():
        errors.append(f"missing contract: {path}")
    else:
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path}: missing required contract marker {marker}")

starter = ROOT / "manga-drama-project-starter"
for retired_path in (starter / "scripts" / "generate_workspace_recipe.py", starter / "references" / "workspace-layout.md"):
    if retired_path.exists():
        errors.append(f"retired starter path still exists: {retired_path}")

active_files = [path for path in ROOT.rglob("*") if path.is_file() and "openspec" not in path.parts and "scripts" not in path.parts]
for path in active_files:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for role in RETIRED_ROLE_NAMES:
        if f"`{role}`" in text and path not in (router_refs / "route-examples.md", router_refs / "context-pack-profiles.md"):
            errors.append(f"{path}: retired drama role reference {role}")

if errors:
    print("FAIL: AI Drama Skills validation failed", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print(f"PASS: validated {len(skill_files)} portable AI Drama Skills structurally")
