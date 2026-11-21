# The Mage Next Run 에셋

**주문 넣고 갑니다 (Spells to Go)**의 제작 원본과 게임 적용용 에셋을 관리한다. 게임에 가져갈 파일은 [에셋 패키지 목록](exports/INDEX.md)에서 찾을 수 있다.

| 경로 | 내용 |
| --- | --- |
| `exports/<패키지>/` | Unity·Tiled에 가져갈 스프라이트, 애니메이션, 타일맵, UI와 사용 안내 |
| `sources/`, `approved/` | 제작 스크립트와 프레임 구성 |
| `manifests/`, `palettes/`, `styles/` | 제작 매니페스트, 팔레트, 스타일 프로파일 |
| `work/` | 제작 스크립트와 검수 설정 |
| `jobs/`, `art-direction.md` | 제작 작업 기록과 아트 방향 |
| `references/`, `.local/` | 출처·라이선스, 참고 에셋 및 로컬 이관 백업 |

## 패키지 관리

- 시트와 같은 이름의 `.sprite.json`, 타이밍 파일, Unity `.meta`를 해당 에셋과 함께 보관한다. Tiled 맵이 참조하는 이미지와 타일셋의 상대 경로를 유지한다. SVG와 편집 가능한 애니메이션 원본도 해당 패키지 또는 제작 원본과 함께 관리한다.
- 게임에 적용하는 최종 PNG와 사용에 필요한 메타데이터를 `exports/`에 보관한다.
- 외부 레퍼런스에 관한 [출처와 사용 조건](references/reference-components/출처와-라이선스/사용-조건-요약.md)은 문서로 보관한다.

## 제작 도구

기존 제작 스크립트는 작업별로 Pillow, Windows 글꼴, 픽셀 아트 제작 도구 또는 Unity 프로젝트를 사용한다. 과거 제작에 사용한 이미지 원본은 해당 Git 이력을 참고한다. 완성된 에셋과 Tiled 맵은 `exports/`에서 바로 가져올 수 있다.
