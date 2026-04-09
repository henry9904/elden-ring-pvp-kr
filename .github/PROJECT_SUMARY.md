# 📋 elden-ring-pvp-kr 프로젝트 진행 요약

> 다음 대화에서 빠르게 컨텍스트 복구용으로 사용할 것

---

## 🗂️ 현재 GitHub 구조

```
henry9904/elden-ring-pvp-kr (main)
│
├── README.md                          ✅ 최신화 완료
│
├── ruleset/
│   ├── Standard_DEN_Restrictions_KR.md   ✅ (일반 결투/래더 - 한국어)
│   ├── Standard_DEN_Restrictions_EN.md   ✅ (일반 결투/래더 - 영문)
│   ├── Duel_Restrictions_KR.md           ✅ (sin 번역본)
│   ├── Tourney_Ruleset_KR.md             ✅ (토너먼트 - 한국어)
│   ├── Tourney_Ruleset_EN.md             ✅ (토너먼트 - 영문)
│   └── Ruleset_Explanation_Document.pdf  ✅ (원본 PDF by crowned_pvp)
│
├── guides/
│   ├── Nohman_TB_Guide_KR.md             ✅ (트윈블레이드 - 한국어)
│   └── Nohman_TB_Guide_EN.md             ✅ (트윈블레이드 - 영문)
│
└── info/
    ├── Stat_Analysis_KR.md               ✅ (스탯 분석 - 한국어)
    └── Stat_Analysis_EN.md               ✅ (스탯 분석 - 영문)
```

---

## 👥 크레딧

| 역할 | 이름 |
|------|------|
| 룰셋 원문 | crowned_pvp, DEN Rules Committee and Competitive Community |
| 트윈블레이드 가이드 원문 | Nohman |
| 스탯 분석 원문 | Drake Ravenwolf |
| 한국어 번역 | sin |
| PvP 스탯 분석 | sin |
| 리디자인 | Crong |
| 1차 검토 | LED |
| 피드백 | Ornstein, Emperor of Flames |

---

## 📝 주요 결정사항

### 문서 구조
- **Standard DEN Rules** = 일반 결투/래더 기본 규정 (메인)
- **Tourney Ruleset** = 토너먼트 전용 부록 (3회 전회 제한 등 추가 규칙 포함)
- **guides/** = 플레이어 가이드 (Nohman TB 등)
- **info/** = 게임 정보 (스탯 분석 등)

### 번역 원칙
- 공식 한국어 용어 기준 (나무위키/공식 번역 우선)
- 전회(AoW), 결정 물방울, 룬의 호 등 공식 명칭 사용
- 추천 섹션은 "원문 작성자의 개인 의견" 명시
- 한다체 사용

### 주요 수정 이력
- 시미터 독기름 금지 → 사실 아님으로 수정 (crowned_pvp 직접 확인)
- 카리아 관통 방패 오역 수정 (클래스 내 하위 무기 명시)
- DEN Rules Committee 크레딧 추가 (crowned_pvp 요청)
- Standard DEN / Tourney Ruleset 분리 (Ornstein 피드백)
- 버프 제한 무기에 한손/오프핸드 제한 없음 명시 (Cielo 피드백)

---

## 🔗 Google Docs 링크

| 문서 | 링크 |
|------|------|
| Standard DEN Restrictions (KR) | https://docs.google.com/document/d/19nzIk1BM0pPc-0tOQ-MzUqjdrQlJVL3PU0Qz2pvPh5s |
| Standard DEN Restrictions (EN) | https://docs.google.com/document/d/1kpKsYj8lQo7KkaKLnMWRCb6JPuC8Y0_M5h7lkdKNgmU |
| Tourney Ruleset (KR) | https://docs.google.com/document/d/1a46GJV2etOHvO8mcXmtXAXa9B8tTml80b4XhBU_x-08 |
| Tourney Ruleset (EN) | https://docs.google.com/document/d/1-ZBznyPk0yW4e7E1Ueo_tBkhQXjJWitsOPEPwASTRKk |
| Nohman TB Guide (KR) | https://docs.google.com/document/d/15EpQ8omEbPYKScOr4E2D9S2l6-G0BCyGJPKtdIN1a9I |
| Nohman TB Guide (EN) | https://docs.google.com/document/d/1gBohQpaa6Vvch9JIO-WneAlsyONmE64UKFV9eBk4DeI |
| Standard DEN (sin 버전 KR) | https://docs.google.com/document/d/1a46GJV2etOHvO8mcXmtXAXa9B8tTml80b4XhBU_x-08 |

---

## 🌿 GitFlow 운영 방법

### 브랜치 구조
```
main       ← 완성된 최종본만 (직접 커밋 금지)
develop    ← 작업 중인 내용 모음
feature/xx ← 각 작업별 브랜치
```

### 현재 상태
- **브랜치:** `main` 하나만 존재 → `develop` 브랜치 생성 필요

### develop 브랜치 생성 (최초 1회)
1. 레포에서 **`main`** 버튼 클릭
2. `develop` 입력
3. **"Create branch: develop from main"** 클릭

---

### 앞으로 작업 흐름

```
1. 파일 수정할 게 생기면
   → develop 브랜치로 이동
   → 파일 열고 편집
   → 커밋 시 "Create a new branch" 선택
   → 브랜치명: feature/작업내용
     (예: feature/stat-analysis-update)

2. 작업 완료되면
   → Pull Requests 탭 → New pull request
   → feature/xxx → develop 으로 PR 생성
   → 신짱 / LED 한테 검토 요청
   → 승인되면 Merge

3. 충분히 쌓이면
   → develop → main 으로 PR 한 번 더
   → Merge 하면 최종 배포 완료
```

### 실제 예시
```
Stat_Analysis 파일 수정할 때:

1. develop 브랜치로 이동
2. Stat_Analysis_KR.md 열고 편집
3. 커밋 시 브랜치명: feature/stat-analysis-kr-fix
4. PR 생성: feature/stat-analysis-kr-fix → develop
5. 신짱 검토 후 Merge
6. 나중에 develop → main Merge
```

> [!IMPORTANT]
> **main 브랜치에는 절대 직접 커밋하지 않는다.**
> 항상 `feature → develop → main` 순서를 지킨다.

---

## 📌 다음에 할 일

- [ ] `develop` 브랜치 생성 (GitFlow 시작)
- [ ] 앞으로 모든 작업은 `feature/` 브랜치로 진행
- [ ] Stat_Analysis 파일 양쪽 검토 후 최종 업로드 (신짱 최종 수정본 반영)
- [ ] sin 사이트 영문 원본 내용 확인 및 반영
- [ ] 추가 가이드 있으면 `guides/` 또는 `info/`에 추가
- [ ] Nohman 가이드 추가 내용 있으면 업데이트

---

## 💬 주요 커뮤니티 관계

| 인물 | 관계 |
|------|------|
| crowned_pvp | 룰셋 원작자. 프로젝트 칭찬 및 erpvp 홍보 제안. GitHub 협업은 정중히 거절 |
| Nohman | 트윈블레이드 가이드 작성자. GitHub 업로드 흔쾌히 허가 |
| sin | 한국어 번역 담당. er-sin.com 운영 |
| LED | 1차 검토. 시미터 독기름 정보 제공 |
| Ornstein | Standard DEN / Tourney 분리 피드백 제공 |
| Cielo | 버프 제한 무기 한손/오프핸드 명시 피드백 제공 |
