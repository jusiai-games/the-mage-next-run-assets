# 게임 에셋

현재 적용 버전은 `v1`이다. 다음 버전은 같은 패키지 구조로 `v2/`에 추가한다.

화면과 상태별 사용처는 [이미지 사용 안내](IMAGE-USAGE.md)를 참고한다.

메인 화면의 석문에 마법광을 추가하고 초원 원경·전경, 캐릭터, 주문 HUD와 원소 효과의 색을 다듬었다.

캐릭터 공통 셀은 32×32px, 발 피벗은 좌상단 기준 (16, 28), 32 PPU다. PNG 시트의 분할 정보는 같은 이름의 `.sprite.json`을 참고한다.

| 에셋 | 프레임과 타이밍 |
| --- | --- |
| [마법사 주인공](v1/wizard/README.md) | 걷기 10, 대기 5, 시전 8, 쓰러짐 6. 시전 시작 100ms에 발사 |
| [초원 슬라임](v1/meadow-slime/README.md) | 전진 18, 공격 6, 대기 3, 피격 4, 사망 4. 전진 한 주기 540ms, 공격 판정 275ms |
| [초원 전투 타일맵](v1/meadow-tilemap/README.md) | 타이틀·스테이지 시작·전투용 Tiled 맵 4종과 Unity 스크립트 |
| [스테이지 시작 화면 3종](v1/meadow-tilemap/stages/README.md) | 들꽃 언덕·솔바람 고개·노을마루의 원경, 지면, 제목 및 Tiled 지형 |
| [모바일 초원](v1/meadow-wave-mobile/README.md) | 160×352 화면, 16×16 타일, 24×24 주문 슬롯 |
| [Spells to Go UI](v1/spells-to-go-ui/README.md) | Unity 9슬라이스 버튼과 패널, 인벤토리 슬롯 상태와 아이템 아이콘 |
| [나무 명판 주문 카드](v1/wood-spell-cards/README.md) | v1 초안. 기본 주문 삽화 5종, 빈 슬롯, 발동 테두리, 충전 게이지 |
| [결과와 웨이브 알림](v1/wave-notices/README.md) | 결과 요약형과 버프·패널티 픽셀 소거형 |
| [기본 주문 이펙트 5종](v1/spell-effects/README.md) | 주문별 투명 시트 6장, 20 FPS(차지드 볼트 회전 파편 25 FPS), Unity 분할 안내 |
| [초원 타일과 마법사 그림자](v1/meadow-terrain/meadow/layout.json) | 타일 16×16 |
| [게임 팔레트](../palettes/README.md) | 제작 원본의 HEX와 최신 내보내기 팔레트 출처 |

마법사 시전 시작 100ms에 투사체를 발사한다. 시트의 프레임 순서와 피벗은 각 .sprite.json, 재생 시간과 이벤트는 각 timing.json 또는 슬라임의 animation.json에 있다.
