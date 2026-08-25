#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def recipe(locale: str) -> dict:
    if locale not in {"en-US", "zh-CN"}:
        raise ValueError("locale must be en-US or zh-CN")
    zh = locale == "zh-CN"

    def pick(en: str, cn: str) -> str:
        return cn if zh else en

    rows = [
        ("screenplay", "screenplay_root", "screenplay", "剧本", True),
        ("outline", "planning_outline", "screenplay/outline", "剧本/大纲", False),
        ("characters", "story_bible_characters", "screenplay/characters", "剧本/人物", False),
        ("world", "story_bible_world", "screenplay/world", "剧本/设定", False),
        ("continuity", "story_continuity", "screenplay/continuity", "剧本/连续性", False),
        ("episodes", "screenplay_episodes", "screenplay/episodes", "剧本/分集", False),
        ("scenes", "screenplay_scenes", "screenplay/scenes", "剧本/场景", False),
        ("materials", "materials", "materials", "素材", True),
        ("reviews", "review_exports", "reviews", "审稿", True),
        ("exports", "exports", "exports", "导出", True),
    ]
    directories = [
        {"key": key, "display_name": Path(pick(en, cn)).name, "display_path": pick(en, cn), "machine_role": role, "materialize": materialize}
        for key, role, en, cn, materialize in rows
    ]
    return {
        "schema_version": "workspace_recipe.v1",
        "profile": "manga-drama",
        "locale": locale,
        "materialization": "on_demand",
        "directories": directories,
        "workspace_roles": [row[1] for row in rows],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", default="en-US", choices=["en-US", "zh-CN"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(recipe(args.locale), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
