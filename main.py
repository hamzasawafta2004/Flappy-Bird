#Hamza sami Alsawafta 161395
import pygame,sys
from pygame.locals import *
import random
from pygame import mixer
pygame.init()
clock=pygame.time.Clock()
fps=60

width = 864
height = 768
#font
font=pygame.font.SysFont('Bauhaus Heavy',60)
#color
white=(255,255,255)
#var by game
ground_scroll=0
scroll_speed=4
bullet_speed=15
flying=False
game_over=False
pipe_gap=200
pipe_frequency=1500
last_pipe=pygame.time.get_ticks()-pipe_frequency
bullet_frequency=1500
last_bullet=pygame.time.get_ticks()-bullet_frequency
score=0
pass_pipe=False
# create screen
Screen= pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy Bird")
#load image
bg=pygame.image.load('night bg.jpg')
ground_img=pygame.image.load('ground.png')
button_img=pygame.image.load('restart.png')

def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    Screen.blit(img,(x,y))
def reset_game():
    pipe_group.empty()
    bullet_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(height/2)
    score=0
    return score
class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for num in range(1,4):
            img=pygame.image.load(f'Bird{num}.png')
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False
    def update(self):
        #gravity
        if flying==True:
           self.vel+=0.5
           if self.vel>8:
             self.vel=8
           if self.rect.bottom<768:
             self.rect.y+=int(self.vel)
        if game_over==False:
        #jump
           if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
               self.clicked=True
               self.vel=-10
           if pygame.mouse.get_pressed()[0]==0:
               self.clicked=False
        #handle the animation
           self.counter+=1
           flap_cooldown=5
           if self.counter>flap_cooldown:
              self.counter=0
              self.index+=1
              if self.index>=len(self.images):
                 self.index=0
           self.image=self.images[self.index]
        # rotate the bird
           self.image=pygame.transform.rotate(self.images[self.index],self.vel* -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('pipe (1).png')
        self.rect=self.image.get_rect()
        # top if position =1 ,bottom if position=-1
        if position==1 :
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-int(pipe_gap)/2]
        if position==-1 :
            self.rect.topleft = [x,y+int(pipe_gap)/2]
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.topleft=[x,y]
    def update(self):
        self.rect.x -= bullet_speed
        if self.rect.right < 0:
            self.kill()
class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
    def draw(self):
        action=False
        #get mouse position
        pos=pygame.mouse.get_pos()
        #check if mouse clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True
        #button
        Screen.blit(self.image,(self.rect.x,self.rect.y))
        return action
bird_group=pygame.sprite.Group()
pipe_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()

flappy=Bird(100,int(height/2))
bird_group.add(flappy)
#restart button instance
button=Button(width//2-50,height//2-100,button_img)

while True:# main game loop
    clock.tick(fps)
    #Background
    Screen.blit(bg,(0,0))
    bird_group.draw(Screen)
    bird_group.update()
    pipe_group.draw(Screen)
    bullet_group.draw(Screen)

    #ground scroll
    Screen.blit(ground_img, (ground_scroll, 700))
    #check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe=True

        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe=False
                score_sound=mixer.Sound('score sound.mp3')
                score_sound.play()

    draw_text(str(score),font,white,int(width/2),20)
    #collision
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top<0:
        game_over=True
    if pygame.sprite.groupcollide(bird_group,bullet_group,False,False) :
        game_over=True
    #check if bird has hit the ground
    if flappy.rect.bottom>=700:
        game_over=True
        flying=False
    if game_over==False and flying==True:
    # more new pipes
      time_now=pygame.time.get_ticks()
      if time_now-last_pipe>pipe_frequency:
          pipe_height=random.randint(-100,100)
          btm_pipe = Pipe(width, int(height / 2)+pipe_height, -1)
          top_pipe = Pipe(width, int(height / 2)+pipe_height, 1)
          pipe_group.add(btm_pipe)
          pipe_group.add(top_pipe)
          last_pipe=time_now
      if time_now-last_bullet>bullet_frequency:
          bullet_height=random.randint(-100,100)
          top_bullet = Bullet(width, int(height / 2)+bullet_height)
          bullet_group.add(top_bullet)
          last_bullet = time_now

    # ground scroll
      ground_scroll-=scroll_speed
      if abs(ground_scroll)>35:
         ground_scroll=0
      pipe_group.update()
      bullet_group.update()
    if game_over==True:
       if button.draw()==True:
           game_over=False
           score=reset_game()
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False:
            flying=True
    pygame.display.update()