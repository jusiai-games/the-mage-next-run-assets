# 주문 넣고 갑니다 · 주문 이펙트 30종

화염·냉기·번개 각 10종. 각 주문은 같은 이름의 투명 RGBA PNG 스프라이트시트와 애니메이션 GIF를 한 장씩 제공합니다. GIF는 2배 확대와 어두운 미리보기 배경으로 반복 재생됩니다. 1회 재생 효과의 GIF에는 다음 재생 전 200ms 여백이 있습니다.

- `spritesheets/{fire,cold,lightning}/` — Unity에서 사용하는 시트 30장.
- `gifs/{fire,cold,lightning}/` — 주문별 재생 미리보기 30개.
- [전체 미리보기](contact-sheet.png) — 주문마다 대표 프레임 한 장.
- [Unity 분할 데이터](unity-slicing.json) — 주문별 셀 너비·높이, 사용 프레임 수, 재생 방식, 피벗, 경로, 권장 배치.

## Unity 2D

1. `spritesheets`의 PNG를 Unity 프로젝트의 `Assets` 아래에 복사합니다. Inspector에서 **Texture Type = Sprite (2D and UI)**, **Sprite Mode = Multiple**, **Pixels Per Unit = 32**, **Mesh Type = Full Rect**, **Filter Mode = Point**, **Compression = None**, **Generate Mip Maps = Off**, **Alpha Is Transparency = On**으로 설정합니다. 큰 시트가 줄어들지 않도록 `Max Size`는 2048 이상을 사용합니다.
2. **Sprite Editor → Slice → Grid By Cell Size**를 선택합니다. 분할 데이터의 `cell`에 적힌 픽셀 너비·높이를 입력하고 Offset과 Padding을 모두 0으로 둡니다. 모든 시트는 8열입니다. **Custom Pivot**에 `pivotUnity` 값을 입력한 뒤 Apply 합니다. 픽셀 피벗 `pivotTopLeftPx`는 좌상단 원점 기준입니다.
3. 첫 행의 맨 왼쪽부터 오른쪽으로 읽고, 다음 행으로 내려갑니다. `frameCount`까지만 클립에 넣습니다. Unity가 완전 투명 셀을 건너뛸 경우 **Keep Empty Rects**를 켠 뒤 필요하면 마지막 투명 프레임을 직접 추가합니다. 1회 효과의 마지막 투명 프레임은 사용 프레임에 포함됩니다. 마지막 행의 나머지 셀은 여백입니다.
4. Animation 창의 **Samples = 20**, 프레임 간격은 **50ms**입니다. `loop: true`는 Loop Time을 켜고, `loop: false`는 종료 뒤 효과를 반환하거나 제거합니다. 한 프레임마다 SpriteRenderer의 Sprite 키를 한 개씩 배치합니다.

### 전투 화면 배치

- Fire Bolt, Fire Ball, Glacial Spike처럼 피벗이 탄두 근처에 있는 비행 효과는 전투 로직으로 이동시킵니다. 시트 안에서 이동하는 Charged Bolt나 Ice Bolt는 발사 범위와 이동 로직이 중복되지 않게 배치합니다.
- 시전자 보호막과 오라는 마법사의 발 위치에 연결합니다. Meteor, Thunder Storm, Telekinesis는 대상 지점에, Fire Wall과 Blaze는 지면에 배치합니다.
- 방향이 있는 효과의 기본 방향은 오른쪽입니다. 왼쪽 발사는 SpriteRenderer의 Flip X를 사용합니다. Chain Lightning의 연결 위치는 시트에 그려져 있습니다. 대상 간격이 달라지는 전투에서는 링크 단위로 맞춰 배치해야 합니다.
- 3종 Mastery와 Warmth는 패시브가 발동하거나 업그레이드될 때 보여줄 수 있는 시각 효과입니다. 게임에서 재생 시점과 지속 시간은 전투 로직으로 정합니다.

PixelFX 기반 효과와 라이선스는 [라이선스](PIXELFX-LICENSE.txt) 및 [출처 고지](PIXELFX-NOTICES.md)를 참고하세요. 각 효과의 제작 출처는 분할 데이터의 `source`에 있습니다.
