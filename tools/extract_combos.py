"""
Extracts true combos from the Mugen Markdown files and produces JSON datasets.

Run with no arguments to (re)generate docs/assets/data/combos_kr.json and combos_en.json.
Run with --check to verify the committed JSON matches the markdown source.
"""
import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KR_PATH = REPO_ROOT / "info" / "True_Combos_Mugen_KR.archive.md"
EN_PATH = REPO_ROOT / "info" / "True_Combos_Mugen_EN.archive.md"
OUT_KR = REPO_ROOT / "assets" / "data" / "combos_kr.json"
OUT_EN = REPO_ROOT / "assets" / "data" / "combos_en.json"

def parse_md(path: Path) -> dict:
    if not path.exists():
        return {}
    
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    
    setups = []
    current_setup = None
    
    for line in lines:
        line = line.strip()
        if line.startswith("### Setup"):
            current_setup = {
                "id": line.replace("### Setup", "").strip(),
                "main_hand": "조건 없음 (Any)",
                "off_hand": "조건 없음 (Any)",
                "combos": []
            }
            setups.append(current_setup)
        elif current_setup:
            if line.startswith("**우수") or line.startswith("**Right Hand"):
                current_setup["main_hand"] = line.split("**")[-1].strip().strip(":")
            elif line.startswith("**좌수") or line.startswith("**Left Hand"):
                current_setup["off_hand"] = line.split("**")[-1].strip().strip(":")
            elif line.startswith("|") and not ("|" in line and "---" in line) and not ("| 콤보" in line) and not ("| Combo" in line):
                parts = [p.strip() for p in line.strip("|").split("|")]
                if len(parts) >= 2:
                    combo = parts[0].replace("`", "").strip()
                    tightness = parts[1].strip()
                    if combo and tightness:
                        current_setup["combos"].append({
                            "combo": combo,
                            "tightness": tightness
                        })
    
    # Post-process to collect unique weapons for filters
    main_hands = set()
    off_hands = set()
    for s in setups:
        for w in s["main_hand"].split(","):
            val = w.strip()
            if val: main_hands.add(val)
        for w in s["off_hand"].split(","):
            val = w.strip()
            if val: off_hands.add(val)
            
    return {
        "schema_version": 1,
        "setup_count": len(setups),
        "main_hands": sorted(list(main_hands)),
        "off_hands": sorted(list(off_hands)),
        "setups": setups
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    kr_data = parse_md(KR_PATH)
    en_data = parse_md(EN_PATH)
    
    kr_json = json.dumps(kr_data, indent=2, ensure_ascii=False) + "\n"
    en_json = json.dumps(en_data, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not OUT_KR.exists() or not OUT_EN.exists():
            print("::error::JSON files missing.")
            return 1
        if OUT_KR.read_text(encoding="utf-8") != kr_json or OUT_EN.read_text(encoding="utf-8") != en_json:
            print("::error::JSON is out of date. Run python tools/extract_combos.py")
            return 1
        print("OK: Combo JSONs match markdown sources.")
        return 0

    OUT_KR.parent.resolve().mkdir(parents=True, exist_ok=True)
    OUT_KR.write_text(kr_json, encoding="utf-8")
    OUT_EN.write_text(en_json, encoding="utf-8")
    print(f"Wrote {OUT_KR} ({kr_data.get('setup_count', 0)} setups)")
    print(f"Wrote {OUT_EN} ({en_data.get('setup_count', 0)} setups)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
