import re

en_text = open('info/True_Combos_Mugen_EN.archive.md', encoding='utf-8').read()
setups = en_text.split('### Setup')

for s in setups:
    if not s.strip() or s.startswith(' ⚔️'): continue
    has_main = '**Main-Hand:**' in s
    has_off = '**Off-Hand:**' in s
    if not has_main or not has_off:
        print(s[:100].strip().encode('ascii', 'ignore').decode())

