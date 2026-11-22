# 기본 전투 주문 5종

## Unity 2D

1. `spritesheets`의 PNG를 Unity 프로젝트의 `Assets` 아래에 복사합니다. Inspector에서 **Texture Type = Sprite (2D and UI)**, **Sprite Mode = Multiple**, **Pixels Per Unit = 32**, **Mesh Type = Full Rect**, **Filter Mode = Point**, **Compression = None**, **Generate Mip Maps = Off**, **Alpha Is Transparency = On**으로 설정합니다. 큰 시트가 줄어들지 않도록 `Max Size`는 2048 이상을 사용합니다.
2. **Sprite Editor → Slice → Grid By Cell Size**를 선택합니다. 분할 데이터의 `cell`에 적힌 픽셀 너비·높이를 입력하고 Offset과 Padding을 모두 0으로 둡니다. 모든 시트는 8열입니다. **Custom Pivot**에 `pivotUnity` 값을 입력한 뒤 Apply 합니다. 픽셀 피벗 `pivotTopLeftPx`는 좌상단 원점 기준입니다.
3. 첫 행의 맨 왼쪽부터 오른쪽으로 읽고, 다음 행으로 내려갑니다. `frameCount`까지만 클립에 넣습니다. Unity가 완전 투명 셀을 건너뛸 경우 **Keep Empty Rects**를 켠 뒤 필요하면 마지막 투명 프레임을 직접 추가합니다. 1회 효과의 마지막 투명 프레임은 사용 프레임에 포함됩니다. 마지막 행의 나머지 셀은 여백입니다.
4. Animation 창의 Samples는 분할 데이터의 `fps`를 따릅니다. 기본값은 20(50ms), 차지드 볼트의 회전 파편은 25(40ms)입니다. `loop: true`는 Loop Time을 켜고, `loop: false`는 종료 뒤 효과를 반환하거나 제거합니다. 한 프레임마다 SpriteRenderer의 Sprite 키를 한 개씩 배치합니다.


## 주문별 배치

| 주문 | 적용 |
| --- | --- |
| 파이어 볼트 · 1 | 지팡이 끝에서 `fire-bolt.png`를 생성해 단일 표적까지 이동시킵니다. 64×40px 셀, 불꽃 머리 중심이 피벗이며 머리 지름 약 13px, 꼬리 포함 약 38px입니다. |
| 차지드 볼트 · 1 | `charged-bolt-orb.png`를 여러 개 생성해 진행 각도와 시작 프레임을 다르게 줍니다. 꺾인 번개 조각이 12프레임(0.48초)에 한 바퀴 회전합니다. [비행 미리보기](preview-charged-bolt.gif) |
| 아이스 볼트 · 1 | 발사점에서 `ice-bolt.png`를 재생합니다. 시트 안에 전진 동작이 있으며 명중 시 둔화를 적용합니다. |
| 매직 볼트 (Magic Missile) | `arcane/magic-missile.png`의 파란 에너지 구체 중심을 기준으로 이동시킵니다. 발사 시 가장 가까운 적을 정하고, 비행 중 대상 위치를 향해 방향을 갱신합니다. 둥근 탄두가 앞서고 푸른 잔광이 뒤로 흐르도록 속도 방향에 맞춰 시트를 회전합니다. 48×28px 셀, 탄두 지름 약 14px입니다. [비행 미리보기](preview-magic-bolt.gif) |
| 매직 실드 | 피해 흡수량이 남아 있는 동안 `arcane/magic-shield.png`를 발 피벗에 반복합니다. 피해를 흡수하면 같은 피벗에 `magic-shield-block.png`를 한 번 겹칩니다. 왼쪽에서 맞으면 피격 시트를 좌우 반전하고, 흡수량이 소진되면 유지 효과를 종료합니다. |

[다섯 주문 미리보기](preview-basic-spells.gif)

파이어 볼트와 매직 볼트는 전투에서 잘 보이도록 이전보다 약 1.5배 크게 다시 그렸습니다. 두 시트와 미리보기 GIF, ZIP은 `work/spell-scale-up/`의 `build.py` → `preview.py` 순서로 다시 만듭니다.


[카드 삽화와 프레임 매핑](../wood-spell-cards/skill-art/basic/manifest.json) · [Unity 분할 데이터](unity-slicing.json) · [사용 조건](PIXELFX-LICENSE.txt) · [출처](PIXELFX-NOTICES.md)
