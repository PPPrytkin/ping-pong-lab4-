from tkinter import *
import random


WIDTH = 900
HEIGHT = 300
PAD_W = 20
PAD_H = 70
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 20
BALL_RADIUS = 25
INITIAL_SPEED = 5
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
right_line_distance = WIDTH - PAD_W
PAUSE = False

def pause():
    global PAUSE, BALL_X_SPEED, BALL_Y_SPEED, PAUSE_X_SPEED, PAUSE_Y_SPEED, WIDTH, HEIGHT
    if PAUSE == False:
        PAUSE_X_SPEED, PAUSE_Y_SPEED = BALL_X_SPEED, BALL_Y_SPEED
        BALL_X_SPEED = 0
        BALL_Y_SPEED = 0
        PAUSE = True
        c.create_rectangle(0, 0, WIDTH, HEIGHT, fill='black', stipple='gray75', tags='p0')
        c.create_line(WIDTH/2-50, HEIGHT/2-100, WIDTH/2-50, HEIGHT/2+100, width='50', fill='white', tags='p1')
        c.create_line(WIDTH/2+50, HEIGHT/2-100, WIDTH/2+50, HEIGHT/2+100, width='50', fill='white', tags='p2')
    elif PAUSE == True:
        c.delete('p0','p1','p2')
        BALL_X_SPEED, BALL_Y_SPEED = PAUSE_X_SPEED, PAUSE_Y_SPEED
        PAUSE = False

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
 
def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)
    c.coords(LEFT_PAD, PAD_W/2, HEIGHT/2-PAD_H/2, PAD_W/2, HEIGHT/2+PAD_H/2)
    c.coords(RIGHT_PAD, WIDTH-PAD_W/2, HEIGHT/2-PAD_H/2, WIDTH-PAD_W/2, HEIGHT/2+PAD_H/2)

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

root = Tk()
root.title("Ping-Pong")

c = Canvas(root, width=WIDTH, height=HEIGHT, background="white", bd=0, highlightthickness=0)
c.create_rectangle(0, 0, WIDTH/2, HEIGHT, fill='#f44336', outline="")
c.create_rectangle(WIDTH/2, 0, WIDTH, HEIGHT, fill='#3f51b5', outline="")
c.pack()

BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2,
                     HEIGHT/2-BALL_RADIUS/2,
                     WIDTH/2+BALL_RADIUS/2,
                     HEIGHT/2+BALL_RADIUS/2, fill="white", outline="")

LEFT_PAD = c.create_line(PAD_W/2, HEIGHT/2-PAD_H/2, PAD_W/2, HEIGHT/2+PAD_H/2, width=PAD_W, fill="white")

RIGHT_PAD = c.create_line(WIDTH-PAD_W/2, HEIGHT/2-PAD_H/2, WIDTH-PAD_W/2, HEIGHT/2+PAD_H/2, width=PAD_W, fill="white")


p_1_text = c.create_text(WIDTH-WIDTH/4, 20,
                         text=PLAYER_1_SCORE,
                         font=("Ubuntu", 34, "bold"),
                         fill="white")
 
p_2_text = c.create_text(WIDTH/4, 20,
                          text=PLAYER_2_SCORE,
                          font=("Ubuntu", 34, "bold"),
                          fill="white")

BALL_X_CHANGE = 20
BALL_Y_CHANGE = 0
 
def move_ball():
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2
    if ball_right + BALL_X_SPEED < right_line_distance and \
            ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                update_score("left")
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED)
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT:
        bounce("ricochet")

PAD_SPEED = 20
LEFT_PAD_SPEED = 0
RIGHT_PAD_SPEED = 0
def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, 
            RIGHT_PAD: RIGHT_PAD_SPEED}
    for pad in PADS:
        c.move(pad, 0, PADS[pad])
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])

 
def main():
    move_ball()
    move_pads()
    # вызываем саму себя каждые 30 миллисекунд
    root.after(30, main)

c.focus_set()

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED, PAUSE
    if not PAUSE:
        if event.keysym == "w":
            LEFT_PAD_SPEED = -PAD_SPEED
        elif event.keysym == "s":
            LEFT_PAD_SPEED = PAD_SPEED
        elif event.keysym == "Up":
            RIGHT_PAD_SPEED = -PAD_SPEED
        elif event.keysym == "Down":
            RIGHT_PAD_SPEED = PAD_SPEED
    if event.keysym == "space":
        pause()

c.bind("<KeyPress>", movement_handler)

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in "ws":
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0
 

c.bind("<KeyRelease>", stop_pad)
main()
root.mainloop()