# 이미지 사용 안내

게임에 적용할 이미지는 `exports/v1/`에서 고른다. 각 패키지의 README, JSON 및 Unity `.meta`에서 배치·분할·피벗·타이밍을 확인한다. 표의 패턴은 해당 패키지 기준이며 같은 종류의 파일 전체에 적용한다.

| 패키지·이미지 | 게임에서 쓰는 경우 |
| --- | --- |
| [wizard](v1/wizard/README.md) · `walk/`, `idle/`, `cast/`, `fall/` PNG | 주인공의 짧은 보폭 걷기 10장, 대기 5장, 시전 8장, 손을 짚고 옆으로 엎어지는 쓰러짐 6장 |
| [wizard-title-hero](v1/wizard-title-hero/README.md) · `idle/`, `walk/`, `cast/`, `fall/` PNG | 채택된 마법사의 제작 시트와 비교판. 게임 적용에는 위 wizard 패키지 사용 |
| [meadow-slime](v1/meadow-slime/README.md) · `advance/`, `idle/`, `attack/`, `hurt/`, `death/` PNG, `meadow_slime_shadow.png` | 초원 슬라임의 다섯 상태와 발밑 그림자 |
| [meadow-terrain](v1/meadow-terrain/meadow/layout.json) · `meadow/terrain.png`, `atlas/hood_staff_meadow.png`, `wizard-shadow.png` | 초원 지형 배치용 이미지, 해당 맵용 지형 타일 아틀라스, 마법사 발밑 그림자 |
| [meadow-tilemap](v1/meadow-tilemap/README.md) · `game-title-*.png` | 타이틀의 원경·구름·전경 레이어 |
| [챕터 1 홈 화면](v1/meadow-tilemap/chapter-01-home/README.md) · `background.png`, `button-game-start.png` | 마법사가 포함된 홈 배경과 투명 게임 시작 버튼 |
| [meadow-tilemap/stages](v1/meadow-tilemap/stages/README.md) · `stage-{01,02,03}/stage-*.png`, `stage-start.tmj`, `terrain.tmj` | 들꽃 언덕·솔바람 고개·노을마루 시작 화면의 산·언덕·지면, 번호·이름 전경 및 화면·지형 맵 |
| meadow-tilemap/stages · `button-battle-start.png`, `stage-*/stage-start-title.png` | 스테이지 공통 전투 시작 버튼과 버튼을 분리한 시작 전경 |
| meadow-tilemap · `tilemap/stage-slime-hop.png` | 스테이지 시작 화면 공통 슬라임 점프 |
| meadow-tilemap · `meadow-ui-tiles.png`, `sprites/*-face.png`, `sprites/*-cooldown-edge.png`, `sprites/ready-rim.png`, `sprites/slot-frame.png` | 타일맵용 UI 시트, 주문별 슬롯 앞면·재사용 대기 테두리, 준비 상태 테두리, 슬롯 프레임 |
| [meadow-wave-mobile](v1/meadow-wave-mobile/README.md) · `distant-meadow.png`, `meadow-terrain.png`, `meadow-hedge.png`, `atlas/meadow_wave.png`, `wizard-idle.png` | 세로형 초원의 원경·전투 지형·덤불, 타일 조립용 아틀라스, 전투 위치의 마법사 대기 이미지 |
| [meadow-wave-mobile/detailed](v1/meadow-wave-mobile/detailed/README.md) · `mountains.png`, `foothills.png`, `battlefield.png`, `battle.tmj`, `terrain.tmj` | 스테이지 1~3 전투용 산·언덕·지면과 화면·지형 맵. 전투 마법사에 맞춘 색과 슬라임 표시 배율 적용 참고 |
| meadow-wave-mobile · `spell-panel.png`, `spell-slots.png` | 세로형 전투 하단 배경과 24×24 슬롯 시트. 슬롯 배치는 `spell-slots.json` 참고 |
| [spell-effects](v1/spell-effects/README.md) · `spritesheets/{fire,cold,lightning,arcane}/*.png` | 주문 시전·비행·적중·오라에 쓰는 기본 주문 5종의 시트 6장. [분할 데이터](v1/spell-effects/unity-slicing.json)에서 재생과 배치를 확인한다. |
| [spells-to-go-ui](v1/spells-to-go-ui/README.md) · `button-{normal,highlighted,pressed,disabled}.png` | 기본·강조/선택·눌림·비활성 버튼 상태 |
| spells-to-go-ui · `NoticeParchment.png` | 웨이브 예고, 선택 안내, 희생 확인, 스테이지 결과 등 공용 알림의 나무틀 양피지 |
| spells-to-go-ui · `panel.png`, `dialogue.png`, `dialogue-tail.png`, `speaker-scroll.png`, `nameplate.png` | 인벤토리·보상용 패널, 캐릭터 대화 본체와 꼬리, 화자 이름용 양피지, 남색 보조 이름판 |
| spells-to-go-ui · `spell-clasp.png`, `panel-crest.png` | 이름판의 주문 문양과 패널 상단 장식 |
| spells-to-go-ui · `inventory-slot-*.png`, `inventory-{potion,rune,scroll}.png` | 인벤토리 기본·선택·잠금 슬롯과 그 위에 놓는 아이템 아이콘 |
| spells-to-go-ui · `package/Reference/ui-tiles-12px.png` | Tiled 등에서 UI를 직접 조립할 때 쓰는 12px 타일 배열 |
| [wood-spell-cards](v1/wood-spell-cards/README.md) · `Card{Fire,Lightning,Ice}.png`, `SlotEmpty.png`, `SlotFlash.png`, `Charge{Track,Fill}.png` | 손패·장착·전투 카드 원소별 앞면, 빈 장착 슬롯, 발동 강조, 충전 게이지 |
| wood-spell-cards · [기본 주문 카드 삽화 5종](v1/wood-spell-cards/skill-art/basic/manifest.json) | 기본 전투 주문 다섯 장은 이 매핑의 art와 frame을 합성한다. 매직 볼트는 푸른 잔광 버전, 차지드 볼트는 회전 파편 버전이다. |
| wood-spell-cards · `sacrifice/embers-{mask,overlay}.png` | 선택한 카드를 희생할 때 카드와 글씨가 타들어 가는 마스크와 불씨 |
| wood-spell-cards · `number-change/scan-{mask,overlay}.png` | 희생 후 다른 카드의 이전 숫자만 스캔해 지우는 마스크와 불티 |
| [health-bars](v1/health-bars/README.md) · `hp-frame.png`, `hp-fill.png`, `hp-chip.png` | 마법사와 몬스터 머리 위 20×4px 체력바의 테두리·현재 체력·피해 잔상. 캐릭터별 위치는 매니페스트의 `barTopLeftFromFeetPx` |
| [wave-notices](v1/wave-notices/README.md) · `{victory,defeat}-rule.png` | 결과 요약형 결과창에서 승리/패배에 맞춰 쓰는 장식선 |
| wave-notices · `{buff,penalty}-card.png`, `erase-mask.png`, `{buff,penalty}-erase.png` | 웨이브 효과 알림 카드와 퇴장용 픽셀 소거 마스크·파티클 |

