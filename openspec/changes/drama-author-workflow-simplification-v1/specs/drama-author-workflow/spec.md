# drama-author-workflow Specification

## Purpose

为剧本作者提供退出 recipe/layout 的自然启动入口、唯一剧本路由和可移植的本地/远程 Auctra owner handoff；不改变 Auctra、Scaena、Eikona 与 ProductionGraph 的既有所有权。

## ADDED Requirements

### Requirement: 剧本 starter MUST 以真实内容和普通作者说明为起点

`manga-drama-project-starter` MUST read the existing project and owner status first, create only directories needed for the requested screenplay/material/outline content, and record current files, first reads, draft/review/history distinction and continuation method in ordinary `AGENTS.md`. It MUST NOT require or generate `workspace_recipe.v1`, `layout.v3`, layout manifests, mandatory frontmatter or an empty full skeleton.

#### Scenario: 只准备一集剧本

- **WHEN** 作者只要求准备一集正文和资料
- **THEN** starter SHALL create only the needed ordinary content entry
- **AND** Auctra/Scaena machine state SHALL remain owner-managed
- **AND** directory existence MUST NOT be described as accepted or production-ready

### Requirement: ai-drama-router MUST remain the only drama entry

All drama author requests MUST enter `ai-drama-router`, then select one primary method and at most one compatible constraint. Missing format facts that would change structure MUST return `needs_format_decision`. The router MUST NOT batch-enable all Skills, create a second screenplay body, or change canonical/production ownership.

#### Scenario: 场景写作请求

- **WHEN** an accepted format and source episode exist and the author asks for a scene
- **THEN** the route SHALL choose the narrowest existing scene-writing method
- **AND** scene references SHALL bind to the canonical episode text/source span
- **AND** the result SHALL remain a candidate until review/acceptance

### Requirement: Local and remote screenplay handoff MUST be explicit

Guidance MUST distinguish local CLI from remote MCP/HTTP discovery, invocation, status and resource/download. Remote clients MUST NOT require Auctra CLI, server filesystem paths, shell commands or injected actor/permission fields. Generation, selection, acceptance, saved version and production handoff MUST remain separate states.

#### Scenario: 远程服务缺少能力

- **WHEN** a required authoring capability is unavailable or the service is unreachable
- **THEN** guidance SHALL return `capability_missing` or `unregistered`
- **AND** MUST NOT fabricate a receipt, create a same-named work, or claim production readiness

### Requirement: Canonical and production owners MUST remain separated

The source guidance MUST preserve Auctra as screenplay/canonical text owner, Scaena as production/ProductionGraph owner, and Eikona as visual artifact owner. Skills MUST output proposal/review/handoff data rather than modifying canonical state or production assets.

#### Scenario: accepted screenplay handoff

- **WHEN** an accepted screenplay is prepared for production
- **THEN** the handoff SHALL include stable refs/digests and accepted-only source semantics
- **AND** the Skill MUST NOT call production, mutate `.scaena`, or infer shot-generation parameters
