# 🗺️ MithMaps 모드 가이드

> [!NOTE]
> **MithMaps**는 2vs2 및 3vs3 전투를 지원하는 엘든링 커스텀 모드입니다. 본 문서는 공식 가이드라인을 기반으로 작성되었습니다.

## 🛠️ 설치 및 설정

- **다운로드**: [🔗 MithMaps 깃허브 페이지(다운로드)](https://github.com/Mithsril/MithMaps)에서 최신 버전을 다운로드 및 설치하세요.
- **실행 방법**: 반드시 `Launch MithMaps.bat` 파일을 사용하여 모드를 실행하세요.
- **비밀번호 변경**: 비밀번호를 변경하려면 DEN1 폴더가 아닌 **MithMaps 내의 seamless 폴더**를 사용해야 합니다.
- **맵 적용 경로**: 이 모드는 `.mith` 확장자를 사용하며, 다음 경로에 추가할 수 있습니다:
  `C:\Users\사용자PC이름\AppData\Roaming\EldenRing`

---

## 📍 커스텀 맵 목록

DEN1 맵 위치를 기반으로 제작된 2v2 및 3v3 커스텀 맵이 포함되어 있습니다.

| 맵 이름 | 인원 | 제작자 |
|---|---|---|
| **Redmane Battlegrounds** | 3v3 | Mithsril |
| **Seaside Stronghold** | 3v3 | Hexwave |
| **Scriptorium Archives** | 2v2 | Mithsril |
| **Brawling Square** | 2v2 | Den Team |
| **Luminous Lake** | 1v1 | Den Team (Mithsril 수정) |
| **Secluded Towers** | 1v1 | Mithsril |

---

## 🎮 주요 기능 (by Molly)

- **팀 구분**: 두 가지 팀 타입 지원 (Red Team / Blue Team)
- **리스폰 포인트**: 사용자 지정 리스폰 위치 설정 기능
- **인게임 스코어보드**: 게임 내 점수판 표시
- **몬스터 킬 스크립트**: 모든 몹을 처치하는 스크립트 내장
- **침입 시스템 개편**:
  - 모드 사용자끼리만 침입이 가능하도록 변경되었습니다.
  - 침입자는 Seamless Co-op의 무색이 아닌 **붉은색(Red)**으로 표시됩니다.
  - 바닐라 지역과 커스텀 지역 모두 침입 가능합니다. (MithMaps 내 seamless 설정에서 비활성화 가능)

---

## ⌨️ 단축키 (Hotkeys)

| 단축키 | 기능 설명 |
|---|---|
| `F1` | 레드 팀(Red Team) 가입 |
| `F2` | 블루 팀(Blue Team) 가입 |
| `F3` | 팀 탈퇴 (결별의 결정을 사용하기 위해 필요) |
| `F4` | 스코어보드 보기 |
| `F5` | 스코어보드 초기화 |
| `F6` | 커스텀 리스폰 위치 지정 |
| `F7` | 모든 몹 처치 (Kill All Mobs) |
| `F8` | 플레이어 목록 켜기/끄기 |

---

## 📦 포함된 모드 (Seamless)

MithMaps는 기본적으로 다음 Seamless 모드들을 포함하고 있습니다.
- **GG**: Seamless Co-op용 플레이어 목록 오버레이 (by tomclark)
- **Transparent UI DLC Fixes**: 투명 UI 픽스 (by ShenDaiSword)

---

## ⚔️ 신규 무기

*새로운 무기는 원탁의 쌍둥이 노파에게서 구매할 수 있습니다.*
- **Void Blade**: HTS, LGS, TS, CS, 그리고 클레이모어의 모션을 섞은 무기 (Original model by Conkin)
- **Regal Maul**: 망치, 모닝스타, 대형 망치, 할버드, 대도, 손톱, CGS의 특성을 섞은 무기 (Original model by Cixler)

---

## 📜 밸런스 패치 노트 (현재 비활성화됨)

> [!WARNING]
> 아래의 밸런스 패치 내용은 유저들의 요청에 의해 **현재 비활성화(Disabled)** 상태입니다. 과거 밸런싱 히스토리 보존을 위해 기록해 둡니다.

### 금지된 무기 (Disabled Weapons)

- 자검류, 파타, 뼛조각 활, 레다의 검, 대장장이 술법의 원반, 저주검, 쌍방패에서의 **사냥개의 스텝(BHS)** 및 **퀵스텝(QS)** 금지

### 너프된 무기 (Nerfed Armor & Weapons)

- **소드 랜스, 경대검(Milady)**: 데미지 30% 너프
- **귀부기사의 검**: 데미지 15% 너프
- **역수검(Backhand Blades)**: 데미지 10% 너프
- **밤의 발톱(Claws of Night)**: 데미지 50% 너프
- **가시 갑옷 세트(Briars Set)**: 더 이상 굴르기 데미지 및 에임 펀치 발생 안 함
- **왕족의 유해 세트**: 낮은 HP에서 회복 효과 제공 안 함

### 금지된 주문 & 소모품 (Disabled Spells & Consumables)

- **주문**: 모든 회복 및 리젠 주문 (짐승의 생명 제외), 인력탄, 회귀성 원리, 밤 무녀의 안개, 보이지 않는 모습, 혜성, 밤의 혜성, 렐라나의 쌍월, 암석검, 거인의 불을 받으라, 고룡의 벼락, 스마라그의 휘석 숨결, 메스메르의 불
- **소모품**: 고양의 향약, 부패/독/방패 기름, 큰 똥항아리와 화산 항아리를 제외한 모든 큰 항아리, 전갈 소모품류, 두 종류의 동침의 축복, 불의 똬리, 고룡의 은총, 용의 심장, 무녀의 심장, 탄식하는 자의 가면

### 향후 예정 (To Do)

- 가벼운 구르기(Lightroll) 삭제
- 고렘의 화살 경직(Stun) 너프
- 산탄 석궁의 상태 이상 볼트 제거
- 오프핸드 자검(offrak)의 하이퍼아머(HA) 제거
- 도가니의 깃털 부적, 붉은 도가니의 깃털 부적, 모든 도가니의 부적 제거
- 양손검의 탈리스만 너프 (20% -> 15% 검토 중)
- 명도 월은 L2 티어 1 경직으로 변경

---

## 🙏 Credits (도움을 주신 분들)

Molly, Hexwave, Emilia, Den Team
