# 주문 넣고 갑니다 · 원소 주문 효과

- 범위 — 화염·냉기·번개 계열별 10개. 주문 이름은 참조용이며 동작과 그래픽은 이 프로젝트의 전투 화면에 맞춘 픽셀 효과로 제작.
- 기존 작업 기준 — 모바일 160×352 논리 픽셀, 마법사 약 26px, 32 PPU. [기존 시전·피격 미리보기](../exports/magic-bolt-electric/cast-flight-impact.gif)의 번개 색을 사용.
- 전용 제작 결정 — 따뜻한 살구와 금색 화염, 연청록 냉기, 하늘빛 번개. 모든 HEX는 [게임 팔레트](../palettes/project.json)에 포함. 프레임은 투명 RGBA, 20 FPS, 위에서 아래로 8열 배치. 피벗과 캔버스는 효과의 실제 사용 위치에 맞춤.
- 제작 명세 및 원본 — [주문 대응표](../sources/sorceress-vfx/spells.mjs), [제작한 동작](../sources/sorceress-vfx/custom.mjs), [출력 도구](../sources/sorceress-vfx/render.mjs). Node, PixelFX 0.3.1 및 FFmpeg로 재생성.
- 결과 — [PNG 및 GIF 패키지 안내](../exports/sorceress-vfx/README.md).
