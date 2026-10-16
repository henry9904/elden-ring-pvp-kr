# 엘든 링 한영 대응표 만들기

영어 이름 1,632개(무기 487, 방어구 722, 탈리스만 154, 소비 아이템·주문·위대한 룬 194, 기본 용어 75)에 대해 한국어판 공식 표기를 찾아 표로 만드는 작업입니다.
`tools/translate_script.py`의 `TRANSLATIONS`를 땜질하는 대신, 한 번 제대로 만든 표를 기준으로 삼으려는 목적입니다.

## 폴더

```text
glossary/
  inputs/    영어 이름 목록 (id, 영어 이름). 수정하지 않는다
  outputs/   카테고리별 결과 (작업자가 채운다)
  prompts/   AI 에이전트에게 줄 프롬프트 (공통 규칙 + 카테고리 5개)
  tools/     check_glossary.py  결과 검증·합치기
  items.csv  모든 카테고리를 합친 최종 표 (검증을 통과하면 생김)
```

## 작업 방법 (누구의 PC에서든 같음)

준비물은 이 저장소와 Python 3.8 이상뿐입니다. 경로가 PC마다 다를 수 있는 부분(게임 설치 위치 등)은 프롬프트가 에이전트에게 직접 찾도록 시킵니다.

1. 이 저장소를 받습니다(clone).
2. 저장소 폴더에서 AI 에이전트(Codex, Claude Code 등)를 엽니다.
3. 카테고리 하나를 골라 아래 문장을 에이전트에게 그대로 붙여 넣습니다. 카테고리끼리는 서로 영향이 없어서 **여러 에이전트에 나눠 동시에** 시켜도 됩니다.

   ```text
   glossary/prompts/01_weapons.md 를 읽고 그대로 작업해 주세요.
   ```

4. 에이전트가 끝나면 직접 검증합니다. 오류가 0이어야 합니다.

   ```bash
   python glossary/tools/check_glossary.py weapons
   ```

5. 모든 카테고리가 끝나면 합칩니다.

   ```bash
   python glossary/tools/check_glossary.py all --merge
   ```

| 프롬프트 | 입력 | 출력 |
|---|---|---|
| `prompts/01_weapons.md` | `inputs/weapons.csv` (487) | `outputs/weapons.csv` |
| `prompts/02_armor.md` | `inputs/armor.csv` (722) | `outputs/armor.csv` |
| `prompts/03_talismans.md` | `inputs/talismans.csv` (154) | `outputs/talismans.csv` |
| `prompts/04_goods.md` | `inputs/goods.csv` (194) | `outputs/goods.csv` |
| `prompts/05_terms.md` | `inputs/terms.csv` (75) | `outputs/terms.csv` |

공통 규칙은 `prompts/00_common.md`에 있습니다. 카테고리 프롬프트가 가장 먼저 읽게 되어 있습니다.

## 어떻게 찾나

- **방법 A(우선)**: 엘든 링이 설치된 PC에서 게임 파일의 한국어/영어 텍스트를 같은 id로 짝지어 뽑습니다. 공식 표기가 그대로 나옵니다. 텍스트 묶음을 푸는 공개 도구가 필요합니다.
- **방법 B(대체)**: 게임 파일을 쓸 수 없을 때 나무위키 등 웹에서 확인합니다.

방법 A가 가능한 PC에서 한 번 돌리는 것이 가장 정확합니다. 한 PC에서 일부만 되면, 되는 카테고리만 `outputs/`에 채워서 합쳐도 됩니다.

## 결과 파일 형식

```text
id,en,ko,status,source,note
1000000,Dagger,단검,ok,game-text,
```

- `status`: `ok`(확인함) / `unsure`(불확실, note에 이유) / `missing`(못 찾음, ko는 비움)
- `source`: `game-text` / `namu` / `other`
- `id`와 `en`은 `inputs/`와 똑같아야 하고, 행 수와 순서도 같아야 합니다.

## 입력 목록의 출처

`inputs/*.csv`의 영어 이름과 id는 `er-planner` 프로젝트가 가진 무기·방어구·탈리스만·버프 데이터에서 뽑았습니다. 소비 아이템과 주문은 그 프로젝트가 다루는 194개뿐이고, 게임의 전체 아이템 목록이 아닙니다. 범위를 넓히려면 `inputs/`에 같은 형식(`id,en,group,dlc`)으로 파일을 추가하고 `tools/check_glossary.py`의 `CATEGORIES`에 이름을 더하면 됩니다.

## 이 표를 쓰는 곳

- `tools/translate_script.py`: `TRANSLATIONS` 딕셔너리 대신 `items.csv`를 읽도록 바꾸는 것이 다음 단계입니다. 바꾸기 전에는 dry-run으로 달라지는 곳만 확인합니다.
