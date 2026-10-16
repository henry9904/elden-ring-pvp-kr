"""
Validate a glossary output CSV against its input list.

Usage (run from anywhere; paths are resolved relative to this file):
    python glossary/tools/check_glossary.py weapons
    python glossary/tools/check_glossary.py all
    python glossary/tools/check_glossary.py all --merge   # also writes glossary/items.csv

Standard library only, so it runs on any machine with Python 3.8+.
Exit code 0 = no errors (warnings are allowed), 1 = errors found.
"""
import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

GLOSSARY_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = GLOSSARY_DIR / "inputs"
OUTPUT_DIR = GLOSSARY_DIR / "outputs"
MERGED_PATH = GLOSSARY_DIR / "items.csv"

CATEGORIES = ["weapons", "armor", "talismans", "goods", "terms"]
OUTPUT_COLUMNS = ["id", "en", "ko", "status", "source", "note"]
STATUSES = {"ok", "unsure", "missing"}
SOURCES = {"game-text", "namu", "other"}

HANGUL = r"가-힣"
# A token that mixes Hangul with Latin letters, e.g. "Cleanrot 창" is two tokens, but "Cleanrot창" is one.
_MIXED_TOKEN = re.compile(rf"(?=\S*[{HANGUL}])(?=\S*[A-Za-z])\S+")
_LATIN = re.compile(r"[A-Za-z]")


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def check_category(name: str):
    errors, warnings = [], []
    in_path = INPUT_DIR / f"{name}.csv"
    out_path = OUTPUT_DIR / f"{name}.csv"
    if not in_path.exists():
        return ["입력 파일이 없습니다: " + str(in_path)], warnings, None
    if not out_path.exists():
        return ["출력 파일이 아직 없습니다: " + str(out_path)], warnings, None

    _, inputs = read_csv(in_path)
    header, outputs = read_csv(out_path)

    if header != OUTPUT_COLUMNS:
        errors.append(f"머리글이 다릅니다. 기대: {','.join(OUTPUT_COLUMNS)} / 실제: {','.join(header)}")
        return errors, warnings, None

    if len(outputs) != len(inputs):
        errors.append(f"행 수가 다릅니다. 입력 {len(inputs)} / 출력 {len(outputs)}")

    by_id = {}
    for line_no, row in enumerate(outputs, start=2):
        rid = row["id"]
        if rid in by_id:
            errors.append(f"{line_no}행: id {rid} 가 중복됩니다")
        by_id[rid] = row

    for row in inputs:
        out = by_id.get(row["id"])
        if out is None:
            errors.append(f"id {row['id']} ({row['en']}) 가 출력에 없습니다")
            continue
        if out["en"] != row["en"]:
            errors.append(f"id {row['id']}: en 이 입력과 다릅니다 (입력 {row['en']!r} / 출력 {out['en']!r})")

    input_ids = {r["id"] for r in inputs}
    for rid in by_id:
        if rid not in input_ids:
            errors.append(f"출력에 입력에 없는 id 가 있습니다: {rid}")

    ko_to_ids = defaultdict(list)
    counts = {"ok": 0, "unsure": 0, "missing": 0}
    for line_no, row in enumerate(outputs, start=2):
        status, source, ko = row["status"], row["source"], row["ko"].strip()
        label = f"{line_no}행 (id {row['id']}, {row['en']})"
        if status not in STATUSES:
            errors.append(f"{label}: status 가 올바르지 않습니다: {status!r}")
            continue
        counts[status] += 1
        if status == "missing":
            if ko:
                errors.append(f"{label}: status 가 missing 인데 ko 가 있습니다")
            continue
        if not ko:
            errors.append(f"{label}: status 가 {status} 인데 ko 가 비어 있습니다")
            continue
        if source not in SOURCES:
            errors.append(f"{label}: source 가 올바르지 않습니다: {source!r}")
        if status == "unsure" and not row["note"].strip():
            warnings.append(f"{label}: unsure 인데 note 가 비어 있습니다")
        if not re.search(f"[{HANGUL}]", ko) and not re.search(r"\d", ko):
            warnings.append(f"{label}: ko 에 한글이 없습니다: {ko!r}")
        elif _MIXED_TOKEN.search(ko):
            warnings.append(f"{label}: 한글과 영문이 한 단어에 섞여 있습니다: {ko!r}")
        elif _LATIN.search(ko):
            warnings.append(f"{label}: ko 에 영문이 남아 있습니다: {ko!r}")
        if ko == row["en"]:
            warnings.append(f"{label}: ko 가 영어 원문과 같습니다")
        ko_to_ids[ko].append(row["id"])

    for ko, ids in ko_to_ids.items():
        if len(ids) > 1:
            warnings.append(f"같은 한국어 이름 {ko!r} 가 id {', '.join(ids)} 에 쓰였습니다")

    summary = {"total": len(inputs), **counts}
    return errors, warnings, (summary, outputs)


def main(argv=None):
    # 출력을 파이프로 받는 도구(에이전트 등)에서도 한글이 깨지지 않게, 터미널이 아닐 때만 UTF-8 로 고정한다.
    if not sys.stdout.isatty() and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("category", choices=CATEGORIES + ["all"])
    parser.add_argument("--merge", action="store_true", help="오류가 없으면 glossary/items.csv 로 합친다")
    parser.add_argument("--max-lines", type=int, default=30, help="오류·경고를 몇 줄까지 보여줄지 (기본 30)")
    args = parser.parse_args(argv)

    names = CATEGORIES if args.category == "all" else [args.category]
    exit_code = 0
    merged = []
    for name in names:
        errors, warnings, result = check_category(name)
        print(f"== {name} ==")
        if result:
            s = result[0]
            print(f"  전체 {s['total']} · ok {s['ok']} · unsure {s['unsure']} · missing {s['missing']}")
        for title, items in (("오류", errors), ("경고", warnings)):
            if items:
                print(f"  {title} {len(items)}개")
                for line in items[: args.max_lines]:
                    print(f"    - {line}")
                if len(items) > args.max_lines:
                    print(f"    ... 외 {len(items) - args.max_lines}개")
        if errors:
            exit_code = 1
        elif result:
            merged.extend((name, row) for row in result[1])

    if args.merge:
        if exit_code != 0:
            print("오류가 있어서 합치지 않았습니다.")
        else:
            with MERGED_PATH.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["category"] + OUTPUT_COLUMNS)
                for name, row in merged:
                    writer.writerow([name] + [row[c] for c in OUTPUT_COLUMNS])
            print(f"합친 파일을 썼습니다: {MERGED_PATH} ({len(merged)}행)")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
