"""
Export the glossary into the files other tools and the website read.

    python glossary/tools/export_names.py           # (re)generate the export files
    python glossary/tools/export_names.py --check   # fail if the files on disk differ (used by CI)

Source of truth: glossary/inputs/*.csv + glossary/outputs/*.csv (validated by check_glossary).
Never edit the generated files by hand; edit outputs/ and run this script again.

Generated files:
    glossary/exports/names.csv        category,id,en,ko,group,dlc,status,source
    glossary/exports/names.txt        "한국어 = English" lines grouped by category
    assets/data/glossary_names.json   used by docs/tools/glossary-explorer.md

Standard library only.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_glossary as cg  # noqa: E402

REPO_ROOT = cg.GLOSSARY_DIR.parent
CSV_PATH = cg.GLOSSARY_DIR / "exports" / "names.csv"
TXT_PATH = cg.GLOSSARY_DIR / "exports" / "names.txt"
JSON_PATH = REPO_ROOT / "assets" / "data" / "glossary_names.json"

LABELS = {
    "weapons": ("무기", "Weapons"),
    "armor": ("방어구", "Armor"),
    "talismans": ("탈리스만", "Talismans"),
    "goods": ("버프·소비·주문", "Consumables & Spells"),
    "terms": ("용어", "Terms"),
}


def load_rows():
    """All rows in category order, input order. Raises SystemExit if validation fails."""
    rows = []
    for category in cg.CATEGORIES:
        errors, _, _ = cg.check_category(category)
        if errors:
            print(f"[{category}] 검증 오류 {len(errors)}개 — 먼저 check_glossary.py {category} 를 고치세요.")
            for line in errors[:5]:
                print("  -", line)
            raise SystemExit(1)
        _, inputs = cg.read_csv(cg.INPUT_DIR / f"{category}.csv")
        _, outputs = cg.read_csv(cg.OUTPUT_DIR / f"{category}.csv")
        by_id = {r["id"]: r for r in outputs}
        for r in inputs:
            o = by_id[r["id"]]
            rows.append(
                {
                    "category": category,
                    "id": r["id"],
                    "en": r["en"],
                    "ko": o["ko"].strip(),
                    "group": r["group"],
                    "dlc": int(r["dlc"] or 0),
                    "status": o["status"],
                    "source": o["source"],
                }
            )
    return rows


def csv_text(rows):
    import csv
    import io

    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["category", "id", "en", "ko", "group", "dlc", "status", "source"])
    for r in rows:
        w.writerow([r["category"], r["id"], r["en"], r["ko"], r["group"], r["dlc"], r["status"], r["source"]])
    return buf.getvalue()


def txt_text(rows):
    translated = [r for r in rows if r["ko"]]
    lines = [f"# 엘든 링 이름 (한국어 = English) — {len(translated)}개", ""]
    for category in cg.CATEGORIES:
        group = [r for r in translated if r["category"] == category]
        lines.append(f"[{LABELS[category][0]}] {len(group)}개")
        lines.extend(f"{r['ko']} = {r['en']}" for r in group)
        lines.append("")
    return "\n".join(lines)


def json_text(rows):
    head = {
        "schema_version": 1,
        "generated_by": "glossary/tools/export_names.py",
        "count": len(rows),
        "categories": [{"key": c, "ko": LABELS[c][0], "en": LABELS[c][1]} for c in cg.CATEGORIES],
    }
    head_json = json.dumps(head, ensure_ascii=False, indent=2)
    items = ",\n".join("    " + json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows)
    return head_json[:-2] + ',\n  "items": [\n' + items + "\n  ]\n}\n"


def expected_files():
    rows = load_rows()
    return {CSV_PATH: csv_text(rows), TXT_PATH: txt_text(rows), JSON_PATH: json_text(rows)}


def main(argv=None):
    cg.ensure_utf8_stdout()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="디스크의 파일이 마스터에서 만든 결과와 같은지 검사")
    args = parser.parse_args(argv)

    files = expected_files()
    if args.check:
        stale = []
        for path, text in files.items():
            on_disk = path.read_text(encoding="utf-8") if path.exists() else None
            if on_disk != text:
                stale.append(path.relative_to(REPO_ROOT))
        if stale:
            print("내보내기 파일이 마스터와 다릅니다. python glossary/tools/export_names.py 를 실행하세요:")
            for p in stale:
                print("  -", p)
            return 1
        print(f"내보내기 파일 {len(files)}개가 마스터와 같습니다.")
        return 0

    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        print("썼습니다:", path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
