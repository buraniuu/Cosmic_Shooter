from pygame import *
from random import randint
from time import time as timer
import pygame_menu
init()
class GameSprite(sprite.Sprite):
    def __init__(self,player_w, player_h, player_x, player_y, player_image,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w,player_h))
        self.rect = self.image.get_rect()
        self.player_speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))
    

class Player(GameSprite):
    
    def moving(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 1100:
            self.rect.x += self.player_speed
        if keys_pressed[K_a] and self.rect.x > 40:
            self.rect.x -= self.player_speed

    def fire(self):
        bullet = Bullet(10,20,self.rect.centerx, self.rect.top,'bullet1.png',-7)
        bullets.add(bullet)

    def boss_fire(self):
        boss_bullet = Bullet(22,22,self.rect.centerx, self.rect.top,'bulletboss2.png',-5)
        boss_bullets.add(boss_bullet)

class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.player_speed
        global lost
        if self.rect.y > 750:
            self.rect.y = 0
            self.rect.x = randint(30, 1080)
            lost +=1

class Bullet(GameSprite):

    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y <= 0:
            self.kill()

class Asteroid(GameSprite):

    def update(self):
        self.rect.y += self.player_speed
        if self.rect.y > 750:
            self.rect.y = 0
            self.rect.x = randint(30, 1080)

class HealthBar(sprite.Sprite):
    def __init__(self,color1, color2, color3, bar_x, bar_y, bar_width, bar_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.bar_width = bar_width
        self.bar_height = bar_height
        self.image = Surface((self.bar_width,self.bar_height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = bar_x
        self.rect.y = bar_y

    def draw_bar(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()
boss_bullets = sprite.Group()
lost = 0
win_w = 1200
win_h = 700
win = display.set_mode((win_w, win_h))
display.set_caption('spacefighter')
backgr = transform.scale(image.load('background3.png'), (win_w,win_h))
clock = time.Clock()
player = Player(70,70,400,600,'player.png',10)
font.init()
mixer.init()
mixer.music.load('music.ogg')
mixer.music.set_volume(0.3)
fire_sound = mixer.Sound('bullet_sound.ogg')
boss_fire_sound = mixer.Sound('boss_fire.ogg')
mixer.music.play()

def main():
    monsters1 = sprite.Group()
    monsters2 = sprite.Group()
    monsters3 = sprite.Group()
    monsters4 = sprite.Group()
    monsters5 = sprite.Group()
    monsters6 = sprite.Group()
    num_fire = 0
    power_num_fire = 0
    rel_time = False
    power_rel_time = False
    font_1 = font.Font(None,44)
    bite = 0
    # color1,color2,color3,x,y,width,height
    healthbar_green = HealthBar(82,222,80,940,50,150,20)
    healthbar_red = HealthBar(207,21,21,1040,50,50,20)
    healthbar_red_low = HealthBar(207,21,21,990,50,50,20)
    healthbar_orange = HealthBar(194,93,35,940,50,50,20)
    healthbar_lose = HealthBar(207,21,21,940,50,150,20)
    life = 3

    boss = sprite.Group()

    for _ in range(1):    
        monster1 = Enemy(50,50,randint(30,1080),0,'enemy1_2.png',randint(1,3))
        monsters1.add(monster1)
    for _ in range(1):
        monster2 = Enemy(50,50,randint(30,1080),0,'enemy2_1.png',randint(1,3))
        monsters2.add(monster2)
    for _ in range(1):
        monster3 = Enemy(50,50,randint(30,1080),0,'enemy2_2.png',randint(1,3))
        monsters3.add(monster3)
    for _ in range(1):
        monster4 = Asteroid(45,45,randint(30,1080),0,'meteor_2.png', randint(1,2))
        monsters4.add(monster4)
    for _ in range(1):
        monster5 = Asteroid(45,45,randint(30,1080),0,'meteor_3.png', randint(1,2))
        monsters5.add(monster5)
    for _ in range(1):
        monster6 = Asteroid(45,45,randint(30,1080), 0, 'meteor_4.png',randint(1,2))
        monsters6.add(monster6)
    for _ in range(1):
        boss_ = Enemy(80,80,randint(30,1080),0,'boss3.png',1)
        boss.add(boss_)
    finish = False
    while  True:

        for e in event.get():
            if e.type == QUIT:
                return        
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if num_fire < 5 and rel_time == False:    
                    player.fire()
                    fire_sound.play()
                    num_fire += 1
                elif num_fire >= 5 and rel_time == False:
                    rel_time = True
                    seconds = timer()
            if e.type == MOUSEBUTTONDOWN and e.button == 3:
                if power_num_fire < 2 and power_rel_time == False:
                    player.boss_fire()
                    boss_fire_sound.play()
                    power_num_fire += 1
                elif power_num_fire >= 2 and power_rel_time == False:
                    power_rel_time = True
                    power_seconds = timer()

        if not finish:

            win.blit(backgr,(0,0))
            lose_font = font_1.render('Пропущено: '+ str(lost),1,(222,255,235))
            bite_font = font_1.render('Сбито: '+ str(bite),1,(222,255,235))
            win_font = font_1.render('YOU WIN!',1,(251,255,0))
            losing_font = font_1.render('YOU LOSE!',1, (254,0,0))
            waiting_font = font_1.render('Wait, reload...',1,(199,255,205))
            win.blit(lose_font,(50,50))
            win.blit(bite_font,(50,120))
            player.reset()
            player.moving()
            bullets.update()
            boss_bullets.update()
            monsters1.update()
            monsters2.update()
            monsters3.update()
            monsters4.update()
            monsters5.update()
            monsters6.update()
            boss.update()
            bullets.draw(win)
            boss_bullets.draw(win)
            monsters1.draw(win)
            monsters2.draw(win)
            monsters3.draw(win)
            monsters4.draw(win)
            monsters5.draw(win)
            monsters6.draw(win)
            boss.draw(win)

            if rel_time == True:
                new_seconds = timer()
                if new_seconds-seconds < 5:
                    win.blit(waiting_font,(500,450))
                else:
                    num_fire = 0
                    rel_time = False

            if power_rel_time == True:
                power_new_seconds = timer()
                if power_new_seconds- power_seconds < 2:
                    win.blit(waiting_font,(60,300))
                else:
                    power_num_fire = 0
                    power_rel_time = False

            collides1 = sprite.groupcollide(bullets, monsters1, True, True) or sprite.groupcollide(boss_bullets, monsters1, True, True)
            collides2 = sprite.groupcollide(bullets, monsters2, True, True) or sprite.groupcollide(boss_bullets, monsters2, True, True)
            collides3 = sprite.groupcollide(bullets, monsters3, True, True) or sprite.groupcollide(boss_bullets, monsters3, True, True)
            collides4 = sprite.groupcollide(boss_bullets, monsters4, True, True)
            collides5 = sprite.groupcollide(boss_bullets, monsters5, True, True)
            collides6 = sprite.groupcollide(boss_bullets, monsters6, True, True)
            collides7 = sprite.groupcollide(boss_bullets, boss, True, True)

            for collide in collides1:
                monster1 = Enemy(50, 50, randint(30,1080), 0, 'enemy1_2.png', randint(1,3))
                bite+=1
                monsters1.add(monster1)
            
            for collide in collides2:
                monster2 = Enemy(50, 50, randint(30,1080), 0, 'enemy2_1.png', randint(1,3))
                bite+=1
                monsters2.add(monster2)

            for collide in collides3:
                monster3 = Enemy(50, 50, randint(30,1080), 0, 'enemy1_2.png', randint(1,3))
                bite+=1
                monsters3.add(monster3)
            
            for collide in collides4:
                monster4 = Asteroid(50, 50, randint(30,1080), 0, 'meteor_2.png', randint(1,3))
                bite+=1
                monsters4.add(monster4)

            for collide in collides5:
                monster5 = Asteroid(50, 50, randint(30,1080), 0, 'meteor_3.png', randint(1,3))
                bite+=1
                monsters5.add(monster5)

            for collide in collides6:
                monster6 = Asteroid(50, 50, randint(30,1080), 0, 'meteor_4.png', randint(1,3))
                bite+=1
                monsters6.add(monster6)

            for collide in collides7:
                boss_ = Enemy(80, 80, randint(0,1380), 0, 'boss3.png', 1)
                bite +=1
                boss.add(boss_)

            if sprite.spritecollide(player, monsters1, True ) or sprite.spritecollide(player, monsters2, True) or sprite.spritecollide(player, monsters3, True) or sprite.spritecollide(player,monsters4,True) or sprite.spritecollide(player, monsters4, True) or sprite.spritecollide(player, monsters5, True) or sprite.spritecollide(player, monsters6, True) or sprite.spritecollide(player, boss, True):
                life-=1

            if bite >= 10 :
                win.blit(win_font,(600,350))
                finish = True
                win_menu()

            if lost >= 10 or life == 0:
                win.blit(losing_font,(600,350))
                finish = True
                healthbar_lose.draw_bar()
                end_menu()

            if life == 3:
                healthbar_green.draw_bar()
            if life == 2:
                healthbar_green.draw_bar()
                healthbar_red.draw_bar()
            if life == 1:
                healthbar_green.draw_bar()
                healthbar_red.draw_bar()
                healthbar_red_low.draw_bar()
                healthbar_orange.draw_bar()


        display.update()
        clock.tick(60)

def start_menu():
    menu = pygame_menu.Menu('Cosmic Shooter', win_w, win_h, theme = pygame_menu.themes.THEME_BLUE)
    menu.add.label('Kill 10 enemies and dont skip 15')
    menu.add.button('Start',main)
    menu.add.button('exit',pygame_menu.events.EXIT)
    menu.mainloop(win)

def end_menu():
    menu = pygame_menu.Menu('Cosmic Shooter', win_w, win_h, theme = pygame_menu.themes.THEME_BLUE)
    menu.add.label('You lose')
    menu.add.button('exit', pygame_menu.events.EXIT)
    menu.mainloop(win) 

def win_menu():
    menu = pygame_menu.Menu('Cosmic Shooter', win_w, win_h, theme = pygame_menu.themes.THEME_BLUE) 
    menu.add.label('You win')
    menu.add.button('exit', pygame_menu.events.EXIT)
    menu.mainloop(win) 
    

start_menu()
