"""
Converts emilia's Elden Ring 1.12 attack-range CSV into a normalized JSON
dataset for the Attack Range Explorer.

Run with no arguments to (re)generate docs/assets/data/attack_ranges.json.
Run with --check to verify the committed JSON matches the CSV source.

Original data: emilia (Elden Ring 1.12 Attack Ranges)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_CSV = REPO_ROOT / "assets" / "data" / "attack_ranges_emilia.csv"
OUTPUT_PATH = REPO_ROOT / "assets" / "data" / "attack_ranges.json"

NUMERIC_FIELDS = {
    "Avg (m)": "avg_m",
    "Root Motion (m)": "root_motion_m",
    "Attack Extension (m)": "extension_m",
    "Estimated Startup (ms)": "startup_ms",
    "Estimated Startup (frames @ 30fps)": "startup_frames",
    "Speed to Active (m/s)": "speed_mps",
    "Min (m)": "min_m",
    "Max (m)": "max_m",
    "SD": "sd",
    "Sample Size": "sample_size",
}


def parse_number(s: str) -> float | int | None:
    s = s.strip()
    if not s:
        return None
    try:
        v = float(s)
        return int(v) if v.is_integer() and "." not in s else v
    except ValueError:
        return None


HAND_RE = re.compile(r"^(1h|2h|Paired)\b", re.IGNORECASE)


def classify_hand(attack: str) -> str:
    m = HAND_RE.match(attack.strip())
    if not m:
        return "other"
    return m.group(1).lower()


# Order matters: check more specific categories first.
CATEGORY_PATTERNS = [
    ("Charged R2", re.compile(r"Charged R2|R2 \d* ?Release", re.IGNORECASE)),
    ("Running", re.compile(r"\bRunning\b", re.IGNORECASE)),
    ("Rolling", re.compile(r"\bRolling\b", re.IGNORECASE)),
    ("Backstep", re.compile(r"\bBackstep\b", re.IGNORECASE)),
    ("Jumping", re.compile(r"\bJumping?\b", re.IGNORECASE)),
    ("Guard Counter", re.compile(r"Guard ?Counter", re.IGNORECASE)),
    ("Paired L1", re.compile(r"Paired L1", re.IGNORECASE)),
    ("Paired L2", re.compile(r"Paired L2", re.IGNORECASE)),
    ("Paired R1", re.compile(r"Paired R1", re.IGNORECASE)),
    ("Paired R2", re.compile(r"Paired R2", re.IGNORECASE)),
    ("R2", re.compile(r"\bR2\b", re.IGNORECASE)),
    ("R1", re.compile(r"\bR1\b", re.IGNORECASE)),
    ("L1", re.compile(r"\bL1\b", re.IGNORECASE)),
    ("L2", re.compile(r"\bL2\b", re.IGNORECASE)),
]


def classify_category(attack: str) -> str:
    for label, pat in CATEGORY_PATTERNS:
        if pat.search(attack):
            return label
    return "Other"


def build() -> dict:
    if not SOURCE_CSV.exists():
        raise FileNotFoundError(f"Source CSV missing: {SOURCE_CSV}")

    attacks = []
    with SOURCE_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                "setup": row["Setup"].strip(),
                "weapon_class": row["Class"].strip(),
                "attack": row["Attack"].strip(),
                "hand": classify_hand(row["Attack"]),
                "category": classify_category(row["Attack"]),
                "notes": row["Notes"].strip(),
                "animation_id": row["Frame Data"].strip(),
            }
            for src, dst in NUMERIC_FIELDS.items():
                entry[dst] = parse_number(row[src])
            attacks.append(entry)

    classes = sorted({a["weapon_class"] for a in attacks})
    categories = sorted({a["category"] for a in attacks})
    hands = sorted({a["hand"] for a in attacks})

    return {
        "schema_version": 1,
        "generated_by": "tools/extract_attack_ranges.py",
        "data_source": "emilia (Elden Ring 1.12 Attack Ranges)",
        "game_version": "1.12",
        "attack_count": len(attacks),
        "weapon_classes": classes,
        "categories": categories,
        "hands": hands,
        "attacks": attacks,
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
            print(f"::error::{OUTPUT_PATH} does not exist. Run tools/extract_attack_ranges.py.")
            return 1
        existing = OUTPUT_PATH.read_text(encoding="utf-8")
        if existing != new_text:
            print(
                f"::error::{OUTPUT_PATH} is out of date. "
                f"Run `python tools/extract_attack_ranges.py` and commit the result."
            )
            return 1
        print(
            f"OK: {OUTPUT_PATH} matches CSV source "
            f"({data['attack_count']} attacks across {len(data['weapon_classes'])} classes)."
        )
        return 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(new_text, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({data['attack_count']} attacks).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
