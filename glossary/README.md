# 엘든 링 한영 대응표 만들기

영어 이름 1,632개(무기 487, 방어구 722, 탈리스만 154, 소비 아이템·주문·위대한 룬 194, 기본 용어 75)에 대해 한국어판 공식 표기를 찾아 표로 만드는 작업입니다.
`tools/translate_script.py`의 `TRANSLATIONS`를 땜질하는 대신, 한 번 제대로 만든 표를 기준으로 삼으려는 목적입니다.

## 폴더

```text
glossary/
  inputs/    영어 이름 목록 (id, 영어 이름). 수정하지 않는다
  outputs/   카테고리별 결과 (작업자가 채운다)
  prompts/   AI 에이전트에게 줄 프롬프트 (공통 규칙 + 카테고리 5개 + 한 번에 시키기용)
  exports/   사용처용 파일 (names.csv, names.txt). export_names.py 가 만든다. 손으로 고치지 않는다
  tools/     check_glossary.py    결과 검증·합치기
             build_master_db.py   마스터 테이블(SQLite) 만들기
             export_names.py      내보내기 만들기·검사
             game_text.py         게임 텍스트 파일과 직접 대조 (로컬 전용)
  items.csv  모든 카테고리를 합친 최종 표 (--merge 하면 생김)
  master.db  마스터 테이블 (build_master_db.py 하면 생김, git에는 안 올림)
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
| `prompts/06_all_remaining.md` | 위 02~05를 한 에이전트가 이어서 | 위 네 개 |

한 에이전트에게 02~05를 전부 맡기려면 `06_all_remaining.md`를 쓰세요. 게임 파일을 한 번만 풀어서 네 카테고리가 같이 씁니다.

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

## 마스터 테이블 (기준 데이터)

```bash
python glossary/tools/build_master_db.py
```

`inputs/`의 1,632행 전부가 `item_master` 테이블의 뼈대가 됩니다. 번역이 아직 없는 행은 `pending`으로 들어가므로, 일부만 끝난 상태에서도 만들 수 있고 몇 번을 돌려도 같은 결과입니다. 결과 파일에 검증 오류가 있으면 만들지 않습니다.

| 요소 | 내용 |
|---|---|
| 기본 키 | `(category, item_id)` (id는 카테고리마다 겹칠 수 있어서 함께 씀) |
| `game_id` | id가 숫자면 정수로도 저장 (조인용) |
| 제약 | `ok`/`unsure`는 `ko_name` 필수, `missing`/`pending`은 `ko_name` 없음, `is_dlc`는 0/1 |
| 참조 테이블 | `lookup_category`, `lookup_status`, `lookup_source` (외래 키로 연결) |
| 뷰 | `v_translation_coverage` (카테고리별 진행률), `v_needs_review` (확인할 행) |

진행 상황 보기:

```sql
SELECT * FROM v_translation_coverage;
SELECT * FROM v_needs_review;
```

기존 ETL 데이터와 연결하기 (영어 이름 기준 조인). `python tools/db_etl_pipeline.py`로 만든 `assets/data/elden_ring.db`에서:

```sql
ATTACH 'glossary/master.db' AS m;
SELECT w.name, m.ko_name
FROM weapons w
LEFT JOIN m.item_master m ON m.category = 'weapons' AND m.en_name = w.name;
```

`m.item_id IS NULL`인 행은 가이드 문서의 무기 이름이 게임의 이름 목록에 없다는 뜻이라, 오타나 표기 차이를 찾는 데이터 품질 검사로도 쓸 수 있습니다. 지금 `weapons` 43개는 전부 일치합니다.

## 내보내기와 사용처

```bash
python glossary/tools/export_names.py          # exports/ 와 assets/data/glossary_names.json 다시 만들기
python glossary/tools/export_names.py --check  # 디스크 파일이 마스터와 같은지 검사 (CI)
```

- **용어 사전 탐색기**: 사이트의 도구 메뉴(`docs/tools/glossary-explorer.md`)가 `assets/data/glossary_names.json`을 읽어 한국어·영어로 검색합니다.
- **`translate_script.py`**: `--use-glossary`를 붙이면 영어 아이템 이름을 이 표의 한국어로 바꿉니다. `--glossary-report`는 기존 `TRANSLATIONS`와 달라지는 항목만 보여줍니다. 둘 다 파일을 쓰지 않는 dry-run이 기본입니다.

구조 설명과 앞으로 할 일은 `ARCHITECTURE.md`에 있습니다.

## 이 표를 쓰는 곳

- `tools/translate_script.py`: `--use-glossary` 옵션으로 연결됨 (위 참고).
- `er-planner`: `exports/names.csv`를 읽게 하는 일이 남아 있습니다.
