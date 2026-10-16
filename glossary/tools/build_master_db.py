"""
Build the item master (dimension) table as a SQLite database.

    python glossary/tools/build_master_db.py            # writes glossary/master.db
    python glossary/tools/build_master_db.py --out some.db

- Every row of glossary/inputs/*.csv becomes one row of item_master (the full item list is the
  spine of the table). If an output file for a category exists, its translations are joined in
  (after check_glossary validation). If it does not exist yet, those rows get status 'pending'.
- The database is rebuilt from scratch on every run, so running it twice gives the same result.
- Standard library only.
"""
import argparse
import csv
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_glossary as cg  # noqa: E402

DEFAULT_DB = cg.GLOSSARY_DIR / "master.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE lookup_category (category TEXT PRIMARY KEY);
CREATE TABLE lookup_status   (status   TEXT PRIMARY KEY);
CREATE TABLE lookup_source   (source   TEXT PRIMARY KEY);

CREATE TABLE item_master (
    category   TEXT    NOT NULL REFERENCES lookup_category(category),
    item_id    TEXT    NOT NULL,                       -- id exactly as in the csv (terms use 'weaponType:Katana')
    game_id    INTEGER,                                -- item_id as a number when it is numeric, else NULL
    en_name    TEXT    NOT NULL,
    ko_name    TEXT,
    group_name TEXT    NOT NULL,                       -- weapon class / armor part / goods category ...
    is_dlc     INTEGER NOT NULL CHECK (is_dlc IN (0, 1)),
    status     TEXT    NOT NULL REFERENCES lookup_status(status),
    source     TEXT    REFERENCES lookup_source(source),
    note       TEXT,
    PRIMARY KEY (category, item_id),
    CHECK (
        (status IN ('ok', 'unsure') AND ko_name IS NOT NULL AND ko_name <> '')
        OR (status IN ('missing', 'pending') AND ko_name IS NULL)
    )
);
CREATE INDEX idx_item_master_en ON item_master (category, en_name);
CREATE INDEX idx_item_master_ko ON item_master (ko_name);

CREATE VIEW v_translation_coverage AS
SELECT category,
       COUNT(*)                                          AS total,
       SUM(status = 'ok')                                AS ok,
       SUM(status = 'unsure')                            AS unsure,
       SUM(status = 'missing')                           AS missing,
       SUM(status = 'pending')                           AS pending,
       ROUND(100.0 * SUM(status = 'ok') / COUNT(*), 1)   AS pct_ok
FROM item_master
GROUP BY category;

CREATE VIEW v_needs_review AS
SELECT category, item_id, en_name, ko_name, status, note
FROM item_master
WHERE status IN ('unsure', 'missing')
ORDER BY category, status, item_id;
"""


def to_game_id(item_id: str):
    return int(item_id) if item_id.isdigit() else None


def load_rows(category: str):
    """Rows for one category, or None if validation fails."""
    _, inputs = cg.read_csv(cg.INPUT_DIR / f"{category}.csv")
    out_path = cg.OUTPUT_DIR / f"{category}.csv"
    translated = {}
    if out_path.exists():
        errors, _, _ = cg.check_category(category)
        if errors:
            print(f"[{category}] 검증 오류가 {len(errors)}개 있어서 DB를 만들 수 없습니다. "
                  f"먼저 check_glossary.py {category} 를 돌려 고치세요.")
            return None
        _, outputs = cg.read_csv(out_path)
        translated = {r["id"]: r for r in outputs}

    rows = []
    for r in inputs:
        t = translated.get(r["id"])
        if t is None:
            status, ko, source, note = "pending", None, None, None
        else:
            status = t["status"]
            ko = t["ko"].strip() or None
            source = t["source"] or None
            note = t["note"].strip() or None
        rows.append((category, r["id"], to_game_id(r["id"]), r["en"], ko, r["group"], int(r["dlc"] or 0), status, source, note))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=DEFAULT_DB, help="만들 DB 파일 (기본 glossary/master.db)")
    args = parser.parse_args(argv)
    cg.ensure_utf8_stdout()

    all_rows = []
    for category in cg.CATEGORIES:
        rows = load_rows(category)
        if rows is None:
            return 1
        all_rows.extend(rows)

    if args.out.exists():
        args.out.unlink()
    con = sqlite3.connect(args.out)
    try:
        con.executescript(SCHEMA)
        con.executemany("INSERT INTO lookup_category VALUES (?)", [(c,) for c in cg.CATEGORIES])
        con.executemany("INSERT INTO lookup_status VALUES (?)", [(s,) for s in sorted(cg.STATUSES | {"pending"})])
        con.executemany("INSERT INTO lookup_source VALUES (?)", [(s,) for s in sorted(cg.SOURCES)])
        con.executemany("INSERT INTO item_master VALUES (?,?,?,?,?,?,?,?,?,?)", all_rows)
        con.commit()
        fk_problems = con.execute("PRAGMA foreign_key_check").fetchall()
        if fk_problems:
            print("외래 키 오류:", fk_problems[:5])
            return 1
        print(f"{args.out} 를 만들었습니다 ({len(all_rows)}행)")
        for row in con.execute("SELECT * FROM v_translation_coverage"):
            print("  {0}: 전체 {1} · ok {2} · unsure {3} · missing {4} · pending {5} ({6}% ok)".format(*row))
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
