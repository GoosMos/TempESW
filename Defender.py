import random
import numpy as np

class Defender:
    def __init__(self, width, height):
        self.position = np.array([120, 210, 150, 240])
        self.jump = False
        self.state = False
        self.user_x = 0
        self.jump_height = 0

    def move(self, user_x):
        self.user_x = user_x
        self.position[0] = max(self.position[0], self.user_x + 5)  # 수비수의 x축 위치는 항상 사용자의 x축 위치보다 큽니다.
        self.position[2] = max(self.position[2], self.user_x + 35)  # 수비수의 x축 위치는 항상 사용자의 x축 위치보다 큽니다.
        
        temp = random.randint(-5, 5)
        self.position[0] += temp
        self.position[2] += temp

        self.position[0] = np.clip(self.position[0], 55, 200)
        self.position[2] = np.clip(self.position[2], 55, 200)
        
        if not self.jump and random.random() < 0.1: # 점프 상태가 아닐 때, 랜덤으로 점프
            self.jump = True
            self.state = True
            self.jump_height = 0

        if self.jump: # 점프가 True일 때
            if self.state and self.jump_height < 130 : # 고점 도달
                self.jump_height += 10
                self.position[1] -= 10
                self.position[3] -= 10
                if (self.jump_height == 130): self.state = False
            else : # 130이 되었을 때
                self.jump_height -= 10
                self.position[1] += 10
                self.position[3] += 10
                if (self.jump_height == 0): self.jump = False