# 모바일 초원 웨이브 화면

160×352 논리 픽셀, 20:9 스마트폰 세로 화면 기준. 배치 좌표는 좌상단 원점이다.

스테이지 1~3 전투 화면의 새 산 원경·중간 언덕·전장 타일맵은 [상세 전장 패키지](detailed/README.md)에 있다.

| 에셋 | 크기 | 배치 |
| --- | --- | --- |
| distant-meadow.png | 160×80 | (0, 0) |
| meadow-terrain.png | 160×144 | (0, 80) |
| meadow-hedge.png | 160×19 | (0, 66), 전투 지형 앞에 배치 |
| spell-panel.png | 160×128 | (0, 224) |
| spell-slots.png | 72×24 | 24×24 셀 3개 |
| wizard-idle.png | 32×32 | [채택된 마법사](../wizard/README.md)의 첫 대기 프레임. 발 위치 (24, 153), 발 피벗 (16, 28) |

- 타일 방식으로 지형을 배치할 때 atlas/meadow_wave.png와 layout.json을 함께 사용한다. 16×16px, 10열×9행이다. meadow-terrain.png는 동일한 지형을 합친 PNG다.
- spell-slots.json에 준비 상태, 충전 중 상태, 충전 막대의 절단 좌표와 패널 안 두 줄 배치 좌표가 있다. 트랙에 맞춰 충전 막대 표시 너비를 0~15px로 조절한다.
- UI를 실제 기기에 배치할 때 상하 시스템 영역은 안전 영역을 기준으로 잡는다.

- 덤불은 원경과 초원 경계를 덮는 투명 장식 레이어다. layout.json의 decorations에 좌표가 있으며 충돌은 꺼 둔다.
