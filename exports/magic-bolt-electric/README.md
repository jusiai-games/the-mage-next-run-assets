# 번개 매직 볼트

[스태프 발사부터 슬라임 적중까지](cast-flight-impact.gif)

| 구간 | 시트 | 재생 |
| --- | --- | --- |
| 발사 | [4프레임](launch/magic_bolt_electric_launch.png) | 120ms, 반복 끔 |
| 비행 | [6프레임](flight/magic_bolt_electric.png) | 50ms씩 반복 |
| 적중 | [4프레임](impact/magic_bolt_electric_impact.png) | 210ms, 반복 끔 |

모든 셀은 32×32, 자동 분할 피벗은 중앙 (16, 16)이다. CAST 시작 100ms에 스태프 끝에서 투사체가 생성되고 발사 스프라이트가 이동하면서 커진다. 발사의 마지막 프레임과 비행의 첫 프레임은 픽셀이 같다.

발사와 비행의 시각 기준점은 좌상단 기준 (22, 15)이다. Unity에서 게임 오브젝트의 원점을 탄두 중심에 둘 때 SpriteRenderer 자식 위치를 32 PPU 기준으로 x=-6/32, y=-1/32 유닛 이동한다. 적중 스프라이트는 중앙 기준으로 충돌 위치에 표시한다.

Unity에는 각 PNG와 같은 이름의 .sprite.json을 가져온다. 재생 시간은 폴더별 timing.json에 있다.
