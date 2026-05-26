import re

file_path = 'tools/translate_script.py'
text = open(file_path, encoding='utf-8').read()

updates = {
    '청색 성배병': '푸른 물방울의 성배병',
    '청색 칠지인': '푸른 날개 칠지인',
    '붉은 칠지인': '붉은 날개 칠지인'
}

match = re.search(r'\}\s*def translate_file', text)
if match:
    # Build string
    additions = ""
    for k, v in updates.items():
        additions += f',\n    "{k}": "{v}"'
    
    text = text[:match.start()] + additions + '\n' + text[match.start():]

open(file_path, 'w', encoding='utf-8').write(text)
print('Flask terms added.')
