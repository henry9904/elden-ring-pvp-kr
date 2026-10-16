# 작업 4: 소비 아이템·주문·위대한 룬 (194개)

먼저 `glossary/prompts/00_common.md`를 끝까지 읽고 그 규칙을 따르세요.

## 할 일

- 입력: `glossary/inputs/goods.csv` (194행: `id,en,group,dlc`)
- 출력: `glossary/outputs/goods.csv`
- `group`은 분류입니다: 소비 아이템(`Edible`, `Grease`, `Crystal Tear` 등), 주문(`Sorcery`, `Incantation`), 위대한 룬(`Great Rune`).
- 보는 FMG는 `GoodsName`입니다. 주문이 다른 FMG에 있으면 어떤 파일에서 찾았는지 `note`에 한 번만 적고 계속합니다.

## 이 목록에서 특히 조심할 것

- 영어 이름에 쉼표가 들어간 것이 있습니다(`Flame, Cleanse Me` 등). CSV로 쓸 때 그 값을 반드시 큰따옴표로 감싸세요.
- 같은 영어 이름이 id만 다르게 두 번 있는 항목이 하나 있습니다. id를 기준으로 짝지으세요.
- id가 `2000000` 이상인 항목은 DLC 쪽입니다. DLC 텍스트 파일(`item_dlc*.msgbnd.dcx`)에서 찾으세요.

## 선택 과제 (필수 아님)

방법 A로 `GoodsName` 전체를 풀었다면, 이 목록에 없는 아이템까지 전부 `glossary/outputs/goods_all.csv`에 같은 형식(`id,en,ko,status,source,note`)으로 저장해 주세요. 이 파일은 검증 스크립트 대상이 아니고, 나중에 다른 아이템을 추가할 때 씁니다.

## 검증

```bash
python glossary/tools/check_glossary.py goods
```
