import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KR_PATH = REPO_ROOT / "info" / "True_Combos_Mugen_KR.archive.md"

TRANSLATIONS = {
    "Antspur Rapier": "개미가시 레이피어",
    "Bandit's Curved Sword": "산적의 곡검",
    "Banished Knight's 그레이트소드": "땅 잃은 기사의 대검",
    "Beastman's Curved Sword": "수인의 곡검",
    "Bloodhound Claws": "사냥개의 발톱",
    "Bloody Helice": "피의 헬리케",
    "Bolt of Gransax": "그랑삭스의 벼락",
    "Butchering Knife": "큰 식칼",
    "Carian Knight's Sword": "카리아 기사의 검",
    "Celebrant's Rib-Rake": "축제의 갈비뼈 갈퀴",
    "Cipher Pata": "비문자의 파타",
    "Clayman's Harpoon": "진흙인의 작살",
    "Cleanrot Knight's Sword": "귀부기사의 검",
    "Cleanrot 창": "귀부기사의 창",
    "Clinging Bone": "매달리는 뼈",
    "Cross-Naginata": "십문자도",
    "Crystal Sword": "결정검",
    "Crystal 창": "결정창",
    "Curved 곤봉": "곡선 곤봉",
    "Death Ritual 창": "죽음 의례의 창",
    "Dragon King's Cragblade": "용왕의 암검",
    "Dragonscale Blade": "용비늘 검",
    "Eclipse Shotel": "일식의 쇼텔",
    "Executioner's Greataxe": "처형인의 대도끼",
    "Falchion": "펄션",
    "Flowing Curved Sword": "유수 곡검",
    "Gargoyle's Black Axe": "가고일의 흑도끼",
    "Gargoyle's Great Axe": "가고일의 대도끼",
    "Ghiza's Wheel": "기자의 수레바퀴",
    "Godskin Peeler": "신의 살갗 쌍날검",
    "Godskin Stitcher": "신의 살갗 꿰매기",
    "Golden Epitaph": "황금 묘비",
    "Grafted Dragon": "접목의 비룡",
    "Grave 낫": "묘지 낫",
    "Great Omenkiller Cleaver": "흉조잡이의 큰 칼",
    "Greataxe": "그레이트 액스",
    "Grossmesser": "그로스메서",
    "Guardian's Swordspear": "수호자의 검창",
    "Halo 낫": "광륜의 낫",
    "Hammer": "해머",
    "Inquisitor's Girandole": "이단 심문관의 촛대",
    "Iron 창": "철창",
    "Katar": "카타르",
    "Knight's 그레이트소드": "기사의 대검",
    "Lazuli Glintstone Sword": "라줄리의 휘석검",
    "Longhaft Axe": "자루 긴 도끼",
    "Longsword": "롱소드",
    "Loretta's War Sickle": "로레타의 전투 낫",
    "Magma Blade": "용암도",
    "Mantis Blade": "사마귀 칼",
    "Marika's Hammer": "마리카의 망치",
    "Meteoric Ore Blade": "운철도",
    "Miquellan Knight's Sword": "미켈라 기사의 검",
    "Mohgwyn's Sacred 창": "모그윈의 성창",
    "Moonveil": "명도 월은",
    "Noble's Slender Sword": "귀인의 세검",
    "Nox Flowing Sword": "녹스의 유수검",
    "Ornamental Straight Sword": "의장 직검",
    "Partisan": "파르티잔",
    "Pike": "파이크",
    "Rapier": "레이피어",
    "Regalia of Eochaid": "에오히드의 보검",
    "Rogier's Rapier": "로지에르의 자검",
    "Rotten Crystal Sword": "부패한 결정검",
    "Rotten Crystal 창": "부패한 결정창",
    "Rusted Anchor": "녹슨 닻",
    "Scavenger's Curved Sword": "시체 뒤지는 자의 곡검",
    "Scimitar": "시미터",
    "Serpent-God's Curved Sword": "뱀신 곡검",
    "Serpent-Hunter": "큰 뱀 사냥꾼",
    "Serpentbone Blade": "뱀뼈의 도",
    "Shamshir": "샴쉬르",
    "Shield of the Guilty": "죄인의 방패",
    "Short 창": "쇼트 스피어",
    "Shotel": "쇼텔",
    "Siluria's Tree": "실루리아의 수목",
    "Sword of Night and Flame": "밤과 불꽃의 검",
    "Sword of St. Trina": "트리나의 검",
    "Treespear": "트리스피어",
    "Unarmed": "맨손",
    "Veteran's Prosthesis": "노장의 의족",
    "Vyke's War 창": "바이크의 전투 창",
    "Warhawk's Talon": "전매의 발톱",
    "Weathered Straight Sword": "풍화된 직검",
    "Wing of Astel": "아스텔의 날개",
    "Winged Greathorn": "날개 달린 큰 뿔",
    "Winged 낫": "날개 낫",
    "가고일의 할버드": "가고일의 도끼창",
    "가고일의 흑 할버드": "가고일의 흑도끼창",
    "가시 창": "가시 창",
    "가시 케스투스": "스파이크 세스타스",
    "갈고리 발톱": "갈고리 발톱",
    "갈래 손도끼": "갈래 손도끼",
    "검 잇기의 대검": "검 잇기의 대검",
    "검은 칼날": "검은 칼날",
    "결정 나이프": "결정 나이프",
    "고리 달린 손가락": "고리 손가락",
    "고원의 도끼": "고원의 도끼",
    "곤봉": "곤봉",
    "군주군의 직검": "군주군의 직검",
    "그레이트소드": "그레이트소드",
    "낙마검": "참마도",
    "낫": "낫",
    "노장의 군기": "노장의 군기",
    "녹스의 흐르는 해머": "녹스의 유수 해머",
    "대거": "대거",
    "대형 나이프": "대형 나이프",
    "독니": "독사의 송곳니",
    "돌 곤봉": "돌 곤봉",
    "뒤틀린 도끼": "뒤틀린 도끼",
    "랜스": "랜스",
    "레두비아": "레두비아",
    "로수스의 도끼": "로제스의 도끼",
    "루체른": "루체른",
    "마그마 뱀룡의 비늘검": "토룡의 비늘검",
    "말레니아의 손": "말레니아의 의수도",
    "말리케스의 흑검": "말리케스의 흑검",
    "맹금의 발톱": "맹금의 발톱",
    "모닝 스타": "모닝 스타",
    "모르곳의 저주검": "모르고트의 저주검",
    "바레의 꽃다발": "바레의 꽃다발",
    "배틀 액스": "배틀 액스",
    "별 부수는 대검": "별 부수는 대검",
    "별주먹": "별 주먹",
    "부호의 검": "비문자의 검",
    "브로드 소드": "브로드 소드",
    "사명의 칼날": "사명의 칼날",
    "사자의 뿔나팔": "사자들의 피리",
    "상아 손낫": "상아 낫",
    "서리날 손도끼": "빙각의 손도끼",
    "숏 소드": "숏 소드",
    "수도승의 불꽃 철퇴": "수도승의 화염 망치",
    "수도승의 불꽃날": "수도승의 화염검",
    "신 사냥의 대검": "신 사냥의 검",
    "암흑의 달 대검": "암월의 대검",
    "야간 기수의 창도": "밤기병의 글레이브",
    "야수인의 식칼": "수인의 큰 칼",
    "역병의 낫창": "벌레의 폴에암",
    "영혼 결합의 검": "나뉘지 않는 쌍생아의 검",
    "왕가의 그레이트소드": "왕가의 그레이트소드",
    "용의 할버드": "용비늘 도끼창",
    "우치가타나": "타도",
    "워픽": "워 피크",
    "유적의 대검": "유적의 대검",
    "자모르 곡검": "자미엘의 곡검",
    "자비의 단검": "자비의 단검",
    "장도": "긴 이빨",
    "전갈의 침": "전갈의 침",
    "전지자의 홀": "기드온의 왕홀",
    "지팡이검": "지팡이검",
    "창도": "글레이브",
    "철 식칼": "철 나타",
    "철구권": "철구권",
    "철퇴": "철퇴",
    "추방 기사의 할버드": "땅 잃은 기사의 도끼창",
    "축제의 손낫": "축제의 낫",
    "축제의 식칼": "축제의 나타",
    "츠바이헨더": "츠바이헨더",
    "친퀘디아": "친퀘디아",
    "케스투스": "세스타스",
    "클레이모어": "클레이모어",
    "턱뼈 도끼": "턱뼈 도끼",
    "트롤 기사의 검": "트롤 기사의 검",
    "트롤의 황금검": "트롤의 황금검",
    "파문 초승달 할버드": "파문 달의 할창",
    "파문 칼날": "파문의 검",
    "파수견의 대검": "파수견의 대검",
    "패링 대거": "패링 대거",
    "폭도 민병대의 낫": "천한 병사의 낫",
    "폭도 민병대의 톱": "천한 병사의 톱",
    "폭풍매의 도끼": "폭풍매의 도끼",
    "피의 강": "시산혈하",
    "피투성이 단도": "피 묻은 단도",
    "할버드": "할버드",
    "핸드 액스": "핸드 액스",
    "혈사냥개의 송곳니": "사냥개의 긴 이빨",
    "협차": "협차",
    "화신의 식칼": "흉조의 큰 칼",
    "황금 할버드": "황금 도끼창",
    "황동 단도": "황동 단도",
    "횃불pole": "횃불대",
    "회석 군주의 검": "백왕의 검",
    "휘석 크리스": "휘석 크리스",
    "흑요석 군주의 대검": "흑왕의 대검",
    "희생의 도끼": "제물의 도끼"
,
    "파문 달의 할창": "파문의 도끼창"
,
    "철 나타": "철 나대"
,
    "실루리아의 수목": "실루리아의 창"
,
    "자루 긴 도끼": "긴 자루 도끼"
,
    "축제의 나타": "축제의 나대"
,
    "기사의 대검": "기사 대검"
,
    "전매의 발톱": "전쟁매의 발톱"
,
    "벌레의 폴에암": "벌레의 글레이브"
,
    "자모르의 곡검": "자미엘의 곡검"
,
    "치아 채찍": "이빨 채찍"
,
    "별 주먹": "가시 철구권"
,
    "펄션": "펄선"
,
    "왕가의 대검": "왕가의 그레이트소드"
,
    "흉조의 큰 칼": "흉조의 대도"
,
    "수도승의 화염검": "승병의 화염도"
,
    "수인의 큰 칼": "수인의 대곡도"
,
    "사자의 발톱": "사자 베기"
,
    "이중 베기": "2연속 베기"
,
    "정방형 공격": "준비 자세"
,
    "사각에서 일격": "사각에서의 일격"
,
    "번개 돌진": "벼락 양"
,
    "홍염 공격": "염격"
,
    
    
    "안개새의 춤": "안개의 맹금"
,
    "꿰뚫는 찌르기": "관통 찌르기"
,
    "피바람 베기": "피의 참격"
,
    "야생 강타": "난격"
,
    "회전 강타": "회전격"
,
    "전투의 외침": "워 크라이"
,
    "독나방 비행": "독나방은 두 번 춤춘다"
,
    "붉은 갈기의 불꽃": "적사자의 화염"
,
    "신수 서리밟기": "신수 서리 밟기"
,
    "로레타의 베기": "로레타의 참격"
,
    "신을 죽이는 자의 대검": "신 사냥의 검"
,
    "별줄무늬 검": "연성검"
,
    "응시하는 손가락": "바라보는 손가락"
,
    "장식 직검": "의장 직검"
,
    "F기사 대검": "불의 기사 대검"
,
    "결의, 왕기사의 결의": "디터미네이션, 도읍 기사의 결의"
,
    "청색 성배병": "푸른 물방울의 성배병",
    "청색 칠지인": "푸른 날개 칠지인",
    "붉은 칠지인": "붉은 날개 칠지인"
}

def translate_file():
    text = KR_PATH.read_text(encoding="utf-8")
    
    # Sort keys by length descending to prevent partial match overwrites
    sorted_keys = sorted(TRANSLATIONS.keys(), key=len, reverse=True)
    
    for key in sorted_keys:
        val = TRANSLATIONS[key]
        text = text.replace(key, val)
        
    KR_PATH.write_text(text, encoding="utf-8")
    print("Translation applied successfully!")

if __name__ == "__main__":
    translate_file()
