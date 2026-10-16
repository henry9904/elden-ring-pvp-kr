# 작업 2: 방어구 (722개)

먼저 `glossary/prompts/00_common.md`를 끝까지 읽고 그 규칙을 따르세요.

## 할 일

- 입력: `glossary/inputs/armor.csv` (722행: `id,en,group,dlc`)
- 출력: `glossary/outputs/armor.csv`
- `group`은 부위입니다: `Head`(투구), `Body`(갑옷), `Arms`(장갑), `Legs`(다리 방어구).
- 보는 FMG는 `ProtectorName`입니다.

## 방어구에서 특히 조심할 것

- 같은 세트의 4부위는 영어 이름이 비슷하지만 한국어 이름은 부위마다 다릅니다. 세트 이름을 복사해서 부위만 바꾸지 말고 id마다 확인하세요.
- `(Altered)`가 붙은 이름은 별개 아이템입니다. 일반 버전과 합치지 않습니다.
- 같은 이름의 방어구가 id만 다르게 여러 번 나올 수 있습니다. id를 기준으로 하고, 한국어 이름이 같아지면 `note`에 적습니다.

## 검증

```bash
python glossary/tools/check_glossary.py armor
```
