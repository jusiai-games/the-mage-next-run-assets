# 빠른 시전 후드 마법사

네 동작 모두 32×32, 발 피벗 (16, 28), 32 PPU다. 각 PNG를 같은 이름의 .sprite.json과 함께 Unity로 가져온다.

- [걷기 4프레임](walk-v2/hood_staff_walk.png)
- [대기 5프레임](idle/hood_staff_idle.png)
- [시전 5프레임](cast/hood_staff_cast.png)
- [쓰러짐 6프레임](fall/hood_staff_fall.png)

시전은 30 Samples, 반복 끔. 키 위치는 0, 1, 3, 5, 8이며, 발사는 샘플 3의 세 번째 프레임에서 시작한다. 실제 투사체를 만드는 타이밍도 시전 시작 후 0.10초에 맞춘다. 스태프 끝 위치는 cast/timing.json을 참고한다. 초원과 그림자는 기존 hood-staff-32-final/meadow를 사용한다.
