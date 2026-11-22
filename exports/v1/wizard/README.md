# 마법사 주인공

적갈색 머리, 보라 망토와 청록 수정 지팡이의 채택본이다. 기존 Unity 참조를 유지하기 위해 시트 파일명과 스프라이트 이름은 유지한다.

네 동작 모두 32×32, 발 피벗 (16, 28), 32 PPU다. 각 PNG를 같은 이름의 .sprite.json과 함께 Unity로 가져온다.

- [걷기 10프레임](walk/hood_staff_walk.png): 상체를 대기 자세 하나로 고정하고 다리를 새로 그린 정리본이다. 변경 내용은 [걷기 정리 기록](../../../work/wizard-walk-clean/README.md)에 있다.
- [대기 5프레임](idle/hood_staff_idle.png)
- [시전 8프레임](cast/hood_staff_cast.png)
- [쓰러짐 6프레임](fall/hood_staff_fall.png)

시전은 30 Samples, 반복 끔. 키 위치는 0, 1, 3, 4, 5, 6, 7, 8이며, 발사는 샘플 3의 세 번째 프레임에서 시작한다. 실제 투사체를 만드는 타이밍도 시전 시작 후 0.10초에 맞춘다. 스태프 끝 위치는 cast/timing.json을 참고한다. 초원과 그림자는 [초원 지형 패키지](../meadow-terrain/meadow/layout.json)에 있다.

## 후속 작업 기준

- [채택된 프레임 비교판](../wizard-title-hero/preview.png)의 적갈색 머리, 단순한 오른쪽 눈매, 보라 망토와 청록 수정 지팡이가 디자인 기준이다. 대기 기준 얼굴을 걷기와 시전에도 사용한다.
- 주인공은 대기 5장, 걷기 10장, 시전 8장, 쓰러짐 6장이다. 모자이크처럼 보이는 부분은 인접 픽셀과 외곽선을 국소적으로 정리한다. 채택 팔레트는 투명을 제외한 28색이며, 이를 줄이거나 프레임을 빼는 변경은 별도 요청이 있을 때 진행한다.
- 머리카락, 망토, 장화의 어두운 바깥 윤곽을 살린다. 허리 안쪽은 망토와 가죽 띠의 색으로 이어서 검은 띠가 몸통을 가로지르지 않게 한다. 지팡이의 수정과 금빛 받침을 보존하고, 축이 꺾여 보이면 막대 픽셀만 정렬한다.
- 32×32 셀, 좌상단 기준 발 피벗 (16, 28), 32 PPU를 유지한다. 시전 중 불투명 발바닥은 y=27, 머리 높이 변화는 최대 1px이다. 발사 시점은 100ms, 세 번째 프레임 수정 끝은 (28, 14)다. 걷기와 시전의 재생 순서는 timing.json의 playback_frame_order_zero_based를 읽는다. Unity의 Mage_Release는 발사 직후부터 재생하는 6개 키이며, 별도 unity_release_frame_order_zero_based를 사용한다.
- 수정본을 적용할 때 이 패키지의 PNG와 .sprite.json 해시를 맞춘다. 별도 Unity 프로젝트의 Assets/Art/PixelArt/wizard_* 폴더에 있는 PNG를 교체할 경우 기존 파일명, 스프라이트 이름 및 .meta를 유지한다. 대기 첫 프레임이 바뀌면 [모바일 초원의 대기 이미지](../meadow-wave-mobile/README.md)도 맞춘다.
- 현재 채택본은 PNG, 프레임 분할 및 Unity 에셋 참조를 확인했다. Unity 플레이 모드에서 애니메이션 재생을 확인하는 작업이 남아 있다.

## 디자인 검토 기록

[마법사 리디자인 시안](../../../work/character-redesign/README.md)은 32×32 대기 포즈 비교용이다.

[전투 마법사 시안](../../../work/character-redesign-combat/README.md)은 장비와 전투 실루엣을 비교하는 대기 포즈다.

[후드 마법사 성격 시안](../../../work/character-redesign-personality/README.md)은 기존 콘셉트에서 얼굴과 의상 디테일을 비교하는 대기 포즈다.

[후드 마법사 여행자 시안](../../../work/wizard-traveler/README.md)은 주인공의 실루엣·자세·소품을 비교하는 정지 포즈다.

[후드 마법사 주인공 시안](../../../work/wizard-hero/README.md)은 새 실루엣을 비교하는 정지 포즈다.

[후드 마법사 수정 시안](../../../work/wizard-hero-refined/README.md)은 체형과 망토 실루엣을 비교하는 정지 포즈다.

[두루마리 마법사 시안](../../../work/wizard-scroll-mage/README.md)은 머리와 코트가 드러나는 별도 주인공 디자인의 정지 포즈다.

[16비트 전투 도트 시안](../../../work/wizard-snes/README.md)은 기존 후드 마법사를 전투 도트 스타일로 그린 정지 포즈다.

[진홍 코트 마법사 시안](../../../work/wizard-crimson/README.md)은 새 주인공의 시전 준비 실루엣을 비교하는 정지 포즈다.

[후드를 벗은 마법사](../../../work/wizard-unhooded/README.md)는 기존 대기 포즈의 머리와 무표정 얼굴을 비교하는 시안이다.

[표지 마법사 스프라이트](../../../work/wizard-title-sprite/README.md)는 표지 주인공의 의상과 장비를 적용한 정지 포즈 시안이다.

[망토 마법사 전투 시안](../../../work/wizard-battle-mantle/README.md)은 넓은 어깨 망토와 시전 자세를 비교하는 정지 포즈다.

[옆모습 전투 마법사](../../../work/wizard-side-battle/README.md)는 오른쪽 옆모습과 팔다리 겹침을 비교하는 정지 포즈다.

[원본 자세의 후드 벗은 마법사](../../../work/wizard-original-pose/README.md)는 기존 대기 프레임에서 머리만 수정한 디자인 시안이다.

[첨부 캐릭터 축소](../../../work/wizard-portrait-reduction/README.md)는 원화를 게임 크기로 줄인 정지 포즈 시안이다.

[마법사 도트 제작 방식 비교](../../../work/wizard-pixel-comparison/README.md)는 작은 전투 도트와 기존 포즈 기반의 새 디자인을 비교하는 정지 포즈다.

[표지 디자인 마법사 교체 패키지](../wizard-title-hero/README.md)는 대기·걷기·시전·쓰러짐 제작 원본과 프레임 비교판을 담고 있다. 게임 적용 시트는 이 문서 상단에서 고른다. walk/transition-review/의 보고서는 이전 후드 디자인의 검수 기록이다.

[전신 걷기 10프레임 시안](../../../work/wizard-walk-review/README.md)은 복원된 걷기 시트와 비교하는 검토 자료다.
