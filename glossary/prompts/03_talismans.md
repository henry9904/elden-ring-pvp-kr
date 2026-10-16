# 작업 3: 탈리스만 (154개)

먼저 `glossary/prompts/00_common.md`를 끝까지 읽고 그 규칙을 따르세요.

## 할 일

- 입력: `glossary/inputs/talismans.csv` (154행: `id,en,group,dlc`)
- 출력: `glossary/outputs/talismans.csv`
- 보는 FMG는 `AccessoryName`입니다.

## 탈리스만에서 특히 조심할 것

- `+1`, `+2`, `+3`이 붙은 같은 계열 탈리스만(`Crimson Amber Medallion +1` 등)은 한국어 이름도 번호가 붙는 규칙이 있습니다. 규칙을 추측해서 채우지 말고 id마다 확인하세요.
- 게임에서 `Talisman`이라는 단어가 이름에 들어가는 것과 안 들어가는 것이 섞여 있습니다. 입력의 영어 이름을 기준으로 하세요.

## 검증

```bash
python glossary/tools/check_glossary.py talismans
```
