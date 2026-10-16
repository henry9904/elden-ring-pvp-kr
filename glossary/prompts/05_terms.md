# 작업 5: 기본 용어 (75개)

먼저 `glossary/prompts/00_common.md`를 끝까지 읽고 그 규칙을 따르세요.

## 할 일

- 입력: `glossary/inputs/terms.csv` (75행: `id,en,group,dlc`)
- 출력: `glossary/outputs/terms.csv`
- 무기군 42종, 변질 13종, 능력치 5종, 속성 5종, 상태이상 6종, 방어구 부위 4종입니다.
- `id`는 `weaponType:Katana`처럼 종류와 영어 이름이 합쳐진 문자열입니다. 그대로 두세요.

## 이 목록은 다른 방법을 씁니다

- 아이템 이름이 아니라 **게임 메뉴 용어**라서, 이름 FMG에는 없을 수 있습니다. 먼저 방법 A에서 찾을 수 있는 곳(장비 메뉴 텍스트 FMG 등)을 확인하고, 없으면 방법 B를 씁니다.
- 무기군 이름은 게임 안의 무기 분류 텍스트(`WeaponName` 옆의 분류 이름 FMG)에 있을 수 있습니다.
- 영어 `en`은 게임의 공식 영어 이름과 다를 수 있습니다(예: `Blood Loss`). 다르면 `note`에 공식 영어 이름을 적으세요. 입력의 `en`은 바꾸지 않습니다.
- 이미 `er-planner` 프로젝트의 `docs/glossary.csv`에 손으로 번역한 값이 있습니다. 비교용으로만 쓰고, 공식 표기와 다르면 공식 표기를 적은 뒤 `note`에 "기존 번역과 다름"이라고 적으세요.

## 검증

```bash
python glossary/tools/check_glossary.py terms
```
