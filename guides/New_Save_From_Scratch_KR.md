# 💾 새 세이브 처음부터 만들기

> [!NOTE]
> 치트 엔진과 ER 인벤토리 플래너를 사용해 PvP 준비 캐릭터를 처음부터 만드는 단계별 가이드입니다.
> 원문: **Anti Mage Association** *(Content & Design: Momo & Poisson, 2025)*.
> 한국어 마크다운 리디자인: **Crong**.

---

## 📋 전체 흐름

| 단계 | 내용 | 위치 |
|------|------|------|
| 1 | 빌드 플래너에서 빌드 작성 | 브라우저 |
| 2 | 치트 엔진 스크립트 생성 | 브라우저 |
| 3 | 스크립트 복사 (Cmd+A / Cmd+C) | 브라우저 |
| 4 | DEN / DEN2로 게임 실행 | 게임 |
| 5 | 캐릭터 생성 | 게임 |
| 6 | 치트 엔진 체크박스 설정 | 치트 엔진 |
| 7 | 인벤토리 스크립트 붙여넣기 | 치트 엔진 |
| 8 | Event Flags 적용 | 치트 엔진 |
| 9 | 룬 추가 및 레벨업 | 게임 + CE |
| 10 | 멜리나 대화 → 원탁의 방 이동 | 게임 |

---

## 🖥️ 1단계 — 빌드 작성

