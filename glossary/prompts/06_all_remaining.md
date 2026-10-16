# 작업 6: 나머지 전부 한 번에 (방어구 · 탈리스만 · 소비 아이템 · 기본 용어)

먼저 `glossary/prompts/00_common.md`를 끝까지 읽고 그 규칙을 따르세요.

한 에이전트가 아래 네 가지를 이어서 처리합니다. 카테고리마다 세부 지시는 해당 파일에 있으니 각각 읽고 따르세요.

| 순서 | 지시서 | 입력 | 출력 |
|---|---|---|---|
| 1 | `glossary/prompts/02_armor.md` | `inputs/armor.csv` (722) | `outputs/armor.csv` |
| 2 | `glossary/prompts/03_talismans.md` | `inputs/talismans.csv` (154) | `outputs/talismans.csv` |
| 3 | `glossary/prompts/04_goods.md` | `inputs/goods.csv` (194) | `outputs/goods.csv` |
| 4 | `glossary/prompts/05_terms.md` | `inputs/terms.csv` (75) | `outputs/terms.csv` |

## 진행 방법

1. 방법 A(게임 파일)를 쓸 수 있다면, 텍스트 묶음을 **한 번만** 풀고 네 카테고리가 같이 씁니다. 카테고리마다 다시 풀지 마세요. 풀어 둔 임시 파일은 `glossary/` 밖(예: 시스템 임시 폴더)에 두고, 저장소에 넣지 않습니다.
2. 카테고리 하나를 끝낼 때마다 바로 검증합니다.

   ```bash
   python glossary/tools/check_glossary.py armor
   ```

   오류가 0이 된 뒤에 다음 카테고리로 넘어갑니다. 검증 이름은 `armor`, `talismans`, `goods`, `terms`입니다.
3. 중간에 멈춰야 하면 이미 끝난 카테고리의 파일은 그대로 두고, 어디까지 했는지 보고합니다. 다음 에이전트가 이어서 하게 됩니다. 이미 `glossary/outputs/`에 검증을 통과한 파일이 있는 카테고리는 다시 하지 않고 건너뜁니다.
4. 무기(`weapons`)는 이 작업에 포함되지 않습니다. `glossary/outputs/weapons.csv`가 있으면 그대로 두세요.

## 전부 끝나면

1. 합치기와 DB 만들기를 돌립니다.

   ```bash
   python glossary/tools/check_glossary.py all --merge
   python glossary/tools/build_master_db.py
   ```

   `weapons.csv`가 아직 없으면 `all`은 무기에서 "출력 파일이 아직 없습니다"라고 알립니다. 그건 이 작업의 문제가 아니니 그대로 보고하면 됩니다.
2. 아래를 보고합니다.
   - 카테고리별로 어느 방법(A/B)을 썼는지
   - 카테고리별 ok/unsure/missing 개수
   - `unsure`와 `missing` 중 눈에 띄는 것 몇 개와 이유
   - `build_master_db.py`가 출력한 `v_translation_coverage` 요약
3. 결과 CSV 파일만 만들어 두고, git 커밋이나 push는 하지 않습니다.
