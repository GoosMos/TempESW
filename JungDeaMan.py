import numpy as np
# 좌상단 (0, 0), 우하단 (240, 240)

class JungDeaMan:
    def __init__(self, width, height) :
        self.shoulderAngel = 45
        self.power = 12
        self.appearance = 'circle'
        self.position = np.array([30, 210 , 40, 240])


    def move(self, command = None) :
        # 상, 하 -> 팔 각도 변경
        if command['up_pressed']:
            if (self.shoulderAngel != 90) : self.shoulderAngel += 5
            print("정대만의 팔 각도 상승!!", end = " ")
            print("현재 팔각도 : ", self.shoulderAngel)
    
        
        if command['down_pressed']:
            if (self.shoulderAngel != 0) : self.shoulderAngel -= 5
            print("정대만의 팔 각도 하강!!", end = " ")
            print("현재 팔각도 : ", self.shoulderAngel)

        if command['left_pressed']:
            if (self.position[0] != 0) : 
                self.position[0] -= 5
                self.position[2] -= 5
            print("정대만의 파워 감소 ", self.power)
        
        if command['right_pressed']:
            if (self.position[0] != 120) : 
                self.position[0] += 5
                self.position[2] += 5
            print("정대만의 파워 증가 ", self.power)