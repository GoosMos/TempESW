import math
print("Hellllllll")
class BasketBall:
    def __init__(self, x, y, power, angle):
        self.x = x
        self.y = y
        self.vx = power * math.cos(math.radians(angle))  # x축 방향의 속도
        self.vy = power * math.sin(math.radians(angle))  # y축 방향의 속도
        self.gravity = 0.5

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gravity  # y축 방향의 속도를 업데이트

        # 화면 범위 내로 공의 위치를 조정
        if self.x < 0:
            self.x = 0
        elif self.x > 240:
            self.x = 240

        if self.y < 0:
            self.y = 0
        elif self.y > 240:
            self.y = 240
            # test

class Hoop:
    hoop_width = 20
    hoop_hegith = 10
    hoop_x = (240 - hoop_width) / 2
    hoop_y = 0
