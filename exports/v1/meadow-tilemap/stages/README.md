# 스테이지 1~3 시작 화면

[비교 이미지](preview.png) · [배치 매니페스트](manifest.json)

전투 진입 후 사용할 산·언덕·전장 타일맵은 [모바일 전투 배경 패키지](../../meadow-wave-mobile/detailed/README.md)에 있다.

| 스테이지 | 원경과 길 | 미리보기 | Tiled 화면 |
| --- | --- | --- | --- |
| 1 들꽃 언덕 | 낮은 초록 능선, 작은 들꽃과 24px 흙길 | [PNG](stage-01/preview.png) | [맵](stage-01/stage-start.tmj) |
| 2 솔바람 고개 | 뾰족한 바위 능선, 소나무 숲과 20px 자갈길 | [PNG](stage-02/preview.png) | [맵](stage-02/stage-start.tmj) |
| 3 노을마루 | 저무는 해, 보랏빛 능선과 22px 흙길 | [PNG](stage-03/preview.png) | [맵](stage-03/stage-start.tmj) |

160×352px 카메라의 좌상단을 공통 원점으로 쓴다. 번호에 해당하는 폴더에서 레이어를 고른다.

1. `stage-far-loop.png` (160×352px)를 18.52px/s로 왼쪽으로 반복 스크롤한다. 원경을 따로 조립할 경우 `stage-mountains-loop.png` 위에 `stage-foothills-loop.png`를 같은 위치와 속도로 겹친다.
2. `stage-ground-loop.png` (320×352px)를 37.04px/s로 왼쪽으로 반복 스크롤한다. 두 레이어는 8.64초에 한 바퀴 돈다. 지면은 길을 포함한다. 별도 합성이 필요한 경우의 길 마스크는 `stage-path-strip.png`에 있다.
3. 공통 슬라임의 발 좌표는 (76, 232)다. [시트 재생 정보](../tilemap/stage-slime-hop.json)에 따라 32×32px 셀을 75% 표시 배율로 배치한다.
4. 번호와 이름이 그려진 `stage-start-foreground.png` (160×352px)를 맨 앞에 고정한다. 시작 화면에서 텍스트와 전투 시작 버튼을 개별 UI로 표시하는 경우 매니페스트의 `number`, `name` 값을 해당 UI에 연결한다.

버튼을 별도 UI로 배치할 때는 번호별 `stage-start-title.png`를 전경으로 쓰고, [공통 전투 시작 버튼](button-battle-start.png)을 (34, 289)에 92×28px 크기로 놓는다. 공통 버튼 이미지에는 문구가 들어 있다.

`stage-start.tmj`에서 산·언덕 이미지 레이어와 풀밭·오솔길 타일 레이어를 편집한다. `terrain.tmj`는 지형 레이어만 담는다. 두 맵은 16×16px 타일 20열×22행과 같은 폴더의 `terrain-tiles.png`를 사용한다. 카메라에는 가로 10열이 보인다. 타일 재조립 결과를 풀밭과 길 원본 레이어와 비교했다. Unity 씬 연결과 실제 플레이 검수는 별도다.
