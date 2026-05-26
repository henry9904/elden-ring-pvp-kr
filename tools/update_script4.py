import re

file_path = 'tools/translate_script.py'
text = open(file_path, encoding='utf-8').read()

# Fix the dictionary
# Replace "결의": "디터미네이션" with "결의, 왕기사의 결의": "디터미네이션, 도읍 기사의 결의"
# Replace "왕기사의 결의": "도읍 기사의 결의" -> remove it, handled above.
# Replace "정방형 공격": "사각에서의 일격" -> "정방형 공격": "준비 자세"

text = re.sub(r'"결의":\s*"디터미네이션"\s*,?', '', text)
text = re.sub(r'"왕기사의 결의":\s*"도읍 기사의 결의"\s*,?', '', text)
text = re.sub(r'"정방형 공격":\s*"사각에서의 일격"', '"정방형 공격": "준비 자세"', text)

# Add the combined replacement
match = re.search(r'\}\s*def translate_file', text)
if match:
    text = text[:match.start()] + ',\n    "결의, 왕기사의 결의": "디터미네이션, 도읍 기사의 결의"\n' + text[match.start():]

open(file_path, 'w', encoding='utf-8').write(text)
print("Dictionary fixed.")
