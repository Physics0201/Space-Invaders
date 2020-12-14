import pygame
import os
import random
import time
pygame.font.init()
pygame.mixer.init()
height, width = 700,700
window = pygame.display.set_mode((height,width))
pygame.display.set_caption("Space invaders (not the original obviously but it works)")

#we are loading the images into the game
space_ship = pygame.image.load(os.path.join("assets", "red_ship.png"))
ship_img_2 = pygame.image.load(os.path.join("assets", "ship_img_2.png"))
space_alien = pygame.image.load(os.path.join("assets", "Alien.png"))
laser_sound = pygame.mixer.Sound("laser sound.mp3")
red_laser = pygame.image.load(os.path.join("assets", "ship laser.png"))

background_earth = pygame.image.load(os.path.join("assets", "background.png"))
class Laser:
    def __init__(self, x,y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img, (self.x,self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
            return not(self.y <= height and self.y >= 0)
    
    def collision(self,obj):
        return collide(obj,self)
        


class Ship:
    cooldown = 5
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser_Sound = laser_sound
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs):
        self.Cooldown()
        self.laser_Sound.play()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(objs):
                objs.health -= 10
                self.lasers.remove(laser)


    def Cooldown(self):
        if self.cool_down_counter >= self.cooldown:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot( self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()



class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x,y, health)
        self.ship_img = space_ship
        self.laser_img = red_laser
        self.laser_Sound = laser_sound
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.Cooldown()
        for laser in self.lasers:
            laser.move(vel)
            self.laser_Sound.play()
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif vel == -20:
                for obj in objs: 
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
            elif laser.collision(objs) and vel == -40:
                objs.health -= 10
                if laser in self.lasers:
                    self.lasers.remove(laser)
                       
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def shoot( self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-47,self.y - 20, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def healthbar(self,window):
        pygame.draw.rect(window, (255, 0 ,0), (self.x,self.y + self.ship_img.get_height() , self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255 ,0), (self.x,self.y + self.ship_img.get_height() , self.ship_img.get_width() * (self.health/self.max_health), 10))

class Player2(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x,y, health)
        self.ship_img = ship_img_2
        self.laser_img = red_laser
        self.laser_Sound = laser_sound
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.Cooldown()
        self.laser_Sound.play()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif vel == -20:
                for obj in objs: 
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
            elif laser.collision(objs) and vel == 40:
                objs.health -= 10
                if laser in self.lasers:
                    self.lasers.remove(laser)
                        
        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def shoot( self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-47,self.y - 20, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def healthbar(self,window):
        pygame.draw.rect(window, (255, 0 ,0), (self.x,self.y + self.ship_img.get_height() - 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255 ,0), (self.x,self.y + self.ship_img.get_height() - 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    
    def __init__(self, x, y, health = 100):
        super().__init__(x,y,health)
        self.ship_img = space_alien
        self.laser_img = red_laser
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
    def shoot( self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 5 ,self.y+30, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None 

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("langar", 50)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    enemy_laser_vel = 10
    laser_vel = 20

    player_vel = 5
    player = Player(325,450)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        window.blit(background_earth, (0,0))
        #draw text
        lives_label = main_font.render(f"Lives: {lives}",1, (255,255,255))
        level_label = main_font.render(f"Level: {level}",1, (255,255,255))

        window.blit(lives_label, (10,10))
        window.blit(level_label, (width - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(window)

        player.draw(window)

        if lost:
            lost_label = main_font.render("You Lost", 1, (255,255,255))
            window.blit(lost_label, (width/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            enemy_vel += 1
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x - player_vel + 50 > 0: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width + 50:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < width:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 120) == 1:
                enemy.shoot()
            
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > height + 250:
                lives -= 1
                enemies.remove(enemy)
            
            
        redraw_window()

        player.move_lasers(-laser_vel, enemies)
def versus():
    run = True
    FPS = 60
    lives = 5
    lives_player2 = 5
    main_font = pygame.font.SysFont("langar", 50)

    
    
    laser_vel = 40

    player_vel = 5
    player = Player(325,450)
    
    player2 = Player2(325,100)

    clock = pygame.time.Clock()

    lost1 = False
    lost2 = False
    lost_count = 0

    def redraw_window():
        window.blit(background_earth, (0,0))
        #draw text

        player.draw(window)
        player2.draw(window)

        if lost1:
            lost_label = main_font.render("You Lost: Player 1", 1, (255,255,255))
            window.blit(lost_label, (width/2 - lost_label.get_width()/2, 350))
        if lost2:
            lost_label = main_font.render("You Lost: Player 2", 1, (255,255,255))
            window.blit(lost_label, (width/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if player.health <= 0:
            lost1 = True
            lost_count += 1
        
        if player2.health <= 0:
            lost2 = True
            lost_count += 1

        if lost1:
            if lost_count > FPS * 5:
                run = False
            else:
                continue
        if lost1:
            if lost_count > FPS * 5:
                run = False
            else:
                continue


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        


        if keys[pygame.K_a] and player.x - player_vel + 50 > 0: #left
            player.x -= player_vel
        if keys[pygame.K_LEFT] and player2.x - player_vel + 50 > 0: #player 2 left
            player2.x -= player_vel
        #------------------------------------------------------------------------------    
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < width + 50: #right for both players
            player.x += player_vel
        if keys[pygame.K_RIGHT] and player2.x - player_vel + player2.get_width() < width + 50:
            player2.x += player_vel
        #-------------------------------------------------------------------------------
        if keys[pygame.K_w] and player.y - player_vel > 0: #up for both players
            player.y -= player_vel
        if keys[pygame.K_UP] and player2.y - player_vel > 0:
            player2.y -= player_vel
        #-------------------------------------------------------------------------------
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < width: #down for both players
            player.y += player_vel
        if keys[pygame.K_DOWN] and player2.y +player_vel + player2.get_height() < width:
            player2.y += player_vel
        #-------------------------------------------------------------------------------
        if keys[pygame.K_SPACE]: #Fire controls for both players
            player.shoot()
        if keys[pygame.K_RCTRL]:
            player2.shoot()
        
            
        if collide(player2, player):
            player.health -= 10
            player2.health -= 10
                

            
            
        redraw_window()

        player.move_lasers(-laser_vel,player2)
        player2.move_lasers(laser_vel,player)



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        window.blit(background_earth, (0,0))
        title_label = title_font.render("Press 1 to fight Aliens", 1, (255,255,255))
        title_label2 = title_font.render("Press 2 to fight Your Friends", 1, (255,255,255))
        window.blit(title_label, (width/2 - title_label.get_width()/2, 300))
        window.blit(title_label2, (width/2 - title_label2.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_1]:
            main()
        if keys[pygame.K_2]:
            versus()
    pygame.quit()
main_menu()