**[ER 인벤토리 플래너](https://er-inventory.nyasu.business/)** 에서 캐릭터 빌드를 만드세요.

> [!TIP]
> 플래너 사용법에 대한 자세한 설명은 사이트에 연결된 영상 가이드를 참고하세요.

스탯, 무기, 탈리스만, 장비를 모두 입력한 뒤, **Load/Save** 탭으로 이동해 **Cheat Engine**을 선택하세요.

---

## 📋 2단계 — 스크립트 생성

플래너의 **Cheat Engine** 탭에서:

1. 페이지 우측 하단의 **"Generate Script"** 버튼 클릭
2. 스크립트가 생성되어 복사 대기 상태가 됩니다

> [!NOTE]
> 이 스크립트는 인벤토리를 수동으로 정렬하지 않아도 되도록 무기와 탈리스만을 순서대로 스폰합니다.
> - **오프라인 상태에서만** 사용하세요
> - **스폰 레벨은 현재 최대 강화 레벨 기준**입니다 — 목표 레벨로 무기를 최소 1개 이상 강화한 뒤 사용하세요
> - 필요 조건: `Scripts → Build Creation → ItemGib` 활성화

---

## 📋 3단계 — 스크립트 복사

브라우저에서 **`Cmd+A`** 후 **`Cmd+C`** (Windows는 `Ctrl+A` / `Ctrl+C`)로 스크립트 전체를 복사합니다.

---

## 🎮 4단계 — 게임 실행

**모드 런처 파일**을 사용해 게임을 실행하세요 — **DEN** 또는 **DEN2**.

> [!IMPORTANT]
> 반드시 DEN 모드 런처를 통해 실행해야 합니다. 일반 런처 사용 불가.

---

## 🎮 5단계 — 캐릭터 생성

빌드에 맞춰 캐릭터를 생성하세요 (클래스, 체형, 외형 설정).

---

## ⚙️ 6단계 — 치트 엔진: 필수 체크박스 설정

*The Grand Archives* 테이블을 로드한 상태에서, 아래 체크박스를 활성화합니다.

### ✅ 활성화할 항목

```
[X] Scripts
    [X] Build Creation
        [ ] AddSoul
        [X] ItemGib
            [ ] Item
            [ ] Quantity
            [ ] Upgrade
            [ ] Reinforcement Level (Regular | Somber)
            [ ] Ash of War
            [ ] > Spawn Item
            [ ] Details
        [X] MassItemGib
            [ ] Give build starting items
            [X] Give all prattling pates    ← 여기에 스크립트 붙여넣기
            [ ] -- Base Game --
            [ ] Give all weapons
            ...
```

> [!IMPORTANT]
> **`Give all prattling pates`** 를 선택한 뒤, **Edit 메뉴**로 이동합니다.
> 기존 코드를 전체 선택 (`Cmd+A` / `Ctrl+A`) 후 삭제하고, 복사해둔 코드를 붙여넣기한 뒤 **OK**를 클릭합니다.

---

## ⚙️ 7단계 — 추가 체크박스 설정

아래 표시된 항목들을 순서대로 선택합니다:

```
MassItemGib
    [ ] Give all accessories
    [ ] Give all ashes of war
    -- Goods --
        [ ] Give misc consumables
        [ ] Give all crafting materials
        [ ] Give all upgrade materials
        [ ] Give all limited quantity craftables
        [ ] Give all greases
        [X] Give all spirit ashes              ← 선택
        [ ] Give all sorceries
        [ ] Give all incantations
        [ ] Give all crystal tears
        [ ] Give all bell bearings
    -- Shadow of the Erdtree --
        [ ] Give all weapons (SotE)
        ...
        [X] Give all crystal tears (SotE)      ← 선택
        [ ] Give all bell bearings (SotE)

[ ] Warp
[ ] Set flask level
[X] Add charge to flask                        ← 선택
[ ] Unlock All Gestures
[ ] Upgrades Need No Materials
```

> [!CAUTION]
> **플라스크 충전을 잊지 마세요!** — `Add charge to flask`를 선택하면 숫자 입력창이 뜹니다. **12**를 입력하고 OK를 클릭합니다 (0~12 사이 값).

---

## ⚙️ 8단계 — Event Flags 설정

**Event Flags** 섹션으로 이동해 아래 체크박스들을 하나씩 선택합니다:

```
[X] Event Flags
    [ ] Unlock all...
        [X] Unlock all Graces              ← 선택
        [X] Unlock all Whetblades          ← 선택
        [X] Unlock all Cookbooks           ← 선택
        [X] Unlock all Maps                ← 선택
        [X] Unlock all Summoning Pools     ← 선택
        [X] Unlock all Colosseums          ← 선택
    [ ] Invasion Regions
    [ ] Save Character Flags
    [ ] Event Flags by ID
    [ ] Deprecated
```

> [!WARNING]
> **이 과정에서 게임이 갑자기 충돌(크래시)할 수 있습니다 — 정상입니다.**
> 게임을 다시 실행하되, 반드시 **모드 런처(DEN/DEN2) 안에서** 재실행하세요. 중단된 지점부터 계속 진행하면 됩니다.

---

## ⚙️ 9단계 — 룬 추가 및 레벨업

치트 엔진에서 `Scripts → Build Creation → AddSoul` 섹션으로 이동합니다:

1. **Runes** 항목을 더블클릭 → 값을 `999999999`로 변경
2. **`> Give Runes`** 체크박스를 선택해 룬을 적용

> [!TIP]
> 인게임에서 룬 수가 변경된 것을 확인할 수 있습니다. 이후 게임으로 돌아가 목표 스탯에 맞게 레벨업합니다.

---

## 🎮 10단계 — 게임으로 복귀

게임으로 돌아갑니다:

1. **가장 가까운 축복**으로 이동
2. **멜리나**와 대화해 레벨업 능력을 획득
3. 빌드 스탯에 맞게 레벨업 완료
4. 멜리나와 한 번 더 대화 → **"원탁의 방으로 이동"** 선택

> [!NOTE]
> 원탁의 방 방문은 **PvP 아레나를 활성화**하기 위한 필수 조건입니다.

---

## ⚠️ 중요 — Morgott's Rune (파이트 클럽)

> [!IMPORTANT]
> **파이트 클럽**에 참여하려면 **Morgott's Rune**을 반드시 활성화해야 합니다.
>
> 치트 엔진으로 추가한 뒤, 인게임에서 **축복(Grace)에서 직접 활성화**해야 합니다.

---

## ✅ 완료!

이제 플레이할 준비가 되었습니다. DEN에 오신 것을 환영합니다.

---

*개발에 도움을 주신 분들께 감사드립니다 👥👑*

| 이름 | 역할 |
|------|------|
| **Emiia** | Elden Ring Planner 제작 |
| **Axi** | DEN2 제작 |

---

<div align="center">

*Content and design by Momo & Poisson · Anti Mage Association, 2025*
*한국어 마크다운 리디자인: Crong*

</div>
