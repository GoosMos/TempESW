import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import numpy as np
import JungDeaMan
import Joystick
from BasketBall import BasketBall
from BasketBall import Hoop

print("Hellllllll")


joystick = Joystick.Joystick()
JungDaeMan = JungDeaMan.JungDeaMan(joystick.width, joystick.height)
balls = []
LifeCount = 5
hoop = Hoop()

# 이미지의 모드 설정 == 디스플레이 전체에 대한 초기화
my_image = Image.new("RGB", (joystick.width, joystick.height)) 
my_draw = ImageDraw.Draw(my_image)
my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
print("HElloo")


while True:
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
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

    if not joystick.button_A.value:
        LifeCount -= 1
        print("Shoot")
        print("남은 시도 횟수 : ", LifeCount)
        balls.append(BasketBall(JungDaeMan.position[0], JungDaeMan.position[1], JungDaeMan.power, JungDaeMan.shoulderAngel))
        # 함수 호출 필요

    for ball in balls:
        ball.move()
        my_draw.ellipse((ball.x - 5, ball.y - 5, ball.x + 5, ball.y + 5), fill = (0, 0, 0))

    if LifeCount == 0: break

    JungDaeMan.move(command)

    #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
    my_draw.ellipse(tuple(JungDaeMan.position), outline = JungDaeMan.outline, fill = (0, 0, 0))
    my_draw.rectangle((0, 0, joystick.width, 5), fill = (255, 0, 0, 100))
    
    my_draw.rectangle((hoop.hoop_x, hoop.hoop_y, hoop.hoop_x + hoop.hoop_width, hoop.hoop_y + hoop.hoop_hegith), outline=(0, 0, 255))
    my_draw.rectangle((0, 0, (JungDaeMan.power - 5) * 24, 5), fill = (255, 255, 0, 100))
    for i in range(1, LifeCount + 1) :
        my_draw.ellipse((0 + 20 * i, 15, 0 + 20 * i + 10, 25), outline = JungDaeMan.outline, fill = (0, 0, 0))
    # balls = [ball for ball in balls if ball.x <= joystick.width and ball.y <= joystick.height]
    joystick.disp.image(my_image)