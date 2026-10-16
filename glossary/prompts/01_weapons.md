# 작업 1: 무기 (487개)

먼저 `glossary/prompts/00_common.md`를 끝까지 읽고 그 규칙을 따르세요.

## 할 일

- 입력: `glossary/inputs/weapons.csv` (487행: `id,en,group,dlc`)
- 출력: `glossary/outputs/weapons.csv`
- `id`는 무기 기본 id입니다. 강화 단계나 변질이 붙은 id가 아니라, 이름 FMG(`WeaponName`)에 있는 id와 같습니다.
- `group`은 무기군 이름(영어)이고, `dlc`가 1이면 DLC 무기입니다. 확인용 정보이고 출력에 넣지 않습니다.

## 무기에서 특히 조심할 것

- 이름이 거의 같은 무기가 많습니다(`Cleanrot Knight's Sword`와 `Cleanrot Spear`, `Rotten Crystal Sword` 등). 반드시 id로 짝지으세요. 이름으로 짝지으면 틀립니다.
- 변질 접두사(`Heavy`, `Keen`, `Fire` 등)가 붙은 이름은 입력에 없습니다. 기본 이름만 다룹니다.
- 한국어판은 같은 영어 단어를 무기군에 따라 다르게 옮기기도 합니다(예: `Spear`, `Greatsword`, `Axe`). 다른 무기의 번역을 보고 추측하지 말고 id마다 확인하세요.
- 방패와 활과 석궁, 지팡이와 인장도 이 목록에 들어 있습니다.

## 검증

```bash
python glossary/tools/check_glossary.py weapons
```
