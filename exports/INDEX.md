# 최신 게임 에셋

메인 화면의 석문에 마법광을 추가하고 초원 원경·전경, 캐릭터, 주문 HUD와 원소 효과의 색을 다듬었다.

캐릭터 공통 셀은 32×32px, 발 피벗은 좌상단 기준 (16, 28), 32 PPU다. 번개 매직 볼트는 32×32px 셀의 중앙을 피벗으로 쓴다. PNG 시트의 분할 정보는 같은 이름의 `.sprite.json`을 참고한다.

| 에셋 | 프레임과 타이밍 |
| --- | --- |
| [후드 마법사 · 빠른 시전](hood-staff-32-quick-cast/README.md) | 걷기 v2 4, 대기 5, 시전 5, 쓰러짐 6. 시전 시작 100ms에 발사 |
| [초원 슬라임 v7](meadow_slime_combat32_v7/README.md) | 전진 18, 공격 6, 대기 3, 피격 4, 사망 4. 전진 한 주기 540ms, 공격 판정 275ms |
| [초원 전투 타일맵](meadow-tilemap/README.md) | 타이틀·스테이지 시작·전투용 Tiled 맵 4종과 Unity 스크립트 |
| [모바일 초원](meadow-wave-mobile/README.md) | 160×352 화면, 16×16 타일, 24×24 주문 슬롯 |
| [Spells to Go UI](spells-to-go-ui/README.md) | Unity 9슬라이스 버튼과 패널, 인벤토리 슬롯 상태와 아이템 아이콘 |
| [번개 매직 볼트](magic-bolt-electric/README.md) | 발사 4, 비행 6, 적중 4 |
| [원소 주문 이펙트 30종](sorceress-vfx/README.md) | 주문별 투명 시트, 20 FPS, Unity 분할 안내 |
| [마법사 초원 타일과 그림자](hood-staff-32-final/meadow/layout.json) | 타일 16×16 |
| [게임 팔레트](../palettes/README.md) | 제작 원본의 HEX와 최신 내보내기 팔레트 출처 |

마법사 시전 시작 100ms에 번개 매직 볼트를 발사한다. 시트의 프레임 순서와 피벗은 각 .sprite.json, 재생 시간과 이벤트는 각 timing.json 또는 슬라임의 animation.json에 있다.
