import math
import mouse
import graphics
import time
import sound
import random

def interpolate(start: float, end: float, fraction: float) -> float:
    return start * (1.0 - fraction) + end * fraction

def run() -> None:
    mouse_x: float
    mouse_x_last: float
    ball_x: float
    ball_y: float
    ball_x_current: float
    ball_y_current: float
    paddle_size: float
    paddle_current: float
    paddle_last: float
    screen_height: float
    screen_width: float
    game_running: bool
    game_over: bool
    ball_size: float
    angle: float
    speed: float
    last_time: float
    start_time: float
    fps_loops_counter: float
    delta_time: float
    fps: int
    last_touched: int
    difficulty_multiplier: float
    pi: float
    spin_duration: float
    spin_time: float
    spin_amount: float
    
    pi = 3.141592653589
    
    screen_height = graphics.screen_height()
    screen_width = graphics.screen_width()
    
    # ----- Settings ----- #
    paddle_size = 100.0 # Overall size of paddle
    ball_size = 20.0 # Overall size of ball
    speed = 300.0 # Inital speed of ball
    difficulty_multiplier = 1.05 # How fast the ball speed increases everytime it hits the paddle
    spin_duration = 5.0 # How long the ball will continue to spin
    # ----- Settings ----- #
    
    paddle_current = 0.0 # Current position of the paddle
    angle = 0.0
    game_running = False
    game_over = False
    mouse_x_last = 0.0
    
    start_time = time.time()
    fps_loops_counter = 0.0
    last_time = time.time()
    fps = 0
    last_touched = 0 # Last boundry touched: paddle 0, left 2, right 3, top 4
    
    spin_time = spin_duration
    spin_amount = 0.0

    while(not game_over):
        # ----- Delta Time ----- #
        delta_time = time.time() - last_time
        last_time = time.time()
        # ----- Delta Time ----- #
        
        # ----- FPS ----- #
        fps_loops_counter = fps_loops_counter + 1.0
        if (time.time() - start_time) > 1.0:
            fps = int(fps_loops_counter / (time.time() - start_time))
            fps_loops_counter = 0.0
            start_time = time.time()
        graphics.draw_text("FPS: " + str(fps), screen_width/2.0-40.0, screen_height/2.0-20.0)
        # ----- FPS ----- #
        
        graphics.draw_text("Score: " + str(int(speed)), -screen_width/2.0+100.0, screen_height/2.0-20.0, 20.0)
        
        paddle_last = paddle_current
        
        mouse_x = mouse.x()
        if (mouse_x == mouse_x):
            mouse_x_last = mouse_x
            paddle_current = interpolate(paddle_current, mouse_x, delta_time*15.0)
        else:
            paddle_current = interpolate(paddle_current, mouse_x_last, delta_time*15.0)
        
        graphics.draw_rect(paddle_current, -screen_height/2.0 + paddle_size/2.0, paddle_size, paddle_size/3.0, "red")
        print(math.degrees(angle))
        if (spin_time < spin_duration):
            if (last_touched != 0):
                spin_time = spin_duration
            else:
                if (math.degrees(angle) + spin_amount > 157.5):
                    angle = math.radians(interpolate(math.degrees(angle), 157.5, spin_time/spin_duration))
                elif (math.degrees(angle) + spin_amount < 22.5):
                    angle = math.radians(interpolate(math.degrees(angle), 22.5, spin_time/spin_duration))
                else:
                    angle = math.radians(interpolate(math.degrees(angle), math.degrees(angle) + spin_amount, spin_time/spin_duration))
                spin_time = spin_time + delta_time
        
        if (not game_running):
            ball_x = paddle_current
            ball_y = -screen_height/2.0 + paddle_size/2.0 + ball_size*1.5
            
            graphics.draw_text("Click to Start!", 0.0,0.0, 20.0)
            
            if (mouse.down(0)):
                game_running = True
                angle = math.radians(float(random.randrange(45,135,1)))
        else:
            if (last_touched != 3 and ball_x + (ball_size/2.0) >= screen_width/2.0):
                angle = math.radians(math.degrees(-angle) + 180.0)
                last_touched = 3
            elif (last_touched != 2 and ball_x - (ball_size/2.0) <= -screen_width/2.0):
                angle = math.radians(math.degrees(-angle) + 180.0)
                last_touched = 2
            elif (last_touched != 4 and ball_y + (ball_size/2.0) >= screen_height/2.0):
                angle = -angle
                last_touched = 4
            elif (ball_y + (ball_size/2.0) <= -screen_height/2.0):
                game_over = True
            
            if (last_touched != 0 and ball_y - ball_size/2.0 <= -screen_height/2.0 + paddle_size/3.0 + paddle_size/3.0):
                if (paddle_current - paddle_size/2.0 < ball_x + (ball_size/2.0) and paddle_current + paddle_size/2.0 > ball_x - (ball_size/2.0)):
                    #angle = math.radians(math.degrees(-angle))
                    angle = math.radians(paddle_current - ball_x + 90.0)
                    
                    spin_amount = (paddle_current*1000.0 - paddle_last*1000.0)/2000.0
                    spin_time = 0.0
                    
                    speed = speed*difficulty_multiplier
                    sound.play("https://cdn.discordapp.com/attachments/749653590326378499/902356910538383400/sfx-pop.mp3")
                #else:
                    #game_over = True
                last_touched = 0
            
            ball_x = (math.cos(angle)*speed*delta_time + ball_x)
            ball_y = (math.sin(angle)*speed*delta_time + ball_y)
            
            #ball_x_current = interpolate(math.cos(angle)*speed*delta_time + ball_x_current, ball_x, delta_time*30.0)
            #ball_y_current = interpolate(math.sin(angle)*speed*delta_time + ball_y_current, ball_y, delta_time*30.0)
                
        graphics.draw_oval(ball_x, ball_y, ball_size, ball_size, "green")
        
        graphics.update()
        #graphics.wait(1)
    while (not mouse.down(0)):
        # ----- FPS ----- #
        fps_loops_counter = fps_loops_counter + 1.0
        if (time.time() - start_time) > 1.0:
            fps = int(fps_loops_counter / (time.time() - start_time))
            fps_loops_counter = 0.0
            start_time = time.time()
        graphics.draw_text("FPS: " + str(fps), screen_width/2.0-40.0, screen_height/2.0-20.0)
        # ----- FPS ----- #
        
        graphics.draw_text("Game Over...", 0.0,0.0, 20.0)
        graphics.draw_text("Score: " + str(int(speed)), 0.0,-20.0, 20.0)
        graphics.update()
        #graphics.wait(1)
    return None

def main() -> None:
    graphics.double_buffer()
    while (True):
        graphics.update()
        run()
    return None
main()
