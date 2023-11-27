import math
import Defender

hoop_position = (210, 130, 240, 140)

class BasketBall:
    def __init__(self, x, y, power, angle):
        self.x = x
        self.y = y
        self.vx = power * math.cos(math.radians(angle))  # x축 방향의 속도
        self.vy = power * math.sin(math.radians(angle))  # y축 방향의 속도
        self.gravity = 0.5
        self.damping_factor = 0.9

    def move(self, defender):
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gravity  # y축 방향의 속도를 업데이트

        if defender.position[0] <= self.x <= defender.position[2] and \
        defender.position[1] <= self.y <= defender.position[3] :
            self.vx = -self.vx * self.damping_factor
            self.vy = -self.vy * self.damping_factor
            print("Blocked")


        # 화면 범위 내로 공의 위치를 조정
        if self.x < 0 or self.x > 240:
            self.vx = 0.8 * (-self.vx * self.damping_factor)  # x축 방향의 속도를 반전시킴
            self.x = max(0, min(240, self.x))  # x좌표가 화면 범위를 벗어나지 않도록 조정
            self.damping_factor *= 0.4
        if self.y < 0 or self.y > 240:
            self.vy = 0.8 * (-self.vy  * self.damping_factor) # y축 방향의 속도를 반전시킴
            self.y = max(0, min(240, self.y))  # y좌표가 화면 범위를 벗어나지 않도록 조정
            self.damping_factor *= 0.4

        # 백보드와 충돌 처리
        if hoop_position[0] <= self.x <= hoop_position[2] and \
        hoop_position[1] <= self.y <= hoop_position[3] :
            self.vx = 0

        
        if self.damping_factor < 0.2 :
            self.damping_factor == 0


    def isGround(self) :
        return self.y >= 240 and self
