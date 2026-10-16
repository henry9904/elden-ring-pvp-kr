# 용어 기준 구조

엘든 링 한영 용어를 **한 곳에서만 정하고**, 나머지는 거기서 만들어 쓰기 위한 구조입니다.
작업이 무엇이든 용어는 여기서 가져오면 되게 하는 것이 목표입니다.

## 기준 저장소

`elden-ring-pvp-kr`의 `glossary/`를 기준으로 삼습니다.

- 검증기(`check_glossary.py`), 마스터 테이블(`build_master_db.py`), 내보내기(`export_names.py`)가 여기 있습니다.
- 모든 행에 `status`(ok/unsure/missing)와 `source`, `note`가 붙어 있습니다.
- CI와 린트가 이 저장소에 걸려 있고, 새 검사 두 개(결과 검증, 내보내기 일치)도 CI에 들어 있습니다.

다른 저장소(`er-planner` 등)는 여기서 만든 파일을 **받아서 쓰기만** 합니다.

## 계층

한 방향으로만 흐릅니다. 아래 계층의 파일은 손으로 고치지 않고, 위 계층에서 다시 만듭니다.

| 계층 | 무엇 | 위치 |
|---|---|---|
| 원천 | 게임의 한국어/영어 텍스트(`msg/korKR`, `msg/engUS`), 보조로 나무위키, 신님이 정리한 이름 목록 | 저장소 밖 |
| 입력 목록 | 영어 이름과 id만 있는 목록 | `glossary/inputs/*.csv` |
| 결과 | 카테고리별 한국어와 상태·출처 | `glossary/outputs/*.csv` (**사람이 고치는 유일한 곳**) |
| 마스터 | 모든 결과를 합친 표, 제약과 뷰 포함 | `glossary/items.csv`, `glossary/master.db` |
| 내보내기 | 사용처가 읽는 모양 (`game_id` 포함) | `glossary/exports/names.csv`, `names.txt`, `assets/data/glossary_names.json` |
| 사용처 | 이 표를 읽는 쪽 | 용어 사전 탐색기 페이지, `translate_script.py --use-glossary`, `er-planner` |

내보내기는 `python glossary/tools/export_names.py`로 만들고, CI가 `--check`로 마스터와 같은지 검사합니다.

## 키 규칙

- **아이템 키는 `(category, game_id)`입니다.** `id` 열이 게임의 id이고, 카테고리마다 겹칠 수 있어서 함께 씁니다.
- **영어 이름만으로 찾지 않습니다.** 무기 `Dagger`는 `대거`이고 무기군 `Dagger`는 `단검`입니다. 이름으로 조인할 때는 반드시 `category`를 함께 씁니다.
- **용어는 `종류:이름` 형태(`weaponType:Katana`)로 키를 만듭니다.** 같은 한국어가 서로 다른 용어에 쓰이는 것(신비 = 능력치 Arcane / 변질 Occult)은 종류 안에서만 구분되면 허용합니다.
- 내보내기 파일에는 영어, 한국어와 함께 **`game_id` 열(`id`)** 이 들어 있습니다. 다른 쪽의 slug(`dagger` 등)는 보조 정보입니다.

## 출처와 버전 기록

- 행마다 `status`, `source`, `note`(근거 주소)를 남깁니다.
- `source`는 `game-text`가 가장 믿을 수 있고, `namu`와 `other`는 나중에 게임 텍스트로 다시 대조할 대상입니다.
- 신님이 직접 정리한 `names.txt`/`names.md`는 정답으로 보고 DLC 이름과 일부 값을 반영했습니다(`note`에 "names.txt … 반영"). 그 파일을 만든 스크립트와 게임 텍스트 자료는 신님 쪽에 있는 것으로 보이고, 이 저장소에는 없습니다. 받게 되면 `source`를 `game-text`로 올릴 수 있습니다.
- 추가할 것: 마스터에 **메타 정보**(게임 버전, DLC 포함 여부, 뽑은 날짜, 뽑은 방법)를 적습니다.
- "공식 이름"이라는 표현은 `source`가 `game-text`인 행에만 씁니다.

## 지금 상태

- 1,632개 중 ok 1,615, unsure 17, missing 0입니다.
- 아이템 이름 1,599개(무기 487, 방어구 722, 탈리스만 154, 버프 194, 무기군 42)는 `items.csv`와 신님의 `names.csv`가 완전히 같습니다.
- 게임 파일에서 직접 뽑은 행은 아직 없습니다. 대부분 `source`가 `other`입니다.
- 화면 용어 284개(`glossary.csv`)는 직접 옮긴 것이고, 효과 이름 168개는 대부분 검토하지 않았다고 문서에 적혀 있습니다. 아직 이 구조에 들어오지 않았습니다.
- 용어표가 두 개(`terms.csv` 75개, `glossary.csv` 284개)이고, `표준`/`일반`, `붉은 부패`/`부패` 두 곳의 표기가 서로 다릅니다.

## 진행 순서

1. ✅ 문서의 출처 설명을 실제에 맞게 고침 (이 문서).
2. ✅ 기준 저장소를 이 저장소로 정함.
3. ✅ 내보내기 스크립트와 CI 검사 (`export_names.py`, `check_glossary.py all`).
4. ⬜ 용어표 합치기: `terms.csv`와 `glossary.csv`를 종류(domain)가 있는 하나의 용어 테이블로 합치고 충돌 2건을 해결합니다.
5. ⬜ 메타 정보 추가: 게임 버전과 뽑은 날짜를 마스터에 기록합니다.
6. ⬜ 게임 텍스트로 다시 대조: `other`/`namu` 행을 확인해서 맞으면 `game-text`로 올립니다. 게임 파일을 풀 도구가 필요합니다.
7. 🔶 사용처 연결: 용어 사전 탐색기와 `translate_script.py --use-glossary`는 연결됨. `er-planner`는 내보내기 파일(`names.csv`)을 읽게 바꾸는 일이 남았고, 신님이 그쪽 저장소에서 따로 만들고 있어서 맞춰야 합니다.

## 지킬 원칙

- 내보내기 파일(`exports/*`, `glossary_names.json`)은 손으로 고치지 않습니다. 고칠 곳은 `outputs/`뿐입니다.
- 추측해서 번역하지 않습니다. 모르면 `missing`입니다.
- 이름만으로 조인하지 않습니다(`category`와 함께).
