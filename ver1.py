from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import JungDeaMan
import Joystick
import Defender
import math
import Defender
import os
import time

hoop_position = (210, 130, 240, 140)

# 점수를 저장하는 함수
def save_score(score) :
    if os.path.exists("scores.txt"):
        with open("scores.txt", 'r') as f:
            scores = [int(line.strip()) for line in f.readlines()]
    else:
        scores = []
    
    scores.append(score)
    scores.sort(reverse=True)
    scores = scores[:5]

    with open("scores.txt", 'w') as f:
        for score in scores:
            f.write(str(score) + '\n')

# 점수를 불러오는 함수
def load_scores():
    if os.path.exists("scores.txt"):
        with open("scores.txt", 'r') as f:
            scores = [int(line.strip()) for line in f.readlines()]
    else:
        scores = []

    return scores

class BasketBall:
    def __init__(self, x, y, power, angle):
        self.x = x
        self.y = y
        self.start_x = x
        self.vx = power * math.cos(math.radians(angle))  # x축 방향의 속도
        self.vy = power * math.sin(math.radians(angle))  # y축 방향의 속도
        self.gravity = 0.5 # 공에 중력을 적용하기 위함
        self.damping_factor = 0.9 # 공이 벽면에 부딪히고 튕겨나올 때 속도를 감소시키기 위한 변수
        self.scored = False # 공이 림을 통과한 경우 

    def move(self, defender):
        self.x += self.vx
        self.y -= self.vy
        self.vy -= self.gravity  # y축 방향의 속도를 업데이트
        global score

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

        # 림의 앞쪽을 맞았을 때 공이 튕겨져 나오도록 한다.
        if hoop_position[0] <= self.x <= hoop_position[0] + 3 and \
        hoop_position[1] <= self.y <= hoop_position[3] :
            self.vx = -self.vx 
            self.vy = -self.vy
        
        # 림의 뒷쪽을 맞았을 때 공이 튕겨져 나오도록 한다.
        if 235 < self.x <= 240 and \
        hoop_position[1] <= self.y <= hoop_position[3] :
            self.vx = -self.vx 
            self.vy = -self.vy 
        
        # 림을 통과한 경우 점수를 1번 올리기 위해 
        if hoop_position[0] + 3 < self.x <= hoop_position[2] - 5 and \
        hoop_position[1] <= self.y <= hoop_position[3] :
            self.vx = 0
            if not self.scored :
                # 농구공이 던져진 위치에 따라 3점슛, 2점슛이 결정
                if (self.start_x < 70) : 
                    score += 3
                    print("3 !! Score : ", score)    
                else : 
                    score += 2
                    print("2 !! Score : ", score)
                self.scored = True
        else :
            self.scored = False

        
        if self.damping_factor < 0.2 :
            self.damping_factor == 0

    def isGround(self) :
        return self.y >= 240 and self


joystick = Joystick.Joystick()

# 각 이미지를 불러오기
ballImage = Image.open("/home/kau-esw/project/basketball.png").resize((10, 10)) # 농구공 이미지
net = Image.open("/home/kau-esw/project/background.png").resize((240, 240)) # 농구코드 이미지
startImage = Image.open("/home/kau-esw/project/start.png").resize((240, 240)) # 시작, 종료화면
DeaMan = Image.open("/home/kau-esw/project/DeaMan.png").resize((30, 30)) # 정대만
DefenderImage = Image.open("/home/kau-esw/project/defense.png").resize((30, 30)) # 수비수

# 이미지의 모드 설정 == 디스플레이 전체에 대한 초기화
my_image = Image.new("RGB", (joystick.width, joystick.height)) 
my_draw = ImageDraw.Draw(my_image)
prev_button_A = True

