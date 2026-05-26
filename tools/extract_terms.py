import sys
from pathlib import Path

files_to_check = [
    "ruleset/Tourney_Ruleset_KR.md",
    "ruleset/Alternative_Ruleset_KR.md",
    "ruleset/Standard_DEN_Restrictions_KR.md",
    "info/PvP_Lexicon_KR.md"
]

out = []

for f_path in files_to_check:
    p = Path(f_path)
    if not p.exists():
        continue
    out.append(f"==== {p.name} ====")
    text = p.read_text(encoding="utf-8")
    capture = False
    category = ""
    for line in text.splitlines():
        if line.startswith("## ") and ("주문" in line or "전회" in line or "탈리스만" in line or "마술" in line or "기도" in line or "AoW" in line or "Spells" in line or "Talismans" in line):
            capture = True
            category = line.strip()
            out.append(f"\n[{category}]")
        elif line.startswith("## ") and capture:
            capture = False
        
        if capture and ("-" in line or "|" in line):
            # Only append lines that might contain an item
            if line.strip() and not line.strip().startswith("| --"):
                out.append(line.strip())

Path("extracted_terms.txt").write_text("\n".join(out), encoding="utf-8")
