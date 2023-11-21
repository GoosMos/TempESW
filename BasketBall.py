import math

backboard_position = (230, 180)

class BasketBall:
    def __init__(self, x, y, power, angle):
        self.x = x
        self.y = y
        self.vx = power * math.cos(math.radians(angle))  # x축 방향의 속도
        self.vy = power * math.sin(math.radians(angle))  # y축 방향의 속도
        self.gravity = 0.5
        self.damping_factor = 0.9

    # def move(self):
    #     self.x += self.vx
    #     self.y -= self.vy
    #     self.vy -= self.gravity  # y축 방향의 속도를 업데이트

    #     # 화면 범위 내로 공의 위치를 조정
    #     if self.x < 0:
    #         self.x = 0
    #     elif self.x > 240:
    #         self.x = 240

    #     if self.y < 0:
    #         self.y = 0
    #     elif self.y > 240:
    #         self.y = 240
    #         # test
    #     if backboard_position[0] <= self.x <= backboard_position[0] + 20 and \
    #        backboard_position[1] <= self.y <= backboard_position[1] + 20:
    #         self.vx = -self.vx  # x축 방향의 속도를 반전시킴

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gravity  # y축 방향의 속도를 업데이트
    

        # 화면 범위 내로 공의 위치를 조정
        if self.x < 0 or self.x > 240:
            self.vx = -self.vx * self.damping_factor  # x축 방향의 속도를 반전시킴
            self.x = max(0, min(240, self.x))  # x좌표가 화면 범위를 벗어나지 않도록 조정
            self.damping_factor *= 0.4
        if self.y < 0 or self.y > 240:
            self.vy = -self.vy  * self.damping_factor # y축 방향의 속도를 반전시킴
            self.y = max(0, min(240, self.y))  # y좌표가 화면 범위를 벗어나지 않도록 조정
            self.damping_factor *= 0.4

        # 백보드와 충돌 처리
        if backboard_position[0] <= self.x <= backboard_position[0] + 20 and \
        backboard_position[1] <= self.y <= backboard_position[1] + 20:
            self.vx = -self.vx * damping_factor # x축 방향의 속도를 반전시킴
            self.vy = -self.vy * damping_factor
            self.damping_factor *= 0.4
        
        if self.damping_factor < 0.2 :
            self.damping_factor == 0



class Hoop:
    hoop_width = 20
    hoop_hegith = 10
    hoop_x = (240 - hoop_width) / 2
    hoop_y = 0
