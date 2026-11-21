# 주문 넣고 갑니다 · Unity UI 타일

깎은 호두색 나무와 회청색 조약돌에 주문 카드의 황동색 테두리와 양피지를 접목했다. 프레임 한 장은 36×36px이고, 모서리·변·중앙이 각각 12×12px이다. 모든 스프라이트는 텍스트가 없는 투명 PNG다.

| 스프라이트 | 용도 |
|---|---|
| `panel` | 인벤토리, 보상, 확인창 외곽 |
| `dialogue`, `speaker-scroll`, `dialogue-tail` | 대화창 본체, 말린 양피지 화자 이름표, 선택해서 붙이는 꼬리 |
| `nameplate` | 남색 보조 프레임 |
| `spell-clasp`, `panel-crest` | 이름판용 주문 문양, 패널 중앙 위쪽에 붙이는 장식 |
| `button-normal`, `button-highlighted`, `button-pressed`, `button-disabled` | 같은 크기의 버튼 상태 4종 |
| `inventory-slot-normal`, `inventory-slot-selected`, `inventory-slot-locked` | 24×24px 인벤토리 슬롯 3종 |
| `inventory-potion`, `inventory-rune`, `inventory-scroll` | 슬롯 가운데에 겹치는 18×18px 아이템 아이콘 |

## Unity Canvas에 적용

1. `package/Assets/SpellsToGo` 폴더를 Unity 프로젝트의 `Assets` 안에 복사한다. PNG와 함께 들어 있는 `.meta`가 32 PPU, Point 필터, 무압축과 9슬라이스용 12px 경계를 설정한다. 기존 스프라이트의 GUID는 유지된다.
2. Canvas 아래에 **UI → Image**를 만들고 원하는 스프라이트를 Source Image에 넣는다. 본체, 이름판, 버튼에는 **Image Type → Sliced**, 꼬리와 장식에는 **Simple**을 선택한다. 모서리를 원본 픽셀 크기로 표시하려면 Canvas의 **Reference Pixels Per Unit**을 32로 맞춘다. 이 설정에서는 RectTransform의 너비와 높이를 각각 24 이상으로 둔다. 이전 버전의 작은 버튼은 높이를 확인한다.
3. `speaker-scroll`은 대화창 위쪽에 Sliced Image로 붙인다. 크기는 84×28에서 시작하고, 이름 길이에 맞춰 가로폭을 조절한다. 양피지 위에는 진한 갈색 글씨를 쓰고 양끝 12px를 여백으로 둔다. 이름표와 텍스트의 Raycast Target을 끈다. 꼬리는 본체 뒤에 5px 겹치고, 패널 장식은 패널 위쪽 가운데에 놓는다.
4. 버튼의 Target Graphic은 같은 Image로 지정하고 **Transition → Sprite Swap**을 선택한다. Normal은 Image의 Source Image에, Highlighted·Pressed·Disabled는 각 Sprite 슬롯에 넣는다. 키보드나 게임패드로 선택했을 때는 Highlighted를 Selected에도 연결한다.

## 타일 단위로 조립

`Reference/ui-tiles-12px.png`는 144×108px 시트다. 간격과 여백은 0px이며, 함께 제공하는 JSON의 행과 열은 좌상단 (0, 0)에서 센다. 각 3×3 블록의 네 모서리를 고정하고, 위아래 변은 가로로, 좌우 변은 세로로, 가운데는 양 방향으로 반복해 박스를 조립할 수 있다. Unity의 일반 Canvas에서는 위의 개별 9슬라이스 스프라이트를 쓴다.

인벤토리 슬롯과 아이콘은 `Image Type → Simple`로 배치한다.

양피지 이름표의 기준은 첨부 레퍼런스 두 번째 이미지의 가로 띠다. 중앙 위아래는 얇고 곧게 두고, 끝에서 종이 앞면이 말린 뒷면을 덮어 깊이가 읽히도록 그린다. 빌드는 48px·84px·101px 폭에서 고정 모서리와 수평 중앙을 확인한다.
