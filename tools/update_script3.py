import re

file_path = 'tools/translate_script.py'
text = open(file_path, encoding='utf-8').read()

updates = {
    '사자의 발톱': '사자 베기',
    '이중 베기': '2연속 베기',
    '정방형 공격': '사각에서의 일격',
    '사각에서 일격': '사각에서의 일격',
    '번개 돌진': '벼락 양',
    '홍염 공격': '염격',
    '결의': '디터미네이션',
    '왕기사의 결의': '도읍 기사의 결의',
    '안개새의 춤': '안개의 맹금',
    '꿰뚫는 찌르기': '관통 찌르기',
    '피바람 베기': '피의 참격',
    '야생 강타': '난격',
    '회전 강타': '회전격',
    '전투의 외침': '워 크라이',
    '독나방 비행': '독나방은 두 번 춤춘다',
    '붉은 갈기의 불꽃': '적사자의 화염',
    '신수 서리밟기': '신수 서리 밟기',
    '로레타의 베기': '로레타의 참격',
    '신을 죽이는 자의 대검': '신 사냥의 검',
    '별줄무늬 검': '연성검',
    '응시하는 손가락': '바라보는 손가락',
    '장식 직검': '의장 직검',
    'F기사 대검': '불의 기사 대검'
}

for k, v in updates.items():
    if f'"{k}":' in text:
        text = re.sub(fr'"{k}":\s*".*?"', f'"{k}": "{v}"', text)
    else:
        match = re.search(r'\}\s*def translate_file', text)
        if match:
            text = text[:match.start()] + f',\n    "{k}": "{v}"\n' + text[match.start():]

open(file_path, 'w', encoding='utf-8').write(text)
print('Updated translate_script.py successfully.')
