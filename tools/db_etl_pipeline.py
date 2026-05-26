import sqlite3
import json
import argparse
from pathlib import Path

from extract_weapons import build as build_weapons
from extract_combos import parse_md as parse_combos

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "assets" / "data" / "elden_ring.db"
JSON_OUT_DIR = REPO_ROOT / "assets" / "data"

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS weapons')
    cursor.execute('DROP TABLE IF EXISTS setups_en')
    cursor.execute('DROP TABLE IF EXISTS combos_en')
    cursor.execute('DROP TABLE IF EXISTS setups_kr')
    cursor.execute('DROP TABLE IF EXISTS combos_kr')
    
    cursor.execute('''
    CREATE TABLE weapons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tier TEXT,
        name TEXT,
        weapon_class TEXT,
        optimal_stats TEXT,
        ar TEXT,
        ar_peak INTEGER,
        damage_1h TEXT,
        damage_peak INTEGER,
        weight REAL,
        extra TEXT,
        extra_label TEXT,
        damage_label TEXT,
        source_guide TEXT,
        source_url TEXT
    )
    ''')
    
    for lang in ["en", "kr"]:
        cursor.execute(f'''
        CREATE TABLE setups_{lang} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setup_name TEXT,
            weapon_class TEXT,
            main_hand TEXT,
            off_hand TEXT
        )
        ''')
        cursor.execute(f'''
        CREATE TABLE combos_{lang} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setup_id INTEGER,
            combo TEXT,
            tightness TEXT,
            FOREIGN KEY(setup_id) REFERENCES setups_{lang}(id)
        )
        ''')
    conn.commit()

def load_weapons(conn):
    data = build_weapons()
    cursor = conn.cursor()
    for w in data['weapons']:
        cursor.execute('''
        INSERT INTO weapons (tier, name, weapon_class, optimal_stats, ar, ar_peak, damage_1h, damage_peak, weight, extra, extra_label, damage_label, source_guide, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (w['tier'], w['name'], w['weapon_class'], w['optimal_stats'], w['ar'], w['ar_peak'], w['damage_1h'], w['damage_peak'], w['weight'], w['extra'], w['extra_label'], w['damage_label'], w['source_guide'], w['source_url']))
    conn.commit()
    print(f"[Load] Inserted {len(data['weapons'])} weapons into DB.")

def load_combos(conn):
    en_path = REPO_ROOT / "info" / "True_Combos_Mugen_EN.archive.md"
    kr_path = REPO_ROOT / "info" / "True_Combos_Mugen_KR.archive.md"
    
    en_data = parse_combos(en_path, "Any")
    kr_data = parse_combos(kr_path, "조건 없음 (Any)")
    
    cursor = conn.cursor()
    
    def insert_setups(data, lang):
        setup_count = 0
        combo_count = 0
        for s in data['setups']:
            cursor.execute(f'''
            INSERT INTO setups_{lang} (setup_name, weapon_class, main_hand, off_hand)
            VALUES (?, ?, ?, ?)
            ''', (s['id'], s['weapon_class'], s['main_hand'], s['off_hand']))
            
            setup_row_id = cursor.lastrowid
            
            setup_count += 1
            for c in s['combos']:
                cursor.execute(f'''
                INSERT INTO combos_{lang} (setup_id, combo, tightness)
                VALUES (?, ?, ?)
                ''', (setup_row_id, c['combo'], c['tightness']))
                combo_count += 1
        return setup_count, combo_count

    en_s, en_c = insert_setups(en_data, "en")
    kr_s, kr_c = insert_setups(kr_data, "kr")
    conn.commit()
    print(f"[Load] Inserted {en_s} EN setups ({en_c} combos) and {kr_s} KR setups ({kr_c} combos).")
    
    return en_data, kr_data  # return original structure info for export

def export_json(conn, en_schema, kr_schema):
    cursor = conn.cursor()
    
    # 1. Export Weapons
    cursor.execute("SELECT * FROM weapons")
    cols = [desc[0] for desc in cursor.description]
    weapons_rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
    for row in weapons_rows:
        del row['id']
    
    weapon_classes = sorted(list(set(w['weapon_class'] for w in weapons_rows)))
    weapons_payload = {
        "schema_version": 1,
        "generated_by": "tools/db_etl_pipeline.py",
        "weapon_count": len(weapons_rows),
        "weapon_classes": weapon_classes,
        "tiers": ["S", "A", "B", "C", "D", "E", "F"],
        "weapons": weapons_rows,
    }
    with open(JSON_OUT_DIR / "weapons.json", "w", encoding="utf-8") as f:
        json.dump(weapons_payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"[Export] weapons.json generated from DB.")

    # 2. Export Combos
    for lang, schema_data in [("en", en_schema), ("kr", kr_schema)]:
        cursor.execute(f"SELECT * FROM setups_{lang}")
        cols = [desc[0] for desc in cursor.description]
        setups_rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        
        for setup in setups_rows:
            setup_row_id = setup.pop('id')
            setup['id'] = setup.pop('setup_name')
            
            cursor.execute(f"SELECT combo, tightness FROM combos_{lang} WHERE setup_id = ?", (setup_row_id,))
            ccols = [desc[0] for desc in cursor.description]
            setup['combos'] = [dict(zip(ccols, row)) for row in cursor.fetchall()]
            
        combo_payload = {
            "schema_version": schema_data['schema_version'],
            "generated_by": "tools/db_etl_pipeline.py",
            "setup_count": len(setups_rows),
            "weapon_classes": schema_data['weapon_classes'],
            "main_hands": schema_data['main_hands'],
            "off_hands": schema_data['off_hands'],
            "setups": setups_rows,
        }
        with open(JSON_OUT_DIR / f"combos_{lang}.json", "w", encoding="utf-8") as f:
            json.dump(combo_payload, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"[Export] combos_{lang}.json generated from DB.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--export", action="store_true", help="Export to JSON after loading")
    args = parser.parse_args()

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    
    init_db(conn)
    load_weapons(conn)
    en_schema, kr_schema = load_combos(conn)
    print(f"[Success] DB Pipeline executed at {DB_PATH.relative_to(REPO_ROOT)}")
    
    if args.export:
        export_json(conn, en_schema, kr_schema)
        
    conn.close()

if __name__ == '__main__':
    main()
