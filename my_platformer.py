import play
import pygame
from random import randint

canJump = False 
starting_y = 0

play.set_backdrop('light green')

score_txt = play.new_text(words='Score:', x=play.screen.right-100, y=play.screen.top-30, size=70)
score = play.new_text(words='0', x=play.screen.right-30, y=play.screen.top-30, size=70)

text = play.new_text(words='Tap SPACE to jump, LEFT/RIGHT to move', x=0, y=play.screen.bottom+60, size=70)

sea = play.new_box(
        color='blue', width=play.screen.width, height=50, x=0, y=play.screen.bottom+20
    )

walls = []

base_1 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_2 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (1 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_3 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (2 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_4 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (3 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_5 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (4 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_6 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (5 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_7 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (6 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)
base_8 = play.new_box(color='grey', x=(-play.screen.width / 2) + (75 / 2) + (7 * (play.screen.width / 8)), y=randint(10, 200), width=play.screen.width / 8, height=25, border_width=0, transparency=90)

walls.append(base_1)
walls.append(base_2)
walls.append(base_3)
walls.append(base_4)
walls.append(base_5)
walls.append(base_6)
walls.append(base_7)
walls.append(base_8)

finish_line = play.new_box(color='red', x=base_8.x + 20, y=base_8.y + 50, width=20, height=70)  
# coin_1_position = randint(1, 8)
# coin_2_position = randint(1, 8)
# coin_3_position = randint(1, 8)

win = play.new_text(words="Congrats! YOU just WON! ", x=0, y=0, font=None, font_size=30, color="green")
win.hide()

lose = play.new_text(words="Sorry! You Lost! Try Again! ", x=0, y=0, font=None, font_size=30, color="green")
lose.hide()
coins = []
for i in range(len(walls)):
    if randint(0, 3) == 1:
        coin = play.new_circle(color='yellow', x=walls[i].x, y=walls[i].y + 40, radius=10, border_width=0)
        coin.start_physics(can_move=True, stable=True, obeys_gravity=False, mass=10, friction=1, bounciness=0)
        coins.append(coin)
# coin_1 = play.new_circle(color='yellow', x=5, y=35, radius=13, border_width=0)
# coin_2 = play.new_circle(color='yellow', x=-50, y=255, radius=13, border_width=0)
# coin_3 = play.new_circle(color='yellow', x=260, y=115, radius=13, border_width=0)

# coins.append(coin_1)
# coins.append(coin_2)
# coins.append(coin_3)


ball = play.new_circle(color='red', x=base_1.x - 10, y=base_1.y + 30, radius=15, border_width=0)

@play.when_program_starts
def start():
    for base in walls:
        base.start_physics(
            can_move=True,
            stable=True, 
            obeys_gravity=False, 
            bounciness=0, 
            mass=1
        )
    ball.start_physics(
        can_move=True,
        stable=False, 
        x_speed=0, y_speed=0, 
        obeys_gravity=True, 
        bounciness=1, 
        mass=5
    )

    
@play.repeat_forever
async def game():
    await play.timer(seconds=1/48)
    global canJump
    global starting_y

    for coin in coins:
        if ball.is_touching(coin):
            coins.remove(coin)
            coin.hide()
            score.words = str(int(score.words) + 10)

    if play.key_is_pressed('right'):
        ball.physics.x_speed = 20
    elif play.key_is_pressed('left'):
        ball.physics.x_speed = -20
    else:
        ball.physics.x_speed = 0

    # if ball.is_touching(coin_1):
    #     score.words = str(int(score.words) + 1)
    #     coin_1.hide()
    #     coins.remove(coin_1)
    # elif ball.is_touching(coin_2):
    #     score.words = str(int(score.words) + 1)
    #     coin_2.hide()
    #     coins.remove(coin_2)
    # elif ball.is_touching(coin_3):
    #     score.words = str(int(score.words) + 1)
    #     coin_3.hide()
    #     coins.remove(coin_3)

    for base in walls:
        if ball.is_touching(base):
            canJump = True
            starting_y = base.y

    if play.key_is_pressed('up') and canJump and (starting_y + 100) > ball.y :
        ball.physics.y_speed = 50
    else:
        canJump = False

    if ball.is_touching(finish_line):
        for base in walls:
            base.hide()
        for coin in coins:
            coin.hide()
        sea.hide()
        ball.hide()
        win.show()

        text.hide()
        finish_line.hide()

    if ball.is_touching(sea):
        for base in walls:
            base.hide()
        for coin in coins:
            coin.hide()
        sea.hide()
        ball.hide()

        lose.show()
        text.hide()

        finish_line.hide()

play.start_program()
