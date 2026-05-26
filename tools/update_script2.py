import re
import os

file_path = 'tools/translate_script.py'
text = open(file_path, encoding='utf-8').read()

# If 왕가의 그레이트소드 is mapped to 왕가의 대검, remove it or change it
text = text.replace('"왕가의 그레이트소드": "왕가의 대검"', '"왕가의 그레이트소드": "왕가의 그레이트소드"')

updates = {
    '별 주먹': '가시 철구권',
    '펄션': '펄선',
    '왕가의 대검': '왕가의 그레이트소드',
    '흉조의 큰 칼': '흉조의 대도',
    '수도승의 화염검': '승병의 화염도',
    '수인의 큰 칼': '수인의 대곡도'
}

for k, v in updates.items():
    if f'"{k}":' in text:
        text = re.sub(fr'"{k}":\s*".*?"', f'"{k}": "{v}"', text)
    else:
        match = re.search(r'\}\s*def translate_file', text)
        if match:
            text = text[:match.start()] + f',\n    "{k}": "{v}"\n' + text[match.start():]

open(file_path, 'w', encoding='utf-8').write(text)
print('Updated translate_script.py')
