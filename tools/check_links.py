import glob
import re
from pathlib import Path

def main():
    md_files = glob.glob('**/*.md', recursive=True)
    valid_files = set([Path(f).as_posix() for f in md_files])
    
    link_re = re.compile(r'\[.*?\]\((?!http)(.*?)\)')
    errors = 0
    
    for f in md_files:
        if 'site\\' in f or 'docs\\' in f: continue # ignore build artifacts
        text = Path(f).read_text(encoding='utf-8', errors='ignore')
        current_dir = Path(f).parent
        
        for line_num, line in enumerate(text.splitlines(), 1):
            for match in link_re.finditer(line):
                link = match.group(1).split('#')[0] # remove anchor
                if not link: continue # internal anchor only like (#section)
                if link.endswith('/'): link = link + 'index.md' # simple resolution
                
                target_path = (current_dir / link).resolve()
                try:
                    rel_target = target_path.relative_to(Path('.').resolve()).as_posix()
                    if rel_target not in valid_files and target_path.is_file() == False:
                        print(f"{f}:{line_num}: Broken link to '{link}' -> resolved as {rel_target}")
                        errors += 1
                except ValueError:
                    print(f"{f}:{line_num}: Link escapes repo '{link}'")
                    errors += 1

    if errors == 0:
        print("OK: No broken internal links found.")
    else:
        print(f"Found {errors} broken links.")

if __name__ == '__main__':
    main()
