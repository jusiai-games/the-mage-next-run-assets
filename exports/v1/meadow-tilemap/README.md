# 초원 전투 타일맵 UI

게임 제목은 **주문 넣고 갑니다**, 영문 제목은 **Spells to Go**다. 두 제목은 메인 화면 상단의 고정 제목 레이어에 배치한다.

모든 맵은 160×352 논리 픽셀에 16×16px 타일을 쓰는 10열×22행이다. Tiled에는 `game-title.tmj`, `stage-start.tmj`, `battle.tmj`, `battle-six-slots.tmj`가 있다. 네 맵은 같은 `meadow-ui-tiles.png`를 사용한다.

| 파일 | 내용 |
| --- | --- |
| `game-title-background.png`, `game-title-clouds.png` | 타이틀의 고정 배경과 반복 구름 레이어 |
| `stage-far-loop.png`, `stage-ground-loop.png` | 전투 시작의 반복 원경과 흙길이 합쳐진 초원 레이어 |
| `stage-path-strip.png` | 기존 초원 그림의 흙길 부분을 16×16px 텍스처로 잘라 구성한 별도 텍스처 레이어 |
| `stage-slime-hop.png`, `stage-slime-hop.json` | 32×32px 원본 크기의 슬라임 전진 18프레임과 재생 시간 |
| `*-foreground.png` | 시작 화면의 정지 제목과 버튼 레이어 |
| `spell-slot-layouts.png` | 주문 3개와 6개를 장착했을 때의 하단 HUD 비교 |
| `spell-cooldown-styles.png` | 세 주문의 시전 직후, 25%, 50%, 75%, 사용 가능 |
| `sprites/` | 슬롯 프레임 22×22px, 주문 안쪽 18×18px 6종, 준비 테두리 22×22px, 원소별 충전 경계 18×1px 6종 |
| `SpellCooldownView.cs` | 주문마다 별도로 연결하는 Unity 슬롯 표시 코드 |
| `StartStripScroll.cs`, `StageSlimeHop.cs` | 배경 레이어 반복과 슬라임 전진 재생 코드 |

게임 시작은 폐허가 보이는 초원을 고정하고 구름만 오른쪽으로 흐르게 한다. 전투 시작은 다른 초원의 원경과 지면을 각각 왼쪽으로 흘리며, 작은 슬라임은 오른쪽을 보고 뛴다. 전투 HUD는 방어막 에너지 5/5와 전투력 120을 예시로 표시한다. 장착한 주문 아이콘은 2px 간격으로 한 줄에 최대 6개가 들어간다.

## 화면 픽셀 배율 검수

1. 1배 원본의 논리 크기와 화면에 들어가는 에셋의 기준 크기를 기록한다. 이 샘플은 화면 160×352px, 타일 16×16px, 양쪽 시작 버튼 92×28px이다. 타이틀 배경은 원본에서 세로 구도를 먼저 잡고 출력 크기로 한 번 샘플링한다.
2. 빌드에서 모든 화면 레이어의 논리 크기를 검사한다. 타이틀 배경은 2·3·4배로 규칙적으로 반복된 픽셀 블록도 검사한다. 아틀라스에서 재조립한 화면이 원본과 일치하는지 이어서 검사한다.
3. 타이틀·전투 시작·전투 화면을 같은 정수 배율로 나란히 확인한다. 타일 경계, 배경의 돌·풀 가장자리, 같은 버튼을 눈금 기준으로 대조한다. 일부 영역만 확대된 그림이나 의도적으로 굵게 그린 에셋은 이 단계에서 판별한다. 기기 실장 시 목표 화면 크기에서 최종 스케일도 확인한다.

## 시작 화면 애니메이션

- 타이틀에서는 고정 배경, 구름, 전경 순으로 그린다. 다른 정지 레이어와 같은 PPU로 맞춘 구름 스프라이트 두 장을 같은 부모 아래 두고 `StartStripScroll`에 연결한다. `pixelsPerSecond`를 `-10`으로 설정하면 오른쪽으로 흐른다.
- 전투 시작의 원경과 지면에는 같은 방식으로 각각 두 장을 배치한다. `pixelsPerSecond`를 각각 `160 / 8.64`, `320 / 8.64`(약 18.52, 37.04)로 설정한다. 흙길은 지면과 함께 움직이며 Tiled의 `stage-start.tmj`에서는 별도 **흙길** 레이어로 편집할 수 있다.
- 슬라임 시트는 32×32px 셀로 나누고 피벗은 좌상단 픽셀 좌표 (16, 28)로 둔다. `StageSlimeHop`에 왼쪽부터 18개 프레임을 연결한다. 기존 전진 프레임을 오른쪽으로 뒤집어 재사용한다. 전경의 제목과 버튼을 가장 앞에 둔다.

## 주문 쿨타임

- 프레임 중앙에 주문 안쪽 SpriteRenderer(`spellFace`)를 놓고, 프레임과 같은 위치에 준비 테두리(`readyRim`)를 겹친다. 주문 안쪽은 SpriteAtlas에 패킹하지 않은 스프라이트로 가져온다.
- `spellFace` 아래에 자식 SpriteRenderer 두 개를 만든다. `chargeFace`는 빈 스프라이트로 시작하고, `chargeEdge`에는 주문 이름이 같은 `*-cooldown-edge.png`를 같은 PPU와 중앙 피벗으로 넣는다. 그리기 순서는 `spellFace` → `chargeFace` → `chargeEdge`다. 자식의 회전과 크기는 기본값을 사용한다.
- 마법 발동이 확정되면 해당 슬롯의 `TryStartCooldown(seconds)`를 호출한다. 같은 슬롯이 충전 중이면 호출은 `false`를 반환한다.
- 슬롯 안쪽은 어두운 색으로 시작한다. 충전된 높이만큼 아래에서 원래 색이 드러나며, 밝은 경계선이 위로 이동한다. 가득 차면 경계선은 사라지고 금색 테두리가 켜진다. 시간이 멈춘 전투에서는 쿨타임도 멈춘다.

## 참고한 파일

- 손패 카드의 출발점은 비교 시안 **`spell-card-directions.png`의 C · 원소**다. 적용된 앞면은 `hand-fire.png`, `hand-lightning.png`, `hand-burst.png`이며 삽화에 쓴 기존 아이콘은 `icon-fire.png`, `icon-lightning.png`, `icon-burst.png`다.
- 하단 스펠 창은 **`스킬-트리-패널-Questwood-1x.png`**의 제목판과 안쪽 홈, **`spell-panel.png`**, **`spell-slots.png`**의 배치와 슬롯 구조를 참고했다. 새 프레임에는 프로젝트의 나무·조약돌 스프라이트인 `panel.png`, `hud.png`, `card.png`를 사용했다.
- 확장 예시의 낙석·물기둥·회오리 아이콘은 Foozle의 [Pixel Magic Effects](https://foozlecc.itch.io/pixel-magic-sprite-effects)에서 가져왔다.
