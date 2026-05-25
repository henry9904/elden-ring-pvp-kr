"""
Converts emilia's Elden Ring Frame Data animations CSV into a normalized
JSON dataset for the Animations Explorer.

Run with no arguments to (re)generate assets/data/animations.json.
Run with --check to verify the committed JSON matches the CSV source.

Original data: emilia (Elden Ring Frame Data Explorer)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_CSV = REPO_ROOT / "assets" / "data" / "animations_emilia.csv"
OUTPUT_PATH = REPO_ROOT / "assets" / "data" / "animations.json"

# Only fields with reliably populated values in this export.
KEPT_FIELDS = {"id", "name", "flags", "class", "weapons"}


def split_list(s: str) -> list[str]:
    if not s:
        return []
    return [p.strip() for p in s.split(",") if p.strip()]


def build() -> dict:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Source CSV missing: {SOURCE_CSV}")

    animations = []
    skipped = 0
    with SOURCE_CSV.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        idx = {name: i for i, name in enumerate(header)}
        for row in reader:
            # Skip malformed rows (quote-escape bugs in the source export
            # produce rows with the wrong column count).
            if len(row) < 5:
                skipped += 1
                continue
            animations.append({
                "id": row[idx["id"]].strip(),
                "name": row[idx["name"]].strip(),
                "class": row[idx["class"]].strip(),
                "flags": split_list(row[idx["flags"]]),
                "weapons": split_list(row[idx["weapons"]]),
            })

    classes = sorted({a["class"] for a in animations})
    all_flags = Counter()
    for a in animations:
        all_flags.update(a["flags"])
    # Sort flags by frequency (most common first) so the UI surfaces the
    # important ones (Attack, Parriable, HyperArmour, …) at the top.
    flags_sorted = [f for f, _ in all_flags.most_common()]

    return {
        "schema_version": 1,
        "generated_by": "tools/extract_animations.py",
        "data_source": "emilia (Elden Ring Frame Data Explorer)",
        "animation_count": len(animations),
        "skipped_malformed": skipped,
        "weapon_classes": classes,
        "flags": flags_sorted,
        "animations": animations,
    }


def serialize(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if committed JSON is stale relative to the CSV source.",
    )
    args = parser.parse_args()

    data = build()
    new_text = serialize(data)

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"::error::{OUTPUT_PATH} does not exist. Run tools/extract_animations.py.")
            return 1
        existing = OUTPUT_PATH.read_text(encoding="utf-8")
        if existing != new_text:
            print(
                f"::error::{OUTPUT_PATH} is out of date. "
                f"Run `python tools/extract_animations.py` and commit the result."
            )
            return 1
        print(
            f"OK: {OUTPUT_PATH} matches CSV source "
            f"({data['animation_count']} animations, {len(data['weapon_classes'])} classes, "
            f"{len(data['flags'])} flags)."
        )
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(new_text, encoding="utf-8")
    print(
        f"Wrote {OUTPUT_PATH} ({data['animation_count']} animations, "
        f"{data['skipped_malformed']} skipped)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
