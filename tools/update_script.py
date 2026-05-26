import re

file_path = 'tools/translate_script.py'
text = open(file_path, encoding='utf-8').read()

updates = {
    '파문 달의 할창': '파문의 도끼창',
    '철 나타': '철 나대',
    '왕가의 그레이트소드': '왕가의 대검',
    '실루리아의 수목': '실루리아의 창',
    '자루 긴 도끼': '긴 자루 도끼',
    '축제의 나타': '축제의 나대',
    '로수스의 도끼': '로제스의 도끼',
    '기사의 대검': '기사 대검',
    '전매의 발톱': '전쟁매의 발톱',
    '벌레의 폴에암': '벌레의 글레이브',
    '워픽': '워 피크',
    '자모르의 곡검': '자미엘의 곡검',
    '자모르 곡검': '자미엘의 곡검',
    '치아 채찍': '이빨 채찍'
}

for k, v in updates.items():
    # If key exists, replace value
    if f'"{k}":' in text:
        text = re.sub(fr'"{k}":\s*".*?"', f'"{k}": "{v}"', text)
    else:
        # insert before the closing brace of TRANSLATIONS
        match = re.search(r'\}\s*def translate_file', text)
        if match:
            text = text[:match.start()] + f',\n    "{k}": "{v}"\n' + text[match.start():]

open(file_path, 'w', encoding='utf-8').write(text)
print('Updated translate_script.py')
