#!/usr/bin/env python3
"""Validate the portable AI drama router package without host dependencies."""

from __future__ import annotations

import sys
from pathlib import Path


ROUTER_REFERENCES = (
    "canon-boundary.md",
    "routing-matrix.md",
    "skill-resolution-policy.md",
    "drama-route-plan-contract.md",
    "artifact-lifecycle.md",
    "originality-and-reference-policy.md",
    "shot-audio-intent-contract.md",
    "video-model-capability-index.md",
    "video-model-profile-minimax-h3.md",
    "video-model-profile-wan-3-0.md",
    "seedance-2-5-capability-profile.md",
    "video-model-profile-kling-v3.md",
    "video-model-profile-kling-v3-omni.md",
    "video-model-drama-workflow-matrix.md",
    "video-model-community-research-2026-09-01.md",
    "upstream-video-production-patterns.md",
    "route-examples.md",
)

REQUIRED_SKILL_NAMES = (
    "manga-drama-project-starter",
    "ai-drama-format-strategist",
    "ai-drama-context-pack-builder",
    "ai-drama-story-architecture",
    "ai-drama-character-engine",
    "ai-drama-showrunner",
    "screenplay-scene-writer",
    "ai-drama-director",
    "ai-drama-video-reference-director",
    "ai-drama-visual-language",
    "ai-drama-edit-and-sound",
    "ai-drama-assessment",
    "ai-drama-continuity-supervisor",
    "ai-drama-critic-panel",
    "ai-drama-producer",
    "ai-drama-production-orchestrator",
    "creative-style-lens-builder",
)

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    script_path = Path(__file__).resolve()
    router_dir = script_path.parents[1]
    references_dir = router_dir / "references"

    for reference in ROUTER_REFERENCES:
        if not (references_dir / reference).is_file():
            fail(f"missing router reference: {reference}")

    skill_text = (router_dir / "SKILL.md").read_text(encoding="utf-8")
    matrix_text = (references_dir / "routing-matrix.md").read_text(encoding="utf-8")
    combined_contract = skill_text + "\n" + matrix_text

    for skill_name in REQUIRED_SKILL_NAMES:
        if f"`{skill_name}`" not in combined_contract:
            fail(f"routing contract does not reference required skill: {skill_name}")

    if "一个 primary" not in skill_text or "最多一个" not in skill_text:
        fail("router must preserve the one-primary/one-constraint invariant")
    for field in (
        "artifact_disposition",
        "persistence_policy",
        "batch_policy",
        "acceptance_state",
    ):
        if field not in skill_text or field not in (
            references_dir / "drama-route-plan-contract.md"
        ).read_text(encoding="utf-8"):
            fail(f"router lifecycle contract is missing field: {field}")
    lifecycle_text = (references_dir / "artifact-lifecycle.md").read_text(
        encoding="utf-8"
    )
    examples_text = (references_dir / "route-examples.md").read_text(
        encoding="utf-8"
    )
    contract_text = (references_dir / "drama-route-plan-contract.md").read_text(
        encoding="utf-8"
    )

    for field in (
        "assessment_contract_ref",
        "assessment_state",
        "score_eligibility",
        "naturalness_profile",
        "naturalness_lanes",
        "naturalness_report_refs",
        "naturalness_score_policy",
    ):
        if field not in skill_text or field not in contract_text:
            fail(f"router assessment contract is missing field: {field}")
    for lane in (
        "dialogue_liveability",
        "narrative_naturalness",
        "structural_formula_risk",
    ):
        if lane not in matrix_text or lane not in contract_text:
            fail(f"router naturalness contract is missing lane: {lane}")
    for failure_code in (
        "needs_assessment_contract",
        "score_not_applicable",
        "assessment_not_comparable",
        "naturalness_not_comparable",
        "author_source_inference_forbidden",
    ):
        if failure_code not in skill_text:
            fail(f"router assessment failure state is missing: {failure_code}")

    model_index_text = (references_dir / "video-model-capability-index.md").read_text(
        encoding="utf-8"
    )
    workflow_matrix_text = (
        references_dir / "video-model-drama-workflow-matrix.md"
    ).read_text(encoding="utf-8")
    community_text = (
        references_dir / "video-model-community-research-2026-09-01.md"
    ).read_text(encoding="utf-8")
    for family in (
        "minimax_h3",
        "wan",
        "seedance",
        "kling_v3",
        "kling_v3_omni",
    ):
        if family not in model_index_text:
            fail(f"video model capability index is missing family: {family}")
    for field in (
        "binding_mode",
        "non_binding",
        "required_capabilities",
        "eligible_model_families",
        "suggested_model_family",
        "suggestion_basis",
        "workflow_profile_ref",
        "workflow_profile_digest",
    ):
        if field not in contract_text:
            fail(f"video model guidance contract is missing field: {field}")
    if (
        "社区热度" not in model_index_text
        or "不得" not in model_index_text
        or "research_signal" not in community_text
    ):
        fail("community research must remain non-routing research_signal")
    for scenario_id in (
        "short_dialogue_shot",
        "action_camera_reference",
        "first_last_frames",
        "keyframe_storyboard",
        "video_edit_extend",
        "long_take_20_30s",
        "h3_2k_refinement",
        "native_audio_candidate",
        "post_replace_audio",
    ):
        if scenario_id not in workflow_matrix_text:
            fail(f"video drama workflow matrix is missing scenario: {scenario_id}")
    originality_text = (
        references_dir / "originality-and-reference-policy.md"
    ).read_text(encoding="utf-8")
    if "Markdown 文件存在 ≠ 用户认可内容" not in lifecycle_text:
        fail("artifact lifecycle must separate output format from acceptance")
    if (
        "batch_policy: proof_slice" not in examples_text
        or "60 集" not in examples_text
    ):
        fail("route examples must keep the multi-episode proof-slice fixture")
    if (
        "output_format: markdown" not in examples_text
        or "acceptance_state: unreviewed" not in examples_text
    ):
        fail("route examples must keep the Markdown-without-acceptance fixture")
    for field in ("originality_mode", "originality_decision_ref"):
        if field not in skill_text or field not in contract_text:
            fail(f"router originality contract is missing field: {field}")
    for mode in (
        "pure_original",
        "licensed_adaptation",
        "reference_constrained",
        "transformative_research",
    ):
        if mode not in originality_text:
            fail(f"originality policy is missing mode: {mode}")
    for failure_code in (
        "needs_originality_decision",
        "reference_rights_unknown",
        "protected_expression_risk",
        "style_identity_leak",
        "similarity_review_required",
        "adaptation_not_authorized",
    ):
        if failure_code not in originality_text or failure_code not in skill_text:
            fail(f"originality failure state is missing: {failure_code}")
    if (
        "纯原创竖屏漫剧全链路" not in examples_text
        or "story_canon_and_screenplay" not in examples_text
        or "production_delivery_review_and_export" not in examples_text
    ):
        fail("route examples must keep the pure-original end-to-end fixture")
    upstream_text = (
        references_dir / "upstream-video-production-patterns.md"
    ).read_text(encoding="utf-8")
    for pattern_id in (
        "one-click-pipeline-lifecycle",
        "cinematic-shot-recipe",
        "long-video-highlight-extraction",
        "programmable-renderer-best-practices",
        "conversational-edit-proposal",
        "external-nle-draft-handoff",
    ):
        if pattern_id not in upstream_text:
            fail(f"upstream reference is missing pattern family: {pattern_id}")
    if "固定 commit" not in skill_text or "不在 active production stage" not in upstream_text:
        fail("upstream patterns must remain pinned and production-stage immutable")
    if "approved_current_request" not in (
        references_dir / "skill-resolution-policy.md"
    ).read_text(encoding="utf-8"):
        fail("activation policy must preserve explicit current-request authorization")

    print("PASS: portable AI drama router package is structurally valid")


if __name__ == "__main__":
    main()
