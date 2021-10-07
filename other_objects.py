import pygame as pg
from settings import *
import pytweening as tween
vec=pg.math.Vector2

from random import randrange,choice
class Button:
    def __init__(self,game):
        self.game=game
        self.image=self.game.button
        self.rect=self.image.get_rect()
    def draw_button(self,text,x,y):
        self.rect.x = x
        self.rect.y = y
        self.text=text
        self.game.screen.blit(self.image, self.rect)
        self.game.draw_text(self.text, self.game.title_font, 40, WHITE, self.rect.x + 100, self.rect.y+30, align='center')
    def on_button(self):
        self.image=self.game.button2
        self.game.screen.blit(self.image, self.rect)
        self.game.draw_text(self.text, self.game.title_font, 40, WHITE, self.rect.x + 100, self.rect.y+30, align='center')
    def off_button(self):
        self.image=self.game.button


class Wight_Button:
    def __init__(self, game):
        self.game = game
        self.image = pg.Surface((100,50))
        self.image.fill(LIGHTGREY )
        self.rect=self.image.get_rect()
        self.delete=False


    def draw_button(self, text, x, y):
            self.rect.x = x
            self.rect.y = y
            self.text = text
            self.game.screen.blit(self.image, self.rect)
            self.game.draw_text(self.text, self.game.title_font, 20, WHITE, self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2,
                            align='center')


    def on_button(self,deld):
        self.delete=deld
        if not self.delete:
            self.image.fill(LIGHTGREY)
            self.game.screen.blit(self.image, self.rect)
            self.game.draw_text(self.text, self.game.title_font, 20, WHITE, self.rect.x + self.rect.width / 2,
                            self.rect.y + self.rect.height / 2,
                            align='center')

    def off_button(self):
            self.image = pg.Surface((100, 50))
            self.image.fill(DARKGREY)



class Menu_img(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self.group = game.menu_sprites,game.for_menu_image
        self._layer = 0
        pg.sprite.Sprite.__init__(self, self.group)
        self.image=self.game.menu_animation[0]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.current_frame=0
        self.last_update = 0
        self.point=False
    def update(self):
        now = pg.time.get_ticks()
        mx, my = pg.mouse.get_pos()
        if self.rect.collidepoint((mx, my)):
            self.point=True
            if self.point:
                if   now - self.last_update > 250:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(UNSLEEP_MENU_ANIMATION)
                    self.image = self.game.unsleep_menu_animation[self.current_frame]
                    center=self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center=center
        else:
                if   now - self.last_update > 250:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(MENU_ANIMATION)
                    self.image = self.game.menu_animation[self.current_frame]
                    center=self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center=center

class Main_fire_fly(pg.sprite.Sprite):
        def __init__(self,game,pos):
            self.game = game
            self.group=game.menu_sprites
            self._layer=1
            pg.sprite.Sprite.__init__(self,self.group)
            self.pos=pos
            self.image = game.firefly_animation[0]
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.pos = vec(pos)
            self.hit_rect = self.rect
            self.current_frame = 0
            self.last_update = 0
            self.tween = tween.easeInOutSine
            self.step = 0
            self.dir = 1
            self.vel = randrange(100, 200)
            self.num = 1
            self.prime_width=self.rect.width
            list = [2, 3, 4, 5]
            self.num = choice(list)
            self.image = pg.transform.scale(self.image,
                                            (int(self.rect.width * self.num), int(self.rect.height * self.num)))
            self.rect = self.image.get_rect()
        def update(self):
            self.animate()
            self.pos.y -= self.vel * self.game.dt
            self.rect.centery = self.pos.y
            self.hit_rect.centery = self.pos.y
            # bobing motion
            offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
            self.rect.centerx = self.pos.x + offset * self.dir
            self.hit_rect.centerx = self.pos.x + offset * self.dir
            self.step += BOB_SPEED
            if self.step > BOB_RANGE:
                self.step = 0
                self.dir *= -1
            if self.rect.top <self.game.map_rect.top-200:
                self.vel = randrange(100, 200)
                list = [2, 3, 4, 5]
                self.num = choice(list)
                self.pos.y = self.game.map_rect.bottom/2
            hits = pg.sprite.spritecollide(self, self.game.for_menu_image, False)
            if hits:
                for num, sprite in enumerate(hits):
                        if self.rect.width/2==self.prime_width or self.rect.width/3==self.prime_width:  # and self.game.all_sprites.get_layer_of_sprite(self)!=PLAYER_LAYER :
                            self.game.menu_sprites.change_layer(self, sprite._layer-1)
                        else:
                            self.game.menu_sprites.change_layer(self, sprite._layer +1)






        def animate(self):
            now = pg.time.get_ticks()

            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(FIREFLY_ANIMATION)
                self.image = self.game.firefly_animation[self.current_frame]
                self.rect = self.image.get_rect()
                self.image = pg.transform.scale(self.image,
                                                (int(self.rect.width * self.num), int(self.rect.height *self.num)))
                self.rect = self.image.get_rect()