## 검토 이미지와 제작 자료

- [걷기 10프레임 정리](../work/wizard-walk-clean/README.md)는 이전 걷기 시트의 비교 GIF와 재생성 스크립트다.

- [전신 걷기 10프레임 시안](../work/wizard-walk-review/README.md)은 복원된 걷기와 팔·지팡이·망토가 보폭에 맞춰 움직이는 새 포즈를 비교하는 검토 자료다.

- [챕터 1 타이틀](../work/wizard-title-illustrated/chapter-01/README.md)은 초원에서 대도시로 향하는 여정과 지하 던전 입구를 담은 홈 화면 시안이다.

- [표지 마법사 스프라이트](../work/wizard-title-sprite/README.md)는 표지 주인공을 옮긴 32×32 정지 포즈 디자인 검토용이다.

- [마법사 일러스트 타이틀](../work/wizard-title-illustrated/README.md)은 새 주인공 일러스트와 산길 배경, 룬석 버튼의 조합을 확인하는 홈 화면 시안이다.

- `exports/v1/**/preview.*`, `result-preview.png`, `wave-preview.gif`는 사용 화면이나 재생을 확인하는 검토 이미지다.
- `work/button-review/`, `work/parchment-review/`의 이미지와 GIF는 카드, 버튼, 양피지 비교용이다.
- `work/card-sacrifice/`, `work/wave-notice-concepts/`의 이미지와 GIF는 동작 시안과 비교용이다. 채택본과 배치 정보는 위 v1 패키지에서 고른다.
- [산 배경과 오솔길 3종](../work/meadow-mountain-concepts/README.md)은 초원 전투 시작 화면용 교체 시안이다. 비교 이미지에는 기존 슬라임과 시작 화면 UI가 합성되어 있다.
- `sources/`의 이미지는 제작 원본, `references/`의 이미지는 참고와 출처 확인, `.local/`의 이미지는 로컬 이관·백업에 사용한다. 외부 자료를 사용할 때는 [출처와 사용 조건](../references/reference-components/출처와-라이선스/사용-조건-요약.md)을 먼저 확인한다.