while True:
    score = 0 # 총 점수 초기화
    LifeCount = 5 # 총 시도횟수 초기화
    JungDaeMan = JungDeaMan.JungDeaMan() # 정대만
    defender = Defender.Defender() # 수비수
    balls = []

    while True:
        if not joystick.button_A.value and prev_button_A:
            # A키를 누르면 게임을 시작
            print("시작합니다.")
            break
        my_image.paste(startImage)
        my_draw.text((90, 130), f"Press A key", fill = (0, 0, 0))
        joystick.disp.image(my_image)

    prev_button_A = joystick.button_A.value

    while True:
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

        if not joystick.button_U.value:  # up pressed
            command['up_pressed'] = True
            command['move'] = True

        if not joystick.button_D.value:  # down pressed
            command['down_pressed'] = True
            command['move'] = True

        if not joystick.button_L.value:  # left pressed
            command['left_pressed'] = True
            command['move'] = True

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True
        # A키를 누르면 슈팅을 시도
        if not joystick.button_A.value and prev_button_A:
            LifeCount -= 1
            print("남은 시도 횟수 : ", LifeCount)
            balls.append(BasketBall(JungDaeMan.position[0], JungDaeMan.position[1], JungDaeMan.power, JungDaeMan.shoulderAngel))
        prev_button_A = joystick.button_A.value

        # 방향키 입력에 따른 정대만과 수비수의 움직임
        JungDaeMan.move(command)
        defender.move(JungDaeMan.position[0])


        my_image.paste(net, (0, 0), net)
        my_image.paste(DefenderImage, (defender.position[0], defender.position[1]), DefenderImage)
        my_image.paste(DeaMan, (JungDaeMan.position[0], JungDaeMan.position[1]), DeaMan) # 정대만 그리기
        my_draw.rectangle((0, 0, joystick.width, 5), fill = (255, 0, 0, 100)) # 3점 라인 바
        my_draw.rectangle((0, 0, (JungDaeMan.position[0] / 120) * 240, 5), fill = (255, 255, 0, 100)) # 3점 라인 바
        my_draw.rectangle((0, 5, (JungDaeMan.shoulderAngel / 90 * 240), 10), fill = (255, 0, 255)) # 각도 바
        
        for i in range(1, LifeCount + 1) :
            my_image.paste(ballImage, (20 * i, 15), ballImage)

        for ball in balls:
            ball.move(defender) # 농구공의 움직임
            my_image.paste(ballImage, (int(ball.x), int(ball.y)), ballImage)

        # 림을 그리기
        my_draw.rectangle((hoop_position[0], hoop_position[1],
                            hoop_position[2], hoop_position[3]), fill = (0, 0, 0))
        
        balls = [ball for ball in balls if not ball.isGround()]
        my_draw.text((0, 30), f"Score : {score}", fill = (255, 255, 255))
        joystick.disp.image(my_image) 

        # 기회가 소진되면 탈출
        if LifeCount == -1: break


    while LifeCount >= 0 and len(balls) > 0: 
        # 게임이 끝났고, 아직 화면에 남아있는 공이 있을 경우
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        if LifeCount > 0: # 아직 던질 공이 남아있는 경우
            if not joystick.button_U.value:  # up pressed
                command['up_pressed'] = True
                command['move'] = True

            if not joystick.button_D.value:  # down pressed
                command['down_pressed'] = True
                command['move'] = True

            if not joystick.button_L.value:  # left pressed
                command['left_pressed'] = True
                command['move'] = True

            if not joystick.button_R.value:  # right pressed
                command['right_pressed'] = True
                command['move'] = True

            if not joystick.button_A.value and prev_button_A:
                LifeCount -= 1
                print("남은 시도 횟수 : ", LifeCount)    
                balls.append(BasketBall(JungDaeMan.position[0], JungDaeMan.position[1], JungDaeMan.power, JungDaeMan.shoulderAngel))
            prev_button_A = joystick.button_A.value

            JungDaeMan.move(command)
            defender.move(JungDaeMan.position[0])

        for ball in balls:
            ball.move(defender)
            if ball.y > 240: # 공이 화면 밖으로 나갔다면
                balls.remove(ball) # 해당 공을 제거합니다.

    # 점수를 저장 및 점수 불러오기
    save_score(score)
    scores = load_scores()
    for i, logscore in enumerate(scores):
        print(f"{i + 1}th : {logscore}")

    while True:
        # 결과 화면을 출력
        my_image.paste(startImage)
        my_draw.text((80, 100), f"Game over : {score}", fill = (0, 0, 0))
        for i, logscore in enumerate(scores):
            my_draw.text((100, 130 + 10 * i), f"{i + 1}th : {logscore}", fill = (255, 0, 0))
        joystick.disp.image(my_image)

        if not joystick.button_A.value and prev_button_A:
            print("다시 하기")
            time.sleep(0.1) # 풀링 방식에서 생기는 글리칭 해결을 위함
            JungDaeMan.position = np.array([30, 210 , 40, 240])
            JungDaeMan.shoulderAngel = 45
            JungDaeMan.power = 13
            break

        prev_button_A = joystick.button_A.value

