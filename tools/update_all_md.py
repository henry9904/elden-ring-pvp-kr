import os
from pathlib import Path

# We will import TRANSLATIONS from translate_script
import sys
sys.path.append(os.path.dirname(__file__))
from translate_script import TRANSLATIONS

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories to search
DIRS = ['info', 'ruleset', 'guides']

# Sort keys by length descending to prevent partial match overwrites
sorted_keys = sorted(TRANSLATIONS.keys(), key=len, reverse=True)

count = 0
for d in DIRS:
    dir_path = REPO_ROOT / d
    if not dir_path.exists():
        continue
    for md_file in dir_path.glob('**/*_KR*.md'):
        text = md_file.read_text(encoding='utf-8', errors='ignore')
        original_text = text
        for key in sorted_keys:
            val = TRANSLATIONS[key]
            text = text.replace(key, val)
        
        if text != original_text:
            md_file.write_text(text, encoding='utf-8')
            print(f"Updated {md_file.name}")
            count += 1

print(f"Total {count} files updated.")
