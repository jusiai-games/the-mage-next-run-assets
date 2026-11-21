# 최신 게임 에셋

[초원 색감 v3 작업 프레임](../work/color-pass-v3/)은 프로토타입에서 사용한다. 가져온 파일에는 v3 Unity 교체 패키지가 포함되어 있지 않다.

[초원 색감 개선안 v2](meadow-color-v2/README.md)에 Unity 교체용 PNG와 제작용 색감 변경본을 정리했다.

캐릭터 공통 셀은 32×32px, 발 피벗은 좌상단 기준 (16, 28), 32 PPU다. 번개 매직 볼트는 32×32px 셀의 중앙을 피벗으로 쓴다. PNG 시트의 분할 정보는 같은 이름의 `.sprite.json`을 참고한다.

| 에셋 | 프레임과 타이밍 |
| --- | --- |
| [후드 마법사 · 빠른 시전](hood-staff-32-quick-cast/README.md) | 걷기 v2 4, 대기 5, 시전 5, 쓰러짐 6. 시전 시작 100ms에 발사 |
| [초원 슬라임 v7](meadow_slime_combat32_v7/README.md) | 전진 18, 공격 6, 대기 3, 피격 4, 사망 4. 전진 한 주기 540ms, 공격 판정 275ms |
| [초원 전투 타일맵](meadow-tilemap/README.md) | 타이틀·스테이지 시작·전투용 Tiled 맵 4종과 Unity 스크립트 |
| [모바일 초원](meadow-wave-mobile/README.md) | 160×352 화면, 16×16 타일, 24×24 주문 슬롯 |
| [Spells to Go UI](spells-to-go-ui/README.md) | Unity 9슬라이스 버튼과 패널 |
| [번개 매직 볼트](magic-bolt-electric/README.md) | 발사 4, 비행 6, 적중 4 |
| [원소 주문 이펙트 30종](sorceress-vfx/README.md) | 주문별 투명 시트와 GIF, 20 FPS, Unity 분할 안내 |
| [초원 전투 화면 주문 검토](sorceress-vfx-meadow-review.md) | 30종을 모바일 초원 화면에 합성하고 배율과 역할을 검토 |
| [마법사 초원 타일과 그림자](hood-staff-32-final/meadow/layout.json) | 타일 16×16 |
| [게임 팔레트](../palettes/README.md) | 위 에셋의 실제 픽셀 HEX |

마법사 시전 시작 100ms에 번개 매직 볼트를 발사한다. 시트의 프레임 순서와 피벗은 각 .sprite.json, 재생 시간과 이벤트는 각 timing.json 또는 슬라임의 animation.json에 있다.
