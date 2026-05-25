"""
Extracts weapon tier tables from English weapon guide markdown files
and produces a unified JSON dataset.

Run with no arguments to (re)generate docs/assets/data/weapons.json.
Run with --check to verify the committed JSON matches the markdown source.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "docs" / "assets" / "data" / "weapons.json"

# Each guide we know how to parse. The key is the displayed weapon class;
# the value is metadata about how to find/interpret the table.
GUIDES = [
    {
        "weapon_class": "Straight Sword",
        "path": REPO_ROOT / "guides" / "Straight_Sword_Guide_EN.md",
        "slug": "Straight_Sword_Guide_EN",
        "section": "tier-list--comparison",
        "damage_label": "1H R1",
    },
    {
        "weapon_class": "Halberd",
        "path": REPO_ROOT / "guides" / "Halberd_Guide_EN.md",
        "slug": "Halberd_Guide_EN",
        "section": "tier-list--comparison",
        "damage_label": "1H RR1",
    },
    {
        "weapon_class": "Katana",
        "path": REPO_ROOT / "guides" / "Katana_Guide_EN.md",
        "slug": "Katana_Guide_EN",
        "section": "tier-list--comparison",
        "damage_label": "1H R1",
    },
]


@dataclass
class Weapon:
    tier: str
    name: str
    weapon_class: str
    optimal_stats: str
    ar: str
    ar_peak: int  # highest numeric AR found, for sorting
    damage_1h: str
    damage_peak: int  # highest numeric damage found, for sorting
    weight: float
    extra: str  # moveset type / status / etc — whatever the guide adds
    extra_label: str
    damage_label: str
    source_guide: str
    source_url: str


TIER_RE = re.compile(r"^\|\s*\*\*([SABCDEF]\+?)\*\*\s*\|")
BOLD_NUM_RE = re.compile(r"\*\*(\d+(?:\.\d+)?)\*\*")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def split_row(line: str) -> list[str]:
    # Drop leading/trailing pipe, split, strip whitespace
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    return parts


def find_table_lines(md: str) -> list[str] | None:
    """Locate the tier table — header row starts with '| Tier |'."""
    lines = md.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("| Tier ") and "Weapon" in line:
            rows = []
            # Skip header (i) and separator (i+1), then collect data rows
            for j in range(i + 2, len(lines)):
                row = lines[j]
                if not row.lstrip().startswith("|"):
                    break
                if TIER_RE.match(row):
                    rows.append(row)
                else:
                    break
            return [lines[i]] + rows
    return None


def peak_number(cell: str) -> int:
    """Return the largest integer found in a cell, or 0 if none."""
    # Prefer bolded numbers (the canonical AR value)
    bolded = [int(float(m)) for m in BOLD_NUM_RE.findall(cell)]
    if bolded:
        return max(bolded)
    nums = [int(float(m)) for m in NUM_RE.findall(cell)]
    return max(nums) if nums else 0


def parse_guide(meta: dict) -> list[Weapon]:
    md = meta["path"].read_text(encoding="utf-8")
    table = find_table_lines(md)
    if not table:
        raise RuntimeError(f"No tier table found in {meta['path']}")

    header_cells = split_row(table[0])
    # Column indices: Tier, Weapon are always first two. The rest varies.
    # We standardize: Tier, Weapon, [maybe Moveset/Type], Optimal Stats, AR, Damage, [maybe Status], Weight
    idx = {name.lower(): i for i, name in enumerate(header_cells)}

    def col(*names: str) -> int:
        for n in names:
            for key, i in idx.items():
                if n.lower() in key:
                    return i
        return -1

    i_tier = col("tier")
    i_name = col("weapon")
    # "Optimal Stats" exists in all three guides
    i_stats = col("optimal stats")
    # AR column has either "AR" or "AR (1H)"
    i_ar = col("ar")
    # Damage column varies; identify by label hint
    i_dmg = col("dmg", "damage")
    i_weight = col("weight")

    # Extra column: anything between Weapon and Optimal Stats
    extra_idx = -1
    extra_label = ""
    for i in range(i_name + 1, i_stats):
        if i != i_tier and header_cells[i]:
            extra_idx = i
            extra_label = header_cells[i]
            break
    # Or after damage if before weight (Katana has Status here)
    if extra_idx == -1:
        for i in range(i_dmg + 1, i_weight):
            if header_cells[i]:
                extra_idx = i
                extra_label = header_cells[i]
                break

    weapons: list[Weapon] = []
    for row in table[1:]:
        cells = split_row(row)
        tier = re.sub(r"\*+", "", cells[i_tier]).strip()
        name = cells[i_name].strip()
        stats = cells[i_stats].strip()
        ar = cells[i_ar].strip()
        dmg = cells[i_dmg].strip()
        weight_str = cells[i_weight].strip()
        try:
            weight = float(NUM_RE.search(weight_str).group())
        except AttributeError:
            weight = 0.0
        extra = cells[extra_idx].strip() if extra_idx >= 0 else ""

        weapons.append(
            Weapon(
                tier=tier,
                name=name,
                weapon_class=meta["weapon_class"],
                optimal_stats=stats,
                ar=ar,
                ar_peak=peak_number(ar),
                damage_1h=dmg,
                damage_peak=peak_number(dmg),
                weight=weight,
                extra=extra,
                extra_label=extra_label,
                damage_label=meta["damage_label"],
                source_guide=meta["weapon_class"] + " Guide",
                source_url=f"../../guides/{meta['slug']}/#{meta['section']}",
            )
        )
    return weapons


def build() -> dict:
    weapons: list[Weapon] = []
    for meta in GUIDES:
        weapons.extend(parse_guide(meta))
    return {
        "schema_version": 1,
        "generated_by": "tools/extract_weapons.py",
        "weapon_count": len(weapons),
        "weapon_classes": sorted({w.weapon_class for w in weapons}),
        "tiers": ["S", "A", "B", "C", "D", "E", "F"],
        "weapons": [asdict(w) for w in weapons],
    }


def write_json(data: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if committed JSON is stale relative to markdown sources.",
    )
    args = parser.parse_args()

    data = build()
    new_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not OUTPUT_PATH.exists():
            print(f"::error::{OUTPUT_PATH} does not exist. Run tools/extract_weapons.py.")
            return 1
        existing = OUTPUT_PATH.read_text(encoding="utf-8")
        if existing != new_text:
            print(
                f"::error::{OUTPUT_PATH} is out of date. "
                f"Run `python tools/extract_weapons.py` and commit the result."
            )
            return 1
        print(f"OK: {OUTPUT_PATH} matches markdown sources "
              f"({data['weapon_count']} weapons across {len(data['weapon_classes'])} classes).")
        return 0

    write_json(data)
    print(f"Wrote {OUTPUT_PATH} ({data['weapon_count']} weapons).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
