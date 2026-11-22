# 초원 전투 시작 화면 · 산과 오솔길 시안

[세 시안 비교](comparison.png)

채택된 스테이지별 에셋과 새 이름은 [v1 배포본](../../exports/v1/meadow-tilemap/stages/README.md)에서 확인한다.

| 시안 | 화면 | Tiled 지형 |
| --- | --- | --- |
| A 꽃초원 · 민트색 산과 분홍 들꽃, 밝은 흙길 | [미리보기](flower/preview.png) | [terrain.tmj](flower/terrain.tmj) |
| B 청록 산길 · 푸른 바위 능선과 회색 자갈길 | [미리보기](jade/preview.png) | [terrain.tmj](jade/terrain.tmj) |
| C 노을 고개 · 라일락 산과 살구빛 흙길 | [미리보기](sunset/preview.png) | [terrain.tmj](sunset/terrain.tmj) |

160×352px 세로 카메라의 초원 전투 시작 화면 기준이다. 오솔길은 슬라임 발 기준점인 (76, 232)을 지나며, 기존 제목과 시작 버튼을 얹은 상태로 비교한다.

- `stage-far-loop.png`는 160×352px 산 원경이다. 화면 좌상단에 놓고 가로로 반복한다.
- `stage-ground-loop.png`는 320×352px 풀밭과 길을 합친 지면이다. 화면 좌상단 기준으로 배치하고 가로로 반복한다.
- `stage-path-strip.png`는 320×352px 길만 분리한 투명 PNG다. 길을 별도 합성할 때 쓴다. 지면 PNG에 같은 길이 이미 포함되어 있다.
- `terrain.tmj`와 `terrain-tiles.png`는 지면을 16×16px, 20열×22행으로 편집하는 Tiled 파일이다. 카메라는 10열을 보여 준다. 아틀라스에서 재조립한 지면과 지면 PNG의 픽셀이 일치한다.
- 스크롤을 적용할 때 원경은 약 18.52px/s, 지면은 약 37.04px/s로 왼쪽 이동시키면 기존 시작 화면의 8.64초 반복 타이밍에 맞는다. 슬라임과 UI는 기존 시작 화면 레이어를 사용한다.

비교 이미지는 최근접 2배 확대다. 게임 적용 전 검토용 시안이며, Unity 실기 화면은 확인 전이다.
