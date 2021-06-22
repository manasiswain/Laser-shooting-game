import pygame
pygame.font.init()
pygame.mixer.init()
WIDTH=900
HEIGHT=500
BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
MAX_BULLETS=3
FPS=60
BULLET_VEL=15
VEL=5
YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Laser Game")
yellow_spaceship_image=pygame.image.load("resources/spaceship_yellow.png")
yellow_spaceship=pygame.transform.scale(yellow_spaceship_image,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
yellow_spaceship=pygame.transform.rotate(yellow_spaceship,90.0)
red_spaceship_image=pygame.image.load("resources/spaceship_red.png")
red_spaceship=pygame.transform.scale(red_spaceship_image,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
red_spaceship=pygame.transform.rotate(red_spaceship,-90.0)
SPACE_IMAGE=pygame.image.load("resources/space.png")
SPACE=pygame.transform.scale(SPACE_IMAGE,(WIDTH,HEIGHT))
BULLET_HIT_SOUND=pygame.mixer.Sound("resources/Grenade+1.mp3")
BULLET_FIRE_SOUND=pygame.mixer.Sound("resources/Gun+Silencer.mp3")
BG_SOUND=pygame.mixer.Sound("resources/guitar-background-beat.mp3")
WIN_SOUND=pygame.mixer.Sound("resources/win.mp3")
def draw_window(red,yellow,red_bullets,yellow_bullets,RED_HEALTH,YELLOW_HEALTH,ini):
    if(ini==0):
        ini+=1
        ct=5
        while(ct>0):
            WINDOW.blit(SPACE, (0, 0))
            f1=pygame.font.Font(None, 60)
            f2=pygame.font.Font(None, 40)
            font = pygame.font.Font(None, 30)
            line1 = f1.render(f"RULES", True, (255, 255, 255))
            line2 = font.render(f"1)LCTRL TO FIRE BULLETS PRESS CONTROL AND TO MOVE USE A W S D", True, (255, 255, 255))
            line3 = font.render(f"2)RCTRL TO FIRE BULLETS PRESS RETURN AND TO MOVE USE LEFT UP DOWN RIGHT", True,
                        (255, 255, 255))
            line4 = font.render(f"3)SPACESHIP HEALTH IS 10", True, (255, 255, 255))
            line5 = f2.render(f"TIMER: {ct}", True, (255, 0, 0))
            WINDOW.blit(line1, (WIDTH//2-50, 0))
            WINDOW.blit(line2, (50, 60))
            WINDOW.blit(line3, (50, 90))
            WINDOW.blit(line4, (50, 120))
            WINDOW.blit(line5, (50, 150))
            pygame.display.update()
            ct -= 1
            pygame.time.delay(1000)

    else:
        WINDOW.blit(SPACE,(0,0))
        pygame.draw.rect(WINDOW, (255,255,255), BORDER)
        font = pygame.font.Font(None, 30)
        yellow_health_text = font.render(f"Health: {YELLOW_HEALTH}", True, (255, 255, 255))
        red_health_text = font.render(f"Health: {RED_HEALTH}", True, (255, 255, 255))
        WINDOW.blit(yellow_health_text,(0, 0))
        WINDOW.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
        WINDOW.blit(yellow_spaceship,(yellow.x,yellow.y))
        WINDOW.blit(red_spaceship,(red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW,(255,0,0),bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW,(255,255,0),bullet)
    pygame.display.update()
def draw_winner(text):
    font = pygame.font.Font(None, 60)
    winner=font.render(f" {text}", True, (255, 255, 255))
    WINDOW.blit(SPACE, (0, 0))
    WINDOW.blit(winner,(WIDTH//2-winner.get_width()+150,HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(3000)

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif(bullet.x>WIDTH):
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif (bullet.x <0):
            red_bullets.remove(bullet)

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x!=0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_w] and yellow.y!=0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_d] and yellow.x+yellow.width!=BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y+yellow.height!=HEIGHT-15: # DOWN
        yellow.y += VEL

def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x!=BORDER.x+10:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_UP] and red.y!=0:  # UP
        red.y-= VEL
    if keys_pressed[pygame.K_DOWN] and red.y+red.height!=HEIGHT-15: # DOWN
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+red.width!=WIDTH :  # RIGHT
        red.x += VEL
def main():
    ini=0
    BG_SOUND.play()
    red=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets=[]
    red_bullets=[]
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    clock=pygame.time.Clock()
    run=True
    while(run==True):
        clock.tick(FPS)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                pygame.quit()
            if(event.type==pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                if(event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS):
                    BULLET_FIRE_SOUND.play()
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2,10,5)
                    yellow_bullets.append(bullet)
                if (event.key == pygame.K_RETURN and len(red_bullets)<MAX_BULLETS):
                    BULLET_FIRE_SOUND.play()
                    bullet = pygame.Rect(red.x , red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
            if(event.type==RED_HIT):
                BULLET_HIT_SOUND.play()
                RED_HEALTH-=1
            if (event.type == YELLOW_HIT):
                BULLET_HIT_SOUND.play()
                YELLOW_HEALTH-=1
        WINNER_TEXT=""
        if(RED_HEALTH<=0):
            WINNER_TEXT="YELLOW WINS!!"
        if(YELLOW_HEALTH<= 0):
            WINNER_TEXT="RED WINS!!"
        if(WINNER_TEXT!=""):
            BG_SOUND.stop()
            WIN_SOUND.play()
            draw_winner(WINNER_TEXT)
            font = pygame.font.Font(None, 30)
            WINDOW.blit(SPACE, (0, 0))
            ct=10
            while(ct>=1):
                end = font.render(f"Do yo want to play again!PRESS RETURN. TO QUIT PRESS ESC TIMER: {str(ct)}", True, (255, 255, 255))
                WINDOW.blit(end, (WIDTH//2-360, HEIGHT // 2))
                pygame.display.update()
                ct-=1
                pygame.time.delay(1000)
                WINDOW.blit(SPACE, (0, 0))
                pygame.display.update()
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        pygame.quit()
                    if(event.type==pygame.KEYDOWN):
                        if(event.key==pygame.K_ESCAPE):
                            pygame.quit()
                        if(event.key==pygame.K_RETURN):
                            main()
            main()


        keys_pressed=pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        if(ini==0):
            draw_window(red, yellow,red_bullets,yellow_bullets,RED_HEALTH,YELLOW_HEALTH,ini)
            ini+=1
        else:
            draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH, ini)



main()

