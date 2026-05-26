"""
Apply TRANSLATIONS from translate_script across all KR markdown files.

Reuses the token-boundary safe replacement logic from translate_script;
defaults to dry-run. Pass --apply to write.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(__file__))
from translate_script import TRANSLATIONS, apply_translations, _audit

REPO_ROOT = Path(__file__).resolve().parent.parent

# Explicit directories — extend deliberately.
SEARCH_DIRS = ["info", "ruleset", "guides"]
# Only files matching this glob within each dir are eligible.
KR_GLOB = "**/*_KR*.md"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--apply", action="store_true",
        help="Write changes to disk. Without this flag, runs in dry-run mode.",
    )
    args = ap.parse_args()

    _audit(TRANSLATIONS)

    files_changed = 0
    total = 0
    for d in SEARCH_DIRS:
        dir_path = REPO_ROOT / d
        if not dir_path.exists():
            continue
        for md_file in sorted(dir_path.glob(KR_GLOB)):
            original = md_file.read_text(encoding="utf-8")
            new_text, count = apply_translations(original, TRANSLATIONS)
            if count == 0:
                continue
            files_changed += 1
            total += count
            rel = md_file.relative_to(REPO_ROOT)
            if args.apply:
                md_file.write_text(new_text, encoding="utf-8")
                print(f"  ✓ wrote {rel}  ({count} replacements)")
            else:
                print(f"  would change {rel}  ({count} replacements)")

    mode = "applied" if args.apply else "dry-run"
    print(f"\n[{mode}] {total} replacements across {files_changed} file(s)")
    if not args.apply and total:
        print("Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